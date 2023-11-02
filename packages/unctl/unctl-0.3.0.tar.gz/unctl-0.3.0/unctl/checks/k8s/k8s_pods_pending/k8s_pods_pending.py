from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_pods_pending(Check):
    def _execute(self, pod, report) -> bool:
        failures = []

        if pod.status.phase != "Pending":
            return True

        # Check through container status to check for crashes
        for condition in pod.status.conditions:
            if condition.type == "PodScheduled" and condition.reason == "Unschedulable":
                failures.append({"name": pod.metadata.name, "condition": condition})
                report.status_extended = "Pod is unschedulable"  # FIXME
                return False

        for container_status in pod.status.container_statuses:
            # container is not running
            if container_status.state.waiting:
                if (
                    container_status.state.waiting.reason == "CrashLoopBackOff"
                    or container_status.state.waiting.reason == "ImagePullBackOff"
                ):
                    report.resource_container = container_status.name

                    # collect waiting message for pod
                    if container_status.state.waiting.message != "":
                        report.status_extended = f"Container {report.resource_container} in {container_status.state.waiting.message} state"

                if container_status.state.waiting.reason == "ContainerCreating":
                    report.resource_container = container_status.name
                    report.status_extended = f"Container {report.resource_container} in {container_status.state.waiting.reason} state"
                    # collect event log for pod
                    # and look for evt.Reason == "FailedCreatePodSandBox" && evt.Message != ""

            else:
                # when pod is Running but its ReadinessProbe fails
                if not container_status.ready and pod.status.phase == "Running":
                    report.resource_container = container_status.name
                    report.status_extended = f"Container {report.resource_container} in {container_status.ready} state"
                    # collect event log for pod
                    # and look for evt.Reason == "Unhealthy" && evt.Message != ""

        return False

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        for pod in data.get_pods():
            report = Check_Report_K8S(self.metadata())
            report.resource_id = pod.metadata.name
            report.resource_pod = pod.metadata.name
            report.resource_namespace = pod.metadata.namespace
            report.status = "PASS"

            if not self._execute(pod, report):
                report.status = "FAIL"

            findings.append(report)

        return findings
