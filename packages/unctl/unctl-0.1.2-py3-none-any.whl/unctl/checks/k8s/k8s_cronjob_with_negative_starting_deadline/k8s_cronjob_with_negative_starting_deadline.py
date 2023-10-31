from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_cronjob_with_negative_starting_deadline(Check):
    def _execute(self, cron, report) -> bool:
        if (
            cron.spec.starting_deadline_seconds is None
            or cron.spec.starting_deadline_seconds < 0
        ):
            report.status_extended = (
                "Cronjob has starting deadline value as ("
                + str(cron.spec.starting_deadline_seconds)
                + ") "
            )
            return False

        return True

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        for cron in data.get_cronjobs():
            report = Check_Report_K8S(self.metadata())
            report.resource_namespace = cron.metadata.namespace
            report.resource_name = cron.metadata.name
            report.status = "PASS"

            if not self._execute(cron, report):
                report.status = "FAIL"

            findings.append(report)

        return findings
