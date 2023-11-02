const i18nStrings = {
  Clusters: {
    widgetTitle: 'Connect to cluster',
    connectCommand: {
      label: 'Connect',
      caption: 'Connect to a cluster',
    },
    connectMessage: {
      errorTitle: 'Error connecting to EMR cluster',
      successTitle: 'Successfully connected to EMR cluster',
      errorDefaultMessage: 'Error connecting to EMR cluster',
      successDefaultMessage: 'Connected to EMR Cluster',
    },
    widgetConnected: 'The notebook is connected to',
    defaultTooltip: 'Select a cluster to connect to',
    widgetHeader:
      'Select a cluster to connect to. A code block will be added to the active cell and run automatically to establish the connection.',
    connectedWidgetHeader: 'cluster. You can submit new jobs to run on the cluster.',
    connectButton: 'Connect',
    learnMore: 'Learn more',
    noResultsMatchingFilters: 'There are no clusters matching the filter.',
    radioButtonLabels: {
      basicAccess: 'Http basic authentication',
      noCredential: 'No credential',
    },
    listClusterError: 'Fail to list clusters, refresh the modal or try again later',
    noCluster: 'No clusters are available',
    selectAuthTitle: 'Select credential type for ',
    clusterButtonLabel: 'Cluster',
    expandCluster: {
      MasterNodes: 'Master nodes',
      CoreNodes: 'Core nodes',
      NotAvailable: 'Not available',
      NoTags: 'No tags',
      SparkHistoryServer: 'Spark History Server',
      TezUI: 'Tez UI',
      Overview: 'Overview',
      Apps: 'Apps',
      ApplicationUserInterface: 'Application user Interface',
      Tags: 'Tags',
    },
    presignedURL: {
      link: 'Link',
      error: 'Error: ',
      retry: 'Retry',
      sparkUIError: 'Spark UI Link is not available or time out. Please try ',
      sshTunnelLink: 'SSH tunnel',
      or: ' or ',
      viewTheGuide: 'view the guide',
      clusterNotReady: 'Cluster is not ready. Please try again later.',
      clusterNotConnected: 'No active cluster connection. Please connect to a cluster and try again.',
      clusterNotCompatible:
        'EMR version 5.33+ or 6.3.0+ required for direct Spark UI links. Try a compatible cluster, use ',
    },
  },
  DefaultModal: {
    CancelButton: 'Cancel',
    SubmitButton: 'Submit',
  },
  TableLabels: {
    name: 'Name',
    id: 'ID',
    status: 'Status',
    creationTime: 'Creation Time',
    createdOn: 'Created On',
    accountId: 'Account ID',
  },
};

export { i18nStrings };
