import os
import logging
import traceback
import botocore


from sagemaker_jupyterlab_extension_common.clients import (
    BaseAysncBoto3Client,
    get_region_name,
    get_partition,
)
from traitlets.config import SingletonConfigurable


class PrivateEMRAsyncBoto3Client(BaseAysncBoto3Client, SingletonConfigurable):
    def _create_emrprivate_client(self):
        create_client_args = {
            "service_name": "emrprivate",
            "config": self.cfg,
            "region_name": self.region_name,
        }
        return self.sess.create_client(**create_client_args)

    async def get_on_cluster_app_ui_presigned_url(self, **kwargs):
        try:
            cluster_Id = kwargs.get("ClusterId")
            if not cluster_Id:
                raise ValueError("Required argument ClusterId is invalid or missing")
            async with self._create_emrprivate_client() as emrprivate:
                response = await emrprivate.get_on_cluster_app_ui_presigned_url(
                    **kwargs
                )
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as error:
            logging.error(
                "Error getting OnCluster app ui presigned url cluster_Id {}, {}".format(
                    cluster_Id,
                    traceback.format_exc(),
                )
            )
            raise error
        except ValueError as e:
            logging.error("Invalid argument:" + str(e))
            raise e
        except Exception as ex:
            logging.error(
                "Error getting OnCluster app ui presigned url cluster_Id {} {}".format(
                    cluster_Id, traceback.format_exc()
                )
            )
            raise ex
        return response

    async def create_persistent_app_ui(self, **kwargs):
        try:
            target_resource_arn = kwargs.get("TargetResourceArn")
            if not target_resource_arn:
                raise ValueError(
                    "Required argument TargetResourceArn is invalid or missing"
                )
            async with self._create_emrprivate_client() as emrprivate:
                response = await emrprivate.create_persistent_app_ui(**kwargs)
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as error:
            logging.error(
                "Error creating persistent app UI {} EMR clusters {}".format(
                    target_resource_arn, traceback.format_exc()
                )
            )
            raise error
        except ValueError as e:
            logging.error("Invalid argument:" + str(e))
            raise e
        except Exception as ex:
            logging.error(
                "Error creating persistent app UI for arn {} {}".format(
                    target_resource_arn, traceback.format_exc()
                )
            )
            raise ex
        return response

    async def describe_persistent_app_ui(self, **kwargs):
        try:
            persistent_app_ui_id = kwargs.get("PersistentAppUIId")
            if not persistent_app_ui_id:
                raise ValueError(
                    "Required argument PersistentAppUIId is invalid or missing"
                )
            async with self._create_emrprivate_client() as emrprivate:
                response = await emrprivate.describe_persistent_app_ui(**kwargs)
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as error:
            logging.error(
                "Error describing persistent app UI for Id {}. {}".format(
                    persistent_app_ui_id, traceback.format_exc()
                )
            )
            raise error
        except ValueError as e:
            logging.error("Invalid argument:" + str(e))
            raise e
        except Exception as ex:
            logging.error(
                "Error describing persistent app UI Id {} {}".format(
                    persistent_app_ui_id, traceback.format_exc()
                )
            )
            raise ex
        return response

    async def get_persistent_app_ui_presigned_url(self, **kwargs):
        try:
            persistent_app_ui_id = kwargs.get("PersistentAppUIId")
            if not persistent_app_ui_id:
                raise ValueError(
                    "Required argument PersistentAppUIId is invalid or missing"
                )
            async with self._create_emrprivate_client() as emrprivate:
                response = await emrprivate.get_persistent_app_ui_presigned_url(
                    **kwargs
                )
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as error:
            logging.error(
                "Error getting persistent app ui presigned url {} {}".format(
                    persistent_app_ui_id,
                    traceback.format_exc(),
                )
            )
            raise error
        except ValueError as e:
            logging.error("Invalid argument:" + str(e))
            raise e
        except Exception as ex:
            logging.error(
                "Error getting persistent app ui presigned url {} {}".format(
                    persistent_app_ui_id, traceback.format_exc()
                )
            )
            raise ex
        return response


def get_emrprivate_client(createNew=False):
    PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
    os.environ["EMR_DATA_PATH"] = os.path.join(PACKAGE_ROOT, "botocore_model")
    model_path = os.environ.get("EMR_DATA_PATH")
    if createNew:
        return PrivateEMRAsyncBoto3Client(
            get_region_name(), get_partition(), model_path
        )
    else:
        return PrivateEMRAsyncBoto3Client.instance(
            get_region_name(), get_partition(), model_path
        )


class EMRAsyncBoto3Client(BaseAysncBoto3Client, SingletonConfigurable):
    def _create_emr_client(self):
        create_client_args = {
            "service_name": "emr",
            "config": self.cfg,
            "region_name": self.region_name,
        }
        return self.sess.create_client(**create_client_args)

    async def list_clusters(self, **kwargs):
        try:
            async with self._create_emr_client() as em_client:
                response = await em_client.list_clusters(**kwargs)
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as error:
            logging.error("Error in listing clusters {}".format(traceback.format_exc()))
            raise error
        return response

    async def describe_cluster(self, **kwargs):
        try:
            cluster_Id = kwargs.get("ClusterId")
            if not cluster_Id:
                raise ValueError("Required argument ClusterId is invalid or missing")
            async with self._create_emr_client() as em_client:
                response = await em_client.describe_cluster(**kwargs)
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as error:
            logging.error(
                "Error describing cluster for Id {}. {}".format(
                    cluster_Id, traceback.format_exc()
                )
            )
            raise error
        except ValueError as e:
            logging.error("Invalid argument:" + str(e))
            raise e
        except Exception as ex:
            logging.error(
                "Error describing cluster for Id {} {}".format(
                    cluster_Id, traceback.format_exc()
                )
            )
            raise ex
        return response

    async def list_instance_groups(self, **kwargs):
        try:
            cluster_Id = kwargs.get("ClusterId")
            if not cluster_Id:
                raise ValueError("Required argument ClusterId is invalid or missing")
            async with self._create_emr_client() as em_client:
                response = await em_client.list_instance_groups(**kwargs)
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as error:
            logging.error(
                "Error listing Instance Group for Cluster Id {}. {}".format(
                    cluster_Id, traceback.format_exc()
                )
            )
            raise error
        except ValueError as e:
            logging.error("Invalid argument:" + str(e))
            raise e
        except Exception as ex:
            logging.error(
                "Error listing Instance Group for Cluster Id {} {}".format(
                    cluster_Id, traceback.format_exc()
                )
            )
            raise ex
        return response


def get_emr_client(createNew=False):
    if createNew:
        return EMRAsyncBoto3Client(get_region_name(), get_partition())
    else:
        return EMRAsyncBoto3Client.instance(get_region_name(), get_partition())
