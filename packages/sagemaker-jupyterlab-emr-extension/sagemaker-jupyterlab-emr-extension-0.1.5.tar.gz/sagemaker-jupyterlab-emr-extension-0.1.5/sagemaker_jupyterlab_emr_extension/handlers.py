import json
import asyncio
import traceback
import jsonschema
import botocore

from tornado import web
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join
from jsonschema.exceptions import ValidationError

from ._version import __version__ as ext_version
from sagemaker_jupyterlab_extension_common.logging.logging_utils import HandlerLogMixin

from sagemaker_jupyterlab_emr_extension.clients import (
    get_emr_client,
    get_emrprivate_client,
)
from sagemaker_jupyterlab_emr_extension.schema.api_schema import (
    describe_cluster_request_schema,
    list_cluster_request_schema,
    create_presistent_app_ui_schema,
    describe_persistent_app_ui_schema,
    get_persistent_app_ui_presigned_url_schema,
    get_on_cluster_app_ui_presigned_url_schema,
    list_instance_groups_schema,
)
from sagemaker_jupyterlab_emr_extension.converters import (
    convertDescribeClusterResponse,
    convertListClustersResponse,
    convertPersistentAppUIResponse,
    convertInstanceGroupsResponse,
)
from sagemaker_jupyterlab_emr_extension.utils.logging_utils import (
    EmrErrorHandler,
)

EXTENSION_NAME = "sagemaker_jupyterlab_emr_extension"
EXTENSION_VERSION = ext_version

from sagemaker_jupyterlab_extension_common.logging.logging_utils import HandlerLogMixin


class DescribeClusterHandler(HandlerLogMixin, JupyterHandler):
    # Do not rename or change the variable names, these are used by
    # loggers in common package.
    jl_extension_name = EXTENSION_NAME
    jl_extension_version = EXTENSION_VERSION

    """
    Response schema
    {
        cluster: Cluster
        errorMessage: String
    }
    """

    @web.authenticated
    async def post(self):
        try:
            body = self.get_json_body()
            jsonschema.validate(body, describe_cluster_request_schema)
            cluster_id = body["ClusterId"]
            self.log.info(f"Describe cluster request {cluster_id}")
            response = await get_emr_client().describe_cluster(**body)
            self.log.info(f"Successfuly described cluster for id {cluster_id}")
            converted_resp = convertDescribeClusterResponse(response)
            self.set_status(200)
            self.finish(json.dumps(converted_resp))
        except (
            botocore.exceptions.ParamValidationError,
            ValidationError,
        ) as error:
            self.log.error("Invalid request {} {}".format(body, traceback.format_exc()))
            self.set_status(400)
            self.finish(
                json.dumps({"errorMessage": "Invalid request missing or wrong input"})
            )
        except botocore.exceptions.ClientError as error:
            self.log.error("SdkClientError {}".format(traceback.format_exc()))
            msg = EmrErrorHandler.get_boto_error(error)
            self.set_status(msg.get("http_code"))
            self.finish(json.dumps(msg.get("message")))
        except Exception as error:
            self.log.error("Internal Service Error: {}".format(traceback.format_exc()))
            self.set_status(500)
            self.finish(json.dumps({"errorMessage": str(error)}))


class ListClustersHandler(HandlerLogMixin, JupyterHandler):
    # Do not rename or change the variable names, these are used by
    # loggers in common package.
    jl_extension_name = EXTENSION_NAME
    jl_extension_version = EXTENSION_VERSION

    """
    Response schema
    {
        clusters: [ClusterSummary]!
        errorMessage: String
    }
    """

    @web.authenticated
    async def post(self):
        try:
            body = self.get_json_body()
            jsonschema.validate(body, list_cluster_request_schema)
            self.log.info(f"List clusters request {body}")
            response = await get_emr_client().list_clusters(**body)
            converted_resp = convertListClustersResponse(response)
            self.set_status(200)
            self.finish(json.dumps(converted_resp))
        except (
            botocore.exceptions.ParamValidationError,
            jsonschema.exceptions.ValidationError,
        ) as error:
            self.log.error("Invalid request {} {}".format(body, traceback.format_exc()))
            self.set_status(400)
            self.finish(
                json.dumps({"ErrorMessage": "Invalid request missing or wrong input"})
            )
        except botocore.exceptions.ClientError as error:
            self.log.error("SdkClientError {}".format(traceback.format_exc()))
            msg = EmrErrorHandler.get_boto_error(error)
            self.set_status(msg.get("http_code"))
            self.finish(json.dumps(msg.get("message")))
        except Exception as error:
            self.log.error("Internal Service Error: {}".format(traceback.format_exc()))
            self.set_status(500)
            self.finish(json.dumps({"error": str(error)}))


class ListInstanceGroupsHandler(HandlerLogMixin, JupyterHandler):
    # Do not rename or change the variable names, these are used by
    # loggers in common package.
    jl_extension_name = EXTENSION_NAME
    jl_extension_version = EXTENSION_VERSION

    """
    Response schema

    InstanceGroup = {
        id: String;
        instanceGroupType: String;
        instanceType: String;
        name: String;
        requestedInstanceCount: Int;
        runningInstanceCount: Int;
    }

    {
        instanceGroups: InstanceGroup
    }
    """

    @web.authenticated
    async def post(self):
        try:
            body = self.get_json_body()
            jsonschema.validate(body, list_instance_groups_schema)
            cluster_id = body["ClusterId"]
            self.log.info(f"ListInstanceGroups for cluster {cluster_id}")
            response = await get_emr_client().list_instance_groups(**body)
            self.log.info(
                f"Successfuly listed instance groups for cluster {cluster_id}"
            )
            converted_resp = convertInstanceGroupsResponse(response)
            self.set_status(200)
            self.finish(json.dumps(converted_resp))
        except (
            botocore.exceptions.ParamValidationError,
            ValidationError,
        ) as error:
            self.log.error("Invalid request {} {}".format(body, traceback.format_exc()))
            self.set_status(400)
            self.finish(
                json.dumps({"errorMessage": "Invalid request missing or wrong input"})
            )
        except botocore.exceptions.ClientError as error:
            self.log.error("SdkClientError {}".format(traceback.format_exc()))
            msg = EmrErrorHandler.get_boto_error(error)
            self.set_status(msg.get("http_code"))
            self.finish(json.dumps(msg.get("message")))
        except Exception as error:
            self.log.error("Internal Service Error: {}".format(traceback.format_exc()))
            self.set_status(500)
            self.finish(json.dumps({"errorMessage": str(error)}))


class CreatePersistentAppUiHandler(HandlerLogMixin, JupyterHandler):
    # Do not rename or change the variable names, these are used by
    # loggers in common package.
    jl_extension_name = EXTENSION_NAME
    jl_extension_version = EXTENSION_VERSION

    """
    Response schema
    {
        persistentAppUIId: String
    }
    """

    @web.authenticated
    async def post(self):
        try:
            body = self.get_json_body()
            jsonschema.validate(body, create_presistent_app_ui_schema)
            target_resource_arn = body.get("TargetResourceArn")
            self.log.info(f"Create Persistent App UI for Arn {target_resource_arn}")
            response = await get_emrprivate_client().create_persistent_app_ui(**body)
            persistent_app_ui_id = response.get("PersistentAppUIId")
            self.log.info(
                f"Successfully cretaed Persistent App UI withId {persistent_app_ui_id}"
            )
            converted_resp = {"persistentAppUIId": persistent_app_ui_id}
            self.set_status(200)
            self.finish(json.dumps(converted_resp))
        except (
            botocore.exceptions.ParamValidationError,
            jsonschema.exceptions.ValidationError,
        ) as error:
            self.log.error("Invalid request {} {}".format(body, traceback.format_exc()))
            self.set_status(400)
            self.finish(
                json.dumps({"ErrorMessage": "Invalid request missing or wrong input"})
            )
        except botocore.exceptions.ClientError as error:
            self.log.error("SdkClientError {}".format(traceback.format_exc()))
            msg = EmrErrorHandler.get_boto_error(error)
            self.set_status(msg.get("http_code"))
            self.finish(json.dumps(msg.get("message")))
        except Exception as error:
            self.log.error("Internal Service Error: {}".format(traceback.format_exc()))
            self.set_status(500)
            self.finish(json.dumps({"error": str(error)}))


class DescribePersistentAppUiHandler(HandlerLogMixin, JupyterHandler):
    # Do not rename or change the variable names, these are used by
    # loggers in common package.
    jl_extension_name = EXTENSION_NAME
    jl_extension_version = EXTENSION_VERSION

    """
    Response schema
    {
        persistentAppUI: PersistentAppUI
        errorMessage: String
    }
    """

    @web.authenticated
    async def post(self):
        try:
            body = self.get_json_body()
            jsonschema.validate(body, describe_persistent_app_ui_schema)
            persistent_app_ui_id = body.get("PersistentAppUIId")
            self.log.info(f"DescribePersistentAppUi for Id {persistent_app_ui_id}")
            response = await get_emrprivate_client().describe_persistent_app_ui(**body)
            converted_resp = convertPersistentAppUIResponse(response)
            self.set_status(200)
            self.finish(json.dumps(converted_resp))
        except (
            botocore.exceptions.ParamValidationError,
            jsonschema.exceptions.ValidationError,
        ) as error:
            self.log.error("Invalid request {} {}".format(body, traceback.format_exc()))
            self.set_status(400)
            self.finish(
                json.dumps({"errorMessage": "Invalid request missing or wrong input"})
            )
        except botocore.exceptions.ClientError as error:
            self.log.error("SdkClientError {}".format(traceback.format_exc()))
            msg = EmrErrorHandler.get_boto_error(error)
            self.set_status(msg.get("http_code"))
            self.finish(json.dumps(msg.get("message")))
        except Exception as error:
            self.log.error("Internal Service Error: {}".format(traceback.format_exc()))
            self.set_status(500)
            self.finish(json.dumps({"error": str(error)}))


class GetPersistentAppUiPresignedUrlHandler(HandlerLogMixin, JupyterHandler):
    # Do not rename or change the variable names, these are used by
    # loggers in common package.
    jl_extension_name = EXTENSION_NAME
    jl_extension_version = EXTENSION_VERSION

    """
    Response schema
    {
        presignedURLReady: Boolean
        presignedURL: String
    }
    """

    @web.authenticated
    async def post(self):
        try:
            body = self.get_json_body()
            jsonschema.validate(body, get_persistent_app_ui_presigned_url_schema)
            persistent_app_ui_id = body["PersistentAppUIId"]
            self.log.info(f"Get Persistent App UI for {persistent_app_ui_id}")
            response = (
                await get_emrprivate_client().get_persistent_app_ui_presigned_url(
                    **body
                )
            )
            converted_resp = {
                "presignedURLReady": response.get("PresignedURLReady"),
                "presignedURL": response.get("PresignedURL"),
            }
            self.set_status(200)
            self.finish(json.dumps(converted_resp))
        except (
            botocore.exceptions.ParamValidationError,
            jsonschema.exceptions.ValidationError,
        ) as error:
            self.log.error("Invalid request {} {}".format(body, traceback.format_exc()))
            self.set_status(400)
            self.finish(
                json.dumps({"errorMessage": "Invalid request missing or wrong input"})
            )
        except botocore.exceptions.ClientError as error:
            self.log.error("SdkClientError {}".format(traceback.format_exc()))
            msg = EmrErrorHandler.get_boto_error(error)
            self.set_status(msg.get("http_code"))
            self.finish(json.dumps(msg.get("message")))
        except Exception as error:
            self.log.error("Internal Service Error: {}".format(traceback.format_exc()))
            self.set_status(500)
            self.finish(json.dumps({"error": str(error)}))


class GetOnClustersAppUiPresignedUrlHandler(HandlerLogMixin, JupyterHandler):
    # Do not rename or change the variable names, these are used by
    # loggers in common package.
    jl_extension_name = EXTENSION_NAME
    jl_extension_version = EXTENSION_VERSION

    """
    Response schema
    {
        presignedURLReady: Boolean
        presignedURL: String
    }
    """

    @web.authenticated
    async def post(self):
        try:
            body = self.get_json_body()
            jsonschema.validate(body, get_on_cluster_app_ui_presigned_url_schema)
            cluster_id = body["ClusterId"]
            self.log.info(f"GetOnClusterAppUiPresignedUrl for cluster id {cluster_id}")
            response = (
                await get_emrprivate_client().get_on_cluster_app_ui_presigned_url(
                    **body
                )
            )
            converted_resp = {
                "presignedURLReady": response.get("PresignedURLReady"),
                "presignedURL": response.get("PresignedURL"),
            }
            self.set_status(200)
            self.finish(json.dumps(converted_resp))
        except (
            botocore.exceptions.ParamValidationError,
            jsonschema.exceptions.ValidationError,
        ) as error:
            self.log.error("Invalid request {} {}".format(body, traceback.format_exc()))
            self.set_status(400)
            self.finish(
                json.dumps({"errorMessage": "Invalid request missing or wrong input"})
            )
        except botocore.exceptions.ClientError as error:
            self.log.error("SdkClientError {}".format(traceback.format_exc()))
            msg = EmrErrorHandler.get_boto_error(error)
            self.set_status(msg.get("http_code"))
            self.finish(json.dumps(msg.get("message")))
        except Exception as error:
            self.log.error("Internal Service Error: {}".format(traceback.format_exc()))
            self.set_status(500)
            self.finish(json.dumps({"error": str(error)}))


def build_url(web_app, endpoint):
    base_url = web_app.settings["base_url"]
    return url_path_join(base_url, endpoint)


def register_handlers(nbapp):
    web_app = nbapp.web_app
    host_pattern = ".*$"
    handlers = [
        (
            build_url(web_app, r"/aws/sagemaker/api/emr/describe-cluster"),
            DescribeClusterHandler,
        ),
        (
            build_url(web_app, r"/aws/sagemaker/api/emr/list-clusters"),
            ListClustersHandler,
        ),
        (
            build_url(web_app, r"/aws/sagemaker/api/emr/create-persistent-app-ui"),
            CreatePersistentAppUiHandler,
        ),
        (
            build_url(web_app, r"/aws/sagemaker/api/emr/describe-persistent-app-ui"),
            DescribePersistentAppUiHandler,
        ),
        (
            build_url(
                web_app, r"/aws/sagemaker/api/emr/get-persistent-app-ui-presigned-url"
            ),
            GetPersistentAppUiPresignedUrlHandler,
        ),
        (
            build_url(
                web_app, r"/aws/sagemaker/api/emr/get-on-cluster-app-ui-presigned-url"
            ),
            GetOnClustersAppUiPresignedUrlHandler,
        ),
        (
            build_url(web_app, r"/aws/sagemaker/api/emr/list-instance-groups"),
            ListInstanceGroupsHandler,
        ),
    ]
    web_app.add_handlers(host_pattern, handlers)
