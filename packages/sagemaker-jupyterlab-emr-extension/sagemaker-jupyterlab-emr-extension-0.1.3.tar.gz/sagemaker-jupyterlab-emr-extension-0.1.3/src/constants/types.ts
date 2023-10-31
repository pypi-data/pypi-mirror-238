import { ISessionContext } from '@jupyterlab/apputils/lib/sessioncontext';
import { NotebookPanel } from '@jupyterlab/notebook/lib/panel';

export type Application = {
  args?: string[];
  name?: string;
  version?: string;
};

export type Cluster = {
  applications?: Application[];
  autoTerminate?: boolean;
  clusterArn?: string;
  configurations?: ClusterConfiguration[];
  crossAccountArn?: string;
  id?: string;
  kerberosAttributes?: KerberosAttributes;
  logUri?: string;
  masterPublicDnsName?: string;
  name?: string;
  normalizedInstanceHours?: number;
  outpostArn?: string;
  releaseLabel?: string;
  securityConfiguration?: string;
  status: ClusterStatus;
  tags?: Tag[];
  terminationProtected?: boolean;
};

export type KerberosAttributes = {
  aDDomainJoinPassword?: string;
  aDDomainJoinUser?: string;
  crossRealmTrustPrincipalPassword?: string;
  kdcAdminPassword?: string;
  realm?: string;
};

export type ClusterConfiguration = {
  classification?: string;
  properties?: ClusterConfigurationProperty;
};

export type ClusterConfigurationProperty = {
  livyServerAuthType?: string;
  livyServerPrincipal?: string;
  livyServerSecretKey?: string;
  sparkSubmitAuthType?: string;
};

export type ClusterSecurityConfiguration = {
  name?: string;
  securityConfiguration?: string;
};

export type Tag = {
  key?: string;
  Key?: string;
  value?: string;
  Value?: string;
};

export type InputTag = {
  key: string;
  value: string;
};

export enum ClusterState {
  Bootstrapping = 'BOOTSTRAPPING',
  Running = 'RUNNING',
  Starting = 'STARTING',
  Terminated = 'TERMINATED',
  TerminatedWithErrors = 'TERMINATED_WITH_ERRORS',
  Terminating = 'TERMINATING',
  Undefined = 'UNDEFINED',
  Waiting = 'WAITING',
}

export enum StateChangeCode {
  AllStepsCompleted = 'All_Steps_Completed',
  BootstrapFailure = 'Bootstrap_Failure',
  InstanceFailure = 'Instance_Failure',
  InstanceFleetTimeout = 'Instance_Fleet_Timeout',
  InternalError = 'Internal_Error',
  StepFailure = 'Step_Failure',
  UserRequest = 'User_Request',
  ValidationError = 'Validation_Error',
}

export type ListClustersInput = {
  accountIds?: string[];
  clusterStates?: ClusterState[];
  createdAfter?: string;
  createdBefore?: string;
  marker?: string;
};

export type ListClustersOutput = {
  clusters: Array<ClusterSummary>;
  errorFlags?: CrossAccountErrorFlags;
  errorMessage?: string;
  validationErrorMessage?: string;
};

export type DescribeClusterInput = {
  accountId?: string;
  ClusterId: string;
};

export type DescribeClusterOutput = {
  cluster?: Cluster;
};

export type ClusterStateChangeReason = {
  code?: StateChangeCode;
  message?: string;
};

export type CrossAccountErrorFlags = {
  assumeRoleError?: boolean;
  assumeRoleTimeout?: boolean;
  assumeRoleUnauthorizedAccess?: boolean;
  assumeRoleUnknownError?: boolean;
  configError?: boolean;
};

export type ClusterStatus = {
  state?: ClusterState;
  stateChangeReason?: string;
  timeline?: ClusterTimeline;
};

export type ClusterSummary = {
  clusterArn?: string;
  id?: string;
  name?: string;
  normalizedInstanceHours?: number;
  outpostArn?: string;
  status: ClusterStatus;
};

export type ClusterTimeline = {
  creationDateTime?: string;
  endDateTime?: string;
  readyDateTime?: string;
};

// For all attributes see https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceGroup.html
export type InstanceGroup = {
  id: string;
  instanceGroupType: string;
  instanceType: string;
  name: string;
  requestedInstanceCount: number;
  runningInstanceCount: number;
};

export type ListInstanceGroupsInput = {
  clusterId: string;
  accountId: string;
};

export type ListInstanceGroupsOutput = {
  instanceGroups: [InstanceGroup];
};

export type DescribeSecurityConfigurationInput = {
  name: string;
  accountId: string;
};

export type DescribeSecurityConfigurationOutput = {
  name: string;
  securityConfiguration: string;
};

export type EMRContainersConfig = {
  jobRunId: string;
};

export enum PersistentAppUIType {
  SHS,
  TEZUI,
  YTS,
}

export type PersistentAppUI = {
  persistentAppUIId: string;
  persistentAppUITypeList: [PersistentAppUIType];
  persistentAppUIStatus: string;
  creationTime: string;
  lastModifiedTime: string;
  lastStateChangeReason: string;
  tags: [Tag];
};

export type CreatePersistentAppUIInput = {
  TargetResourceArn: string | undefined;
  EmrContainersConfig?: EMRContainersConfig;
  Tags?: [InputTag];
  xReferer?: string;
  AccountId?: string;
};

export type CreatePersistentAppUIOutput = {
  [x: string]: any;
  persistentAppUIId: string;
};

export type GetOnClusterAppUIPresignedURLInput = {
  ClusterId: string;
  OnClusterAppUIType: string;
  ApplicationId?: string | undefined;
  accountId?: string | undefined;
};

export type GetOnClusterAppUIPresignedURLOutput = {
  [x: string]: any;
  presignedURLReady: boolean;
  presignedURL: string;
};

export type GetPersistentAppUIPresignedURLInput = {
  PersistentAppUIId: string;
  PersistentAppUIType: string | undefined;
  ApplicationId?: string | undefined;
  accountId?: string;
};

export type GetPersistentAppUIPresignedURLOutput = {
  [x: string]: any;
  presignedURLReady: boolean;
  presignedURL: string;
};

export type DescribePersistentAppUIInput = {
  PersistentAppUIId: string;
  AccountId?: string;
};

export type DescribePersistentAppUIOutput = {
  [x: string]: any;
  persistentAppUI: PersistentAppUI;
  errorMessage: string;
};

export interface ResourceBaseType {
  readonly id: string;
}
export interface ClusterRowType extends Omit<Cluster, 'id'>, ResourceBaseType {}

export type HandleConnectType = (
  disposeDialog: () => void,
  selectedCluster: ClusterRowType | undefined,
  type?: AuthType,
  sessionContext?: ISessionContext,
  notebookPanel?: NotebookPanel,
) => () => void;

export type AuthType = 'Kerberos' | 'None' | 'Basic_Access';

export enum NotificationStatus {
  Success = 'Success',
  Fail = 'Fail',
}

export enum LinkType {
  Content,
  External,
  Notebook,
}

export type ShowNotificationHandlerType = (status?: NotificationStatus, notificationBody?: React.ReactNode) => void;
