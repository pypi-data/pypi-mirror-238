from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_service_empty(Check):
    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        endpoints = data.get_endpoints()
        for service in data.get_services():
            report = Check_Report_K8S(self.metadata())
            report.resource_id = service.metadata.name
            report.resource_service = service.metadata.name
            report.resource_namespace = service.metadata.namespace
            report.status = "PASS"

            service_endpoints = [
                ep
                for ep in endpoints
                if ep.metadata.name == service.metadata.name and ep.subsets
            ]

            if len(service_endpoints) == 0:
                report.status = "FAIL"
                report.status_extended = "Service has NO endpoints"

                # populate the selector for diagnostics
                s = []
                for k, v in service.spec.selector.items():
                    s.append(f"{k}={v}")
                report.resource_selector = ",".join(s)

            findings.append(report)

        return findings
