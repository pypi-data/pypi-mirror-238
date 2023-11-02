import { getAuthTypeFromCluster } from '../AuthTypeUtil';
import { ClusterRowType } from '../../constants/types';

type GetMockCluster = {
  kdcAdminPassword?: string;
  type?: string;
};

const getMockCluster = ({ kdcAdminPassword, type }: GetMockCluster) =>
  ({
    kerberosAttributes: {
      kdcAdminPassword,
    },
    configurations: [
      {
        properties: { livyServerAuthType: type },
      },
    ],
  } as unknown as ClusterRowType);

describe('AuthType Util', () => {
  it('should return "Kerberos" for a cluster with kerberos admin password', () => {
    const authTypeFromCluster = getAuthTypeFromCluster(getMockCluster({ kdcAdminPassword: '********' }));
    expect(authTypeFromCluster).toEqual('Kerberos');
  });

  it('should return "Basic_Access" for a ldap type clusters', () => {
    const authTypeFromCluster = getAuthTypeFromCluster(getMockCluster({ type: 'ldap' }));
    expect(authTypeFromCluster).toEqual('Basic_Access');
  });

  it('should return null for none Kerberos or ldap clusters', () => {
    const authTypeFromCluster = getAuthTypeFromCluster(getMockCluster({}));
    expect(authTypeFromCluster).toBeNull();
  });
});
