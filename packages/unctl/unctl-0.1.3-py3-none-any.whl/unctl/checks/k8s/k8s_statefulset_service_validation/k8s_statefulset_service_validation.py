from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_statefulset_service_validation(Check):
    def _execute(self, statefulset, services, report) -> bool:
        statefulset_serviceName = statefulset.spec.service_name
        statefulset_namespace = statefulset.metadata.namespace
        statefulset_name = statefulset.metadata.name

        serviceInfo = [(s.metadata.name, s.metadata.namespace) for s in services]
        match_found = False

        for name, namespace in serviceInfo:
            # Check whether the name and namespace from serviceInfo matches name and namespace from the statefulset
            if name == statefulset_serviceName and namespace == statefulset_namespace:
                match_found = True
                break
        if match_found == False:
            report.status_extended = f"StatefulSet {statefulset_name} uses non-existent service {statefulset_serviceName} in namespace {statefulset_namespace}"
            return False

        return True

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        services = data.get_services()
        for statefulset in data.get_statefulsets():
            report = Check_Report_K8S(self.metadata())
            report.resource_namespace = statefulset.metadata.namespace
            report.resource_id = statefulset.metadata.name
            report.status = "PASS"

            if not self._execute(statefulset, services, report):
                report.status = "FAIL"

            findings.append(report)

        return findings
