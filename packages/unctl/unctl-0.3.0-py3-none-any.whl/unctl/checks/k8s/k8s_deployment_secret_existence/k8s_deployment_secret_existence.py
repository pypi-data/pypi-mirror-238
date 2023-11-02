from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_deployment_secret_existence(Check):
    def _execute(self, deployment, secrets, report) -> bool:
        secretsInfo = [
            (secret.metadata.name, secret.metadata.namespace) for secret in secrets
        ]
        deploymentNamespace = deployment.metadata.namespace

        containers_info = deployment.spec.template.spec.containers or []

        # Get the secrets from deployments
        secrets = [
            env.value_from.secret_key_ref.name
            for container_info in containers_info
            for env in (container_info.env or [])
            if env.value_from and env.value_from.secret_key_ref
        ]

        no_match_found = True

        for secret_name in secrets:
            if (secret_name, deploymentNamespace) not in secretsInfo:
                report.status_extended = f"Secret name {secret_name} in Deployment for namespace {deploymentNamespace} does not exist in the list of Secrets."
                no_match_found = False  # Set the flag to False

        return no_match_found

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        secrets = data.get_secrets()
        for deployment in data.get_deployments():
            report = Check_Report_K8S(self.metadata())
            report.resource_namespace = deployment.metadata.namespace
            report.resource_id = deployment.metadata.name
            report.status = "PASS"

            if not self._execute(deployment, secrets, report):
                report.status = "FAIL"

            findings.append(report)

        return findings
