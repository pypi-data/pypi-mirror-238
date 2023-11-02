from unctl.lib.check.models import Check, Check_Report_K8S
from kubernetes import client


class k8s_horizontal_pod_autoscaling(Check):
    def _execute(
        self,
        hpa,
        deployments,
        replicationControllers,
        replicaSets,
        statefulsets,
        report,
    ) -> bool:
        scaleTargetRefName = hpa.spec.scale_target_ref.name
        hpaNamespace = hpa.metadata.namespace
        scaleTargetKind = hpa.spec.scale_target_ref.kind

        matched_resource = None

        if scaleTargetKind == "Deployment":
            for resource in deployments:
                if (
                    resource.metadata.name == scaleTargetRefName
                    and resource.metadata.namespace == hpaNamespace
                ):
                    matched_resource = resource
                    break
        elif scaleTargetKind == "ReplicationController":
            for resource in replicationControllers:
                if (
                    resource.metadata.name == scaleTargetRefName
                    and resource.metadata.namespace == hpaNamespace
                ):
                    matched_resource = resource
                    break
        elif scaleTargetKind == "ReplicaSet":
            for resource in replicaSets:
                if (
                    resource.metadata.name == scaleTargetRefName
                    and resource.metadata.namespace == hpaNamespace
                ):
                    matched_resource = resource
                    break
        elif scaleTargetKind == "StatefulSet":
            for resource in statefulsets:
                if (
                    resource.metadata.name == scaleTargetRefName
                    and resource.metadata.namespace == hpaNamespace
                ):
                    matched_resource = resource
                    break
        else:
            report.status_extended = f"HorizontalPodAutoscaler uses {scaleTargetKind} as ScaleTargetRef, which is not an option."
            return False

        if matched_resource is None:
            report.status_extended = f"HorizontalPodAutoscaler uses {scaleTargetKind}/{scaleTargetRefName} as ScaleTargetRef, which does not exist"
            return False

        report.resource_dep_type = hpa.spec.scale_target_ref.kind
        report.resource_dep_name = hpa.spec.scale_target_ref.name
        containers = len(matched_resource.spec.template.spec.containers)
        for container in matched_resource.spec.template.spec.containers:
            if (
                container.resources.requests is None
                or container.resources.limits is None
            ):
                containers -= 1

        if containers <= 0:
            report.status_extended = f"{scaleTargetKind} {hpa.metadata.namespace}/{scaleTargetRefName} does not have resource configured."
            return False

        return True

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        deployments = data.get_deployments()
        replicationControllers = data.get_replication_controllers()
        replicaSets = data.get_replica_sets()
        statefulsets = data.get_statefulsets()

        for hpa in data.get_hpas():
            report = Check_Report_K8S(self.metadata())
            report.resource_namespace = hpa.metadata.namespace
            report.resource_id = hpa.metadata.name
            report.resource_name = hpa.metadata.name
            report.status = "PASS"

            if not self._execute(
                hpa,
                deployments,
                replicationControllers,
                replicaSets,
                statefulsets,
                report,
            ):
                report.status = "FAIL"

            findings.append(report)

        return findings
