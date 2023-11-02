import { ClusterRowType, ClusterConfiguration, AuthType } from '../constants/types';

export const getAuthTypeFromCluster = (cluster: ClusterRowType): AuthType | null => {
  if (cluster.kerberosAttributes?.kdcAdminPassword) {
    return 'Kerberos';
  } else if (
    cluster.configurations?.some((c: ClusterConfiguration | undefined) => c?.properties?.livyServerAuthType === 'ldap')
  ) {
    return 'Basic_Access';
  } else {
    return null;
  }
};
