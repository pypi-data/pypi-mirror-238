from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_statefulset_storage_class_validation(Check):
    def _execute(self, statefulset, storageClasses, report) -> bool:
        statefulset_namespace = statefulset.metadata.namespace
        statefulset_name = statefulset.metadata.name

        storageClass = [s.metadata.name for s in storageClasses]

        if statefulset.spec is None or statefulset.spec.volume_claim_templates is None:
            return True

        claims_list = statefulset.spec.volume_claim_templates
        for volumeClaimTemplate in claims_list:
            storageclass_name = volumeClaimTemplate.spec.storage_class_name
            # check if its valid name
            if storageclass_name is None or storageclass_name in storageClass:
                continue

            # bailing out on the first error
            report.resource_storageclass = storageclass_name
            report.status_extended = f"StatefulSet {statefulset_name} uses non-existent storageclass {storageclass_name} in namespace {statefulset_namespace}"
            return False

        return True

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        storageClasses = data.get_storage_classes()
        for statefulset in data.get_statefulsets():
            report = Check_Report_K8S(self.metadata())
            report.resource_namespace = statefulset.metadata.namespace
            report.resource_id = statefulset.metadata.name
            report.status = "PASS"

            if not self._execute(statefulset, storageClasses, report):
                report.status = "FAIL"

            findings.append(report)

        return findings
