from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_pvc_pending(Check):
    def __init__(self, **data):
        super().__init__(**data)

    def create_jobs(self):
        # You might or might not need this depending on your structure
        return None

    def _execute(self, pvc, report) -> bool:
        # Check PVC status
        if pvc.status.phase == "Pending":
            report.status_extended = f"PVC {pvc.metadata.name} in namespace {pvc.metadata.namespace} is in Pending state."
            return False

        return True

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        # Iterate over each PVC
        for pvc in data.get_pvcs():
            report = Check_Report_K8S(self.metadata())

            # Populate report details
            report.resource_id = pvc.metadata.name
            report.resource_pvc = pvc.metadata.name  # New field you might want to add
            report.resource_namespace = pvc.metadata.namespace
            report.status = "PASS"

            if not self._execute(pvc, report):
                report.status = "FAIL"

            findings.append(report)

        return findings
