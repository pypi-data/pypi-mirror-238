from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_node_ready(Check):
    def _execute(self, node, report) -> bool:
        failures = []

        for condition in node.status.conditions:
            # node is ready
            if condition.type == "Ready" and condition.status == "True":
                continue

            # node is not ready
            if condition.type == "Ready" and condition.status != "True":
                failures.append({"name": node.metadata.name, "condition": condition})

            # node has some other failure condition
            if condition.status != "False":
                failures.append({"name": node.metadata.name, "condition": condition})

        if len(failures) > 0:
            return False

        return True

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        for node in data.get_nodes():
            report = Check_Report_K8S(self.metadata())
            report.resource_id = node.metadata.name
            report.resource_node = node.metadata.name
            report.status = "PASS"

            if not self._execute(node, report):
                report.status = "FAIL"
                report.status_extended = "Node has failure conditions"

            findings.append(report)

        return findings
