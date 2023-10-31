from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_deployment_insufficient_replicas(Check):
    def __init__(self, **data):
        super().__init__(**data)

    def create_jobs(self):
        return None

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        for deployment in data.get_deployments():
            report = Check_Report_K8S(self.metadata())
            report.resource_id = deployment.metadata.name
            report.resource_namespace = deployment.metadata.namespace
            report.status = "PASS"

            # Check if the desired replica count matches the available replica count
            if deployment.spec.replicas != deployment.status.available_replicas:
                report.status = "FAIL"
                report.status_extended = f"Deployment {deployment.metadata.name} has {deployment.status.available_replicas} replicas available out of {deployment.spec.replicas} desired."
                findings.append(report)

            if report.status == "PASS":
                findings.append(report)

        return findings
