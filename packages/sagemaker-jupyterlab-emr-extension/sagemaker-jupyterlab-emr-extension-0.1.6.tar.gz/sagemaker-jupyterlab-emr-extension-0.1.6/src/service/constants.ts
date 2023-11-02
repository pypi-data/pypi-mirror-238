/**
 * Urls
 */
const DESCRIBE_CLUSTER_URL = '/aws/sagemaker/api/emr/describe-cluster';
const LIST_CLUSTERS_URL = '/aws/sagemaker/api/emr/list-clusters';
const GET_ON_CLUSTER_APP_UI_PRESIGNED_URL = '/aws/sagemaker/api/emr/get-on-cluster-app-ui-presigned-url';
const CREATE_PERSISTENT_APP_UI = '/aws/sagemaker/api/emr/create-persistent-app-ui';
const DESCRIBE_PERSISTENT_APP_UI = '/aws/sagemaker/api/emr/describe-persistent-app-ui';
const GET_PERSISTENT_APP_UI_PRESIGNED_URL = '/aws/sagemaker/api/emr/get-persistent-app-ui-presigned-url';
const LIST_INSTANCE_GROUPS = '/aws/sagemaker/api/emr/list-instance-groups';

/**
 * API calls constants
 */
const SUCCESS_RESPONSE_STATUS = [200, 201];

export {
  DESCRIBE_CLUSTER_URL,
  LIST_CLUSTERS_URL,
  SUCCESS_RESPONSE_STATUS,
  GET_ON_CLUSTER_APP_UI_PRESIGNED_URL,
  CREATE_PERSISTENT_APP_UI,
  DESCRIBE_PERSISTENT_APP_UI,
  GET_PERSISTENT_APP_UI_PRESIGNED_URL,
  LIST_INSTANCE_GROUPS,
};
