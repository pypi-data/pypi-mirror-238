from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_deployment_configmap_existence(Check):
    def _execute(self, deployment, configmaps, report) -> bool:
        configmap_names = [
            (configmap.metadata.name, configmap.metadata.namespace)
            for configmap in configmaps
        ]
        deploymentNamespace = deployment.metadata.namespace
        deploymentName = deployment.metadata.name

        if deployment.spec.template.spec.volumes:
            for volume in deployment.spec.template.spec.volumes:
                if volume.config_map is not None:
                    configmapName = volume.config_map.name

                    configmapMatchFound = False

                    for configmap_name, configmap_namespace in configmap_names:
                        if (
                            configmap_name == configmapName
                            and configmap_namespace == deploymentNamespace
                        ):
                            configmapMatchFound = True
                            break

                    if configmapMatchFound == False:
                        report.status_extended = f"ConfigMap name {volume.config_map.name} in Deployment namespace {deployment.metadata.namespace} does not exist in the list of ConfigMaps."
                        report.resource_id = deploymentName
                        report.resource_configmap = configmapName
                        return False
        return True

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        configmaps = data.get_configmaps()
        for deployment in data.get_deployments():
            report = Check_Report_K8S(self.metadata())
            report.resource_namespace = deployment.metadata.namespace
            report.resource_name = deployment.metadata.name
            report.status = "PASS"

            if not self._execute(deployment, configmaps, report):
                report.status = "FAIL"

            findings.append(report)

        return findings
