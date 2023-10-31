from sagemaker_jupyterlab_emr_extension.schema.api_schema import (
    ClusterStateEnum,
    PersistentAppUiType,
)


def convertDescribeClusterResponse(describe_cluster_response: {}):
    cluster = describe_cluster_response.get("Cluster")
    if not cluster:
        return {"errorMessage": "Cluster is undefined"}
    else:
        return {
            "cluster": {
                "clusterArn": cluster.get("ClusterArn"),
                "id": cluster.get("Id"),
                "name": cluster.get("Name"),
                "autoTerminate": cluster.get("AutoTerminate", None),
                "masterPublicDnsName": cluster.get("MasterPublicDnsName", None),
                "normalizedInstanceHours": cluster.get("NormalizedInstanceHours", None),
                "outpostArn": cluster.get("OutpostArn", None),
                "securityConfiguration": cluster.get("SecurityConfiguration", None),
                "terminationProtected": cluster.get("TerminationProtected", None),
                "releaseLabel": cluster.get("ReleaseLabel", None),
                "crossAccountArn": None,
                "applications": convertApplications(cluster.get("Applications", [])),
                "configurations": convertConfigurations(
                    cluster.get("Configurations", [])
                ),
                "kerberosAttributes": convertKerberosAttributes(
                    cluster.get("KerberosAttributes", None)
                ),
                "status": convertClusterStatus(cluster.get("Status")),
                "tags": convertTags(cluster.get("Tags", [])),
            }
        }


def convertApplications(applications=[]):
    app_list = []
    for app in applications:
        application = {
            "name": app.get("Name"),
            "version": app.get("Version"),
            "args": app.get("Args"),
        }
        app_list.append(application)
    return app_list


def convertConfigurations(configurations=[]):
    configuration_list = []
    for config in configurations:
        if (
            config.get("Properties")
            and config.get("Properties") == "livy.server.auth.type"
        ):
            configuration = {
                "classification": config.get("Classificationtion", None),
                "properties": {
                    "livyServerAuthType": config.get("Properties").get(
                        "livy.server.auth.type"
                    ),
                },
            }
            configuration_list.append(configuration)
    return configuration_list


def convertKerberosAttributes(attributes={}):
    if not attributes:
        return None
    else:
        return {
            "aDDomainJoinPassword": attributes.get("ADDomainJoinPassword"),
            "aDDomainJoinUser": attributes.get("ADDomainJoinUser"),
            "crossRealmTrustPrincipalPassword": attributes.get(
                "CrossRealmTrustPrincipalPassword"
            ),
            "kdcAdminPassword": attributes.get("KdcAdminPassword"),
            "realm": attributes.get("Realm"),
        }


def convertClusterStatus(status=None):
    if status is None:
        return {
            "state": ClusterStateEnum.UNDEFINED,
        }
    if status.get("Timeline") is not None:
        timeline = convertClusterTimeline(status.get("Timeline"))
    return {"state": status.get("State"), "timeline": timeline}


def convertClusterTimeline(timeline=None):
    if not timeline.get("CreationDateTime"):
        return {
            "creationDateTime": None,
        }
    else:
        return {"creationDateTime": timeline.get("CreationDateTime").isoformat()}


def convertTags(tags=[]):
    tag_list = []
    for tag in tags:
        ctag = {"key": tag.get("Key"), "value": tag.get("Value")}
        tag_list.append(ctag)
    return tag_list


def convertListClustersResponse(list_cluster_response: {}):
    clusters_list = []
    clusters = list_cluster_response.get("Clusters", [])
    marker = list_cluster_response.get("Marker")
    if not clusters:
        return clusters_list
    else:
        for cluster in clusters:
            clusters_list.append(convertCluster(cluster))
    return {"clusters": clusters_list, "Marker": marker}


def convertCluster(cluster={}):
    converted_cluster = {
        "id": cluster.get("Id"),
        "clusterArn": cluster.get("ClusterArn"),
        "name": cluster.get("Name"),
        "status": convertClusterStatus(cluster.get("Status")),
    }
    if cluster.get("NormalizedInstanceHours"):
        converted_cluster["normalizedInstanceHours"] = cluster.get(
            "NormalizedInstanceHours"
        )

    if cluster.get("OutpostArn"):
        converted_cluster["outpostArn"] = cluster.get("OutpostArn")

    return converted_cluster


def convertPersistentAppUIResponse(response={}):
    persistentAppUI = response.get("PersistentAppUI")
    if not persistentAppUI:
        return {"persistentAppUI": None}
    converted = {
        "persistentAppUIId": persistentAppUI.get("PersistentAppUIId"),
        "persistentAppUITypeList": convertPersistentAppUITypeList(
            persistentAppUI.get("PersistentAppUITypeList")
        ),
        "persistentAppUIStatus": persistentAppUI.get("PersistentAppUIStatus"),
        "creationTime": persistentAppUI.get("CreationTime")
        if persistentAppUI.get("CreationTime") is not None
        else None,
        "lastModifiedTime": persistentAppUI.get("LastModifiedTime")
        if persistentAppUI.get("LastModifiedTime") is not None
        else None,
        "lastStateChangeReason": persistentAppUI.get("LastStateChangeReason"),
        "tags": persistentAppUI.get("Tags"),
    }
    return {"persistentAppUI": converted}


def convertPersistentAppUITypeList(PersistentAppUITypeList):
    persistentUiTypeList = []
    if not PersistentAppUITypeList:
        return persistentUiTypeList
    persistentUiTypeList.extend(PersistentAppUITypeList)
    return persistentUiTypeList


def convertInstanceGroupsResponse(response={}):
    instanceGroups = response.get("InstanceGroups", [])
    marker = response.get("Marker")
    converted_instance_groups = []
    for instance in instanceGroups:
        converted_instance = {
            "id": instance.get("Id"),
            "name": instance.get("Name"),
            "instanceType": instance.get("InstanceType"),
            "instanceGroupType": instance.get("InstanceGroupType"),
            "requestedInstanceCount": instance.get("RequestedInstanceCount"),
            "runningInstanceCount": instance.get("RunningInstanceCount"),
        }
        converted_instance_groups.append(converted_instance)
    return {"instanceGroups": converted_instance_groups, "Marker": marker}
