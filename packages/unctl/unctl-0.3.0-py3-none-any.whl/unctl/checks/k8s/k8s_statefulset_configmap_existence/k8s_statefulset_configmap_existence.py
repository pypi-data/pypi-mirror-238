from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_statefulset_configmap_existence(Check):
    def _execute(self, statefulset, configmaps, report) -> bool:
        configmap_names = [
            (configmap.metadata.name, configmap.metadata.namespace)
            for configmap in configmaps
        ]

        statefulsetNamespace = statefulset.metadata.namespace
        volumes = statefulset.spec.template.spec.volumes
        volumeClaimTemplates = statefulset.spec.volume_claim_templates

        if volumeClaimTemplates is not None:
            for volumeClaimTemplate in volumeClaimTemplates:
                if not hasattr(volumeClaimTemplate.spec, "data_source"):
                    continue

                datasource = volumeClaimTemplate.spec.data_source
                if not hasattr(datasource, "name"):
                    continue

                configmap_vct = volumeClaimTemplate.spec.data_source.name
                if configmap_vct not in [
                    name
                    for (name, namespace) in configmap_names
                    if namespace == statefulsetNamespace
                ]:
                    report.status_extended = f"ConfigMap {configmap_vct} not found in namespace {statefulsetNamespace}"
                    report.resource_configmap = configmap_vct
                    return False

        if volumes is not None:
            for volume in volumes:
                if not hasattr(volume.config_map, "name"):
                    continue

                if volume.config_map.name is None:
                    continue

                configmap_vol = volume.config_map.name
                if configmap_vol not in [
                    name
                    for (name, namespace) in configmap_names
                    if namespace == statefulsetNamespace
                ]:
                    report.status_extended = f"ConfigMap {configmap_vol} not found in namespace {statefulsetNamespace}"
                    report.resource_configmap = configmap_vol
                    return False

        return True

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        configmaps = data.get_configmaps()
        for statefulset in data.get_statefulsets():
            report = Check_Report_K8S(self.metadata())
            report.resource_namespace = statefulset.metadata.namespace
            report.resource_id = statefulset.metadata.name
            report.resource_name = statefulset.metadata.name
            report.status = "PASS"

            if not self._execute(statefulset, configmaps, report):
                report.status = "FAIL"

            findings.append(report)
        return findings
