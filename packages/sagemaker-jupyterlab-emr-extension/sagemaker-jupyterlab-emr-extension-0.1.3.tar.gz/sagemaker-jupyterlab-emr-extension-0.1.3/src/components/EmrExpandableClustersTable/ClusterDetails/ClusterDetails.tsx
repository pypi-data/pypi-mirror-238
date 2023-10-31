import React, { useEffect, useState } from 'react';
import { cx } from '@emotion/css';
import { i18nStrings } from '../../../constants/i18n';
import { ClusterTags } from './ClusterTags';
import { Cluster, ListInstanceGroupsOutput } from '../../../constants/types';
import {
  generateMasterNodesStringFromInstanceGroupData,
  generateApplicationsStringFromClusterData,
  generateCoreNodesStringFromInstanceGroupData,
} from '../../../utils/ClusterDetailUtils';
import { ClusterApplicationLinks } from '../ClusterApplicationLinks/ClusterApplicationLinks';
import * as styles from './styles';
import { OPTIONS_TYPE, fetchApiResponse } from '../../../service/fetchApiWrapper';
import { LIST_INSTANCE_GROUPS } from '../../../service';

interface Props {
  selectedClusterId: string;
  accountId: string;
  clusterArn: string;
  clusterData: Cluster | undefined;
  instanceGroupData?: ListInstanceGroupsOutput | undefined;
}

const expandClusterStrings = i18nStrings.Clusters.expandCluster;

const ClusterDetails: React.FunctionComponent<Props> = ({ clusterArn, accountId, selectedClusterId, clusterData }) => {
  const cluster = clusterData;
  const [instanceGroupsData, setInstanceGroupsData] = useState<any>();

  const getListInstanceGroups = async (selectedClusterId: string | undefined) => {
    const params = JSON.stringify({
      ClusterId: selectedClusterId,
    });
    const data = await fetchApiResponse(LIST_INSTANCE_GROUPS, OPTIONS_TYPE.POST, params);
    setInstanceGroupsData(data);
  };

  useEffect(() => {
    getListInstanceGroups(selectedClusterId);
  }, [selectedClusterId]);

  return (
    <div className={styles.InfoMainContainer}>
      <div className={styles.InformationContainer}>
        <h4>{expandClusterStrings.Overview}</h4>
        <div className={styles.Info}>{generateMasterNodesStringFromInstanceGroupData(instanceGroupsData)}</div>
        <div className={styles.Info}>{generateCoreNodesStringFromInstanceGroupData(instanceGroupsData)}</div>
        <div className={styles.Info}>
          {expandClusterStrings.Apps}: {generateApplicationsStringFromClusterData(cluster)}
        </div>
      </div>
      <div className={cx(styles.InformationContainer, styles.LinksContainer)}>
        <h4>{expandClusterStrings.ApplicationUserInterface}</h4>
        <ClusterApplicationLinks selectedClusterId={selectedClusterId} accountId={accountId} clusterArn={clusterArn} />
      </div>
      <div className={styles.InformationContainer}>
        <h4>{expandClusterStrings.Tags}</h4>
        <ClusterTags clusterData={clusterData} />
      </div>
    </div>
  );
};

export { ClusterDetails, Props };
