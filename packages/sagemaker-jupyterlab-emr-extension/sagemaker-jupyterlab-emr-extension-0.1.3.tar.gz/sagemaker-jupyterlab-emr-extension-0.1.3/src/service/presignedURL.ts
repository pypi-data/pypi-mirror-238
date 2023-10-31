import { OPTIONS_TYPE, fetchApiResponse } from './fetchApiWrapper';
import {
  CreatePersistentAppUIInput,
  CreatePersistentAppUIOutput,
  DescribeClusterInput,
  DescribePersistentAppUIInput,
  DescribePersistentAppUIOutput,
  GetOnClusterAppUIPresignedURLInput,
  GetOnClusterAppUIPresignedURLOutput,
  GetPersistentAppUIPresignedURLInput,
  GetPersistentAppUIPresignedURLOutput,
} from '../constants/types';
import {
  CREATE_PERSISTENT_APP_UI,
  DESCRIBE_CLUSTER_URL,
  DESCRIBE_PERSISTENT_APP_UI,
  GET_ON_CLUSTER_APP_UI_PRESIGNED_URL,
  GET_PERSISTENT_APP_UI_PRESIGNED_URL,
} from './constants';

const ON_CLUSTER_APP_UI_TYPE = 'ApplicationMaster';
const PERSISTENT_APP_UI_READY = 'ATTACHED';

const getOnClusterAppUIPresignedURL = async (
  clusterId: string,
  applicationId?: string | undefined,
): Promise<GetOnClusterAppUIPresignedURLOutput> => {
  const onClusterInput: GetOnClusterAppUIPresignedURLInput = {
    ClusterId: clusterId,
    OnClusterAppUIType: ON_CLUSTER_APP_UI_TYPE,
    ApplicationId: applicationId,
  };

  const params = JSON.stringify(onClusterInput);

  const data = await fetchApiResponse(GET_ON_CLUSTER_APP_UI_PRESIGNED_URL, OPTIONS_TYPE.POST, params);
  return data;
};

const createPersistentAppUI = async (targetResourceArn: string | undefined): Promise<CreatePersistentAppUIOutput> => {
  if (targetResourceArn === undefined) {
    throw new Error('Error describing persistent app UI: Invalid persistent app UI ID');
  }

  const createPersistentInput: CreatePersistentAppUIInput = {
    TargetResourceArn: targetResourceArn,
  };

  const params = JSON.stringify(createPersistentInput);

  const data = await fetchApiResponse(CREATE_PERSISTENT_APP_UI, OPTIONS_TYPE.POST, params);
  return data;
};

const describePersistentAppUI = async (
  persistentAppUIId: string | undefined,
): Promise<DescribePersistentAppUIOutput> => {
  if (persistentAppUIId === undefined) {
    throw new Error('Error describing persistent app UI: Invalid persistent app UI ID');
  }

  const describePersistentInput: DescribePersistentAppUIInput = {
    PersistentAppUIId: persistentAppUIId,
  };

  const params = JSON.stringify(describePersistentInput);

  const data = await fetchApiResponse(DESCRIBE_PERSISTENT_APP_UI, OPTIONS_TYPE.POST, params);
  return data;
};

const delay = async (timeout: number) => await new Promise((resolve) => setTimeout(resolve, timeout));

const pollUntilPersistentAppUIReady = async (
  persistentAppUIId: string | undefined,
  maxTimeoutMs: number,
  attemptIntervalMs: number,
): Promise<DescribePersistentAppUIOutput | undefined> => {
  const start = Date.now();
  let timeElapsed = 0;
  let result = undefined;

  while (timeElapsed <= maxTimeoutMs) {
    const queryResult = await describePersistentAppUI(persistentAppUIId);
    const status = queryResult?.persistentAppUI?.persistentAppUIStatus;
    if (status && status === PERSISTENT_APP_UI_READY) {
      result = queryResult;
      break;
    }

    await delay(attemptIntervalMs);
    timeElapsed = Date.now() - start;
  }

  if (result == null) {
    throw new Error('Error waiting for persistent app UI ready: Max attempts reached');
  }
  return result;
};

const getPersistentAppUIPresignedURL = async (
  persistentAppUIId: string | undefined,
  persistentAppUIType?: string | undefined,
  applicationId?: string | undefined,
): Promise<GetPersistentAppUIPresignedURLOutput> => {
  if (persistentAppUIId === undefined) {
    throw new Error('Error getting persistent app UI presigned URL: Invalid persistent app UI ID');
  }

  const getPersistentAppUIPresignedURLInput: GetPersistentAppUIPresignedURLInput = {
    PersistentAppUIId: persistentAppUIId,
    PersistentAppUIType: persistentAppUIType,
  };

  const params = JSON.stringify(getPersistentAppUIPresignedURLInput);

  const data = await fetchApiResponse(GET_PERSISTENT_APP_UI_PRESIGNED_URL, OPTIONS_TYPE.POST, params);
  return data;
};

const describeCluster = async (clusterId: string) => {
  const describeClusterInput: DescribeClusterInput = {
    ClusterId: clusterId,
  };

  const params = JSON.stringify(describeClusterInput);

  const data = await fetchApiResponse(DESCRIBE_CLUSTER_URL, OPTIONS_TYPE.POST, params);
  return data;
};

export {
  getOnClusterAppUIPresignedURL,
  createPersistentAppUI,
  describePersistentAppUI,
  pollUntilPersistentAppUIReady,
  getPersistentAppUIPresignedURL,
  describeCluster,
};
