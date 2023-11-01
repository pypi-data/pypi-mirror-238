"""
Note that pyrightconfig.json is set to ignore this file. If our spark integration becomes more well supported,
we should undo that and fix the type errors.
"""
import os
import pathlib
import shlex
import subprocess
import sys
import warnings

# pyspark isn't a requirement for coiled, but
# maybe we should have some try/except with an explanation
import pyspark  # type: ignore
from dask.distributed import Client
from distributed.diagnostics.plugin import SchedulerPlugin, WorkerPlugin
from pyspark.sql import SparkSession

from coiled import Cluster

SPARK_VERSION = pyspark.__version__
# sc._jvm.org.apache.hadoop.util.VersionInfo.getVersion()
HADOOP_AWS_VERSION = "3.3.4"
AWS_JAVA_SDK_BUNDLE_VERSION = "1.12.262"


class SparkMaster(SchedulerPlugin):
    name = "spark-master"
    cls = "org.apache.spark.deploy.master.Master"

    def start(self, scheduler):
        self.scheduler = scheduler
        self.scheduler.add_plugin(self)

        path = pathlib.Path(pyspark.__file__).absolute()
        module_loc = path.parent
        os.environ["SPARK_HOME"] = str(module_loc)
        os.environ["PYSPARK_PYTHON"] = sys.executable

        host = scheduler.address.split("//")[1].split(":")[0]
        cmd = f"spark-class {self.cls} --host {host} --port 7077 --webui-port 8080"
        print(f"Executing\n{cmd}")
        self.proc = subprocess.Popen(shlex.split(cmd))
        print("Launched Spark Master")

    def close(self):
        self.proc.terminate()
        self.proc.wait()
        return super().close()


class SparkConnect(SchedulerPlugin):
    name = "spark-connect"
    cls = "org.apache.spark.sql.connect.service.SparkConnectServer"

    def start(self, scheduler):
        print("Starting SparkConnect")
        self.scheduler = scheduler
        self.scheduler.add_plugin(self)

        path = pathlib.Path(pyspark.__file__).absolute()
        module_loc = path.parent
        os.environ["SPARK_HOME"] = str(module_loc)
        os.environ["PYSPARK_PYTHON"] = sys.executable

        host = scheduler.address.split("//")[1].split(":")[0]
        spark_master = f"{host}:7077"
        cmd = (
            f"spark-submit --class {self.cls} "
            '--name "SparkConnectServer" '
            f"--packages org.apache.spark:spark-connect_2.12:{pyspark.__version__}"
            f",{','.join(PACKAGES)} "
            f"--master spark://{spark_master} "
            f"--conf spark.driver.host={host} "
            f"--conf spark.hadoop.fs.s3a.aws.credentials.provider="
            "com.amazonaws.auth.EnvironmentVariableCredentialsProvider"
            ",org.apache.hadoop.fs.s3a.auth.IAMInstanceCredentialsProvider"
            ",com.amazonaws.auth.profile.ProfileCredentialsProvider "
        )
        print(f"Executing\n{cmd}")
        self.proc = subprocess.Popen(shlex.split(cmd))

    def close(self):
        self.proc.terminate()
        self.proc.wait()
        return super().close()


class SparkWorker(WorkerPlugin):
    name = "spark-worker"
    cls = "org.apache.spark.deploy.worker.Worker"

    def setup(self, worker):
        self.worker = worker

        path = pathlib.Path(pyspark.__file__).absolute()
        module_loc = path.parent
        os.environ["SPARK_HOME"] = str(module_loc)
        os.environ["PYSPARK_PYTHON"] = sys.executable

        host = worker.scheduler.address.split("//")[1].split(":")[0]
        spark_master = f"spark://{host}:7077"
        print(f"Launching Spark Worker connecting to {spark_master}")
        cmd = (
            f"spark-class {self.cls} {spark_master} "
            f"--cores {self.worker.state.nthreads} "
            f"--memory {self.worker.memory_manager.memory_limit // 2**30}G "
        )
        self.proc = subprocess.Popen(shlex.split(cmd))
        print("Launched Spark Worker")

    def close(self):
        self.proc.terminate()
        self.proc.wait()
        return super().close()


PACKAGES = (
    f"org.apache.hadoop:hadoop-client:{HADOOP_AWS_VERSION}",
    f"org.apache.hadoop:hadoop-common:{HADOOP_AWS_VERSION}",
    f"org.apache.hadoop:hadoop-aws:{HADOOP_AWS_VERSION}",
    f"com.amazonaws:aws-java-sdk-bundle:{AWS_JAVA_SDK_BUNDLE_VERSION}",
)


def get_spark(client: Client, name="Coiled") -> SparkSession:
    """Launch Spark on a Dask Client

    This returns a ``spark`` session instance connected via SparkConnect
    """
    from coiled.spark import SparkConnect, SparkMaster, SparkWorker

    host = client.scheduler.address.split("//")[1].split(":")[0]
    port = 15002

    if client.scheduler.address.startswith("tls://"):
        warnings.warn(
            "Spark Connect session is neither enrypted nor secured. " f"This operates in the open on {host}:{port}"
        )

    client.register_plugin(SparkMaster(), idempotent=True)
    client.register_plugin(SparkWorker(), idempotent=True)
    client.register_plugin(SparkConnect(), idempotent=True)

    spark = (
        SparkSession.builder.remote(f"sc://{host}:{port}")  # TODO: security?
        .appName(name)
        .getOrCreate()
    )
    return spark


def get_spark_cluster(*args, **kwargs):
    cluster = Cluster(
        *args,
        **kwargs,
        backend_options={
            "ingress": [
                {"ports": [443, 8786, 8787, 7077, 8080, 4040, 15002], "cidr": "0.0.0.0/0"},
            ],
        },
    )
    return cluster
