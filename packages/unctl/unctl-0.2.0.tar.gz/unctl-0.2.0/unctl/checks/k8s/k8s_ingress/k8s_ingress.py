from unctl.lib.check.models import Check, Check_Report_K8S


class k8s_ingress(Check):
    def _execute(self, ingress, services, secrets, ingress_classes, report) -> bool:
        ingressName = ingress.metadata.name
        ingressClassName = None

        if hasattr(ingress, "spec"):
            ingressClassName = ingress.spec.ingress_class_name

        ingressNamespace = ingress.metadata.namespace
        ingressClassInfo = [
            (s.metadata.name, s.metadata.namespace) for s in ingress_classes
        ]

        serviceInfo = [(s.metadata.name, s.metadata.namespace) for s in services]
        secretsInfo = [(s.metadata.name, s.metadata.namespace) for s in secrets]

        if ingressClassName is None:
            ingressClassValue = ingress.metadata.annotations.get(
                "kubernetes.io/ingress.class"
            )
            if not ingressClassValue:
                # this is more a best practice issue that a requirement
                report.status_extended = f"Ingress {ingressNamespace}/{ingressName} is missing an Ingress class configuration"
                return False

            ingressClassName = ingressClassValue

        if ingressClassName is not None:
            classMatchFound = False
            for name, namespace in ingressClassInfo:
                if ingressClassName == name and ingressNamespace == namespace:
                    classMatchFound = True
                    break

            if classMatchFound == False:
                report.status_extended = f"Ingress {ingressNamespace}/{ingressName} uses non-existent ingress class {ingressClassName}"
                return False

        if hasattr(ingress, "spec") and hasattr(ingress.spec, "rules"):
            for rule in ingress.spec.rules:
                for path in rule.http.paths:
                    ingressServiceName = path.backend.service.name
                    serviceMatchFound = False
                    for service_name, service_namespace in serviceInfo:
                        if (
                            ingressServiceName == service_name
                            and ingressNamespace == service_namespace
                        ):
                            serviceMatchFound = True
                            break

                    if serviceMatchFound == False:
                        report.status_extended = f"Ingress {ingressNamespace}/{ingressName} uses non-existent service {ingressServiceName}"
                        return False

        if hasattr(ingress, "spec") and hasattr(ingress.spec, "tls"):
            for tls in ingress.spec.tls:
                tlsSecretName = tls.secret_name
                secretMatchFound = False
                for secret_name, secret_namespace in secretsInfo:
                    if (
                        tlsSecretName == secret_name
                        and ingressNamespace == secret_namespace
                    ):
                        secretMatchFound = True
                        break

                if secretMatchFound == False:
                    report.status_extended = f"Ingress {ingressNamespace}/{ingressName} uses non-existent TLS secret {ingress.metadata.namespace}/{tls.secret_name}"
                    return False

        return True

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        services = data.get_services()
        secrets = data.get_secrets()
        ingress_classes = data.get_ingress_classes()

        for ingress in data.get_ingresses():
            report = Check_Report_K8S(self.metadata())
            report.resource_namespace = ingress.metadata.namespace
            report.resource_id = ingress.metadata.name
            report.status = "PASS"

            if not self._execute(ingress, services, secrets, ingress_classes, report):
                report.status = "FAIL"

            findings.append(report)

        return findings
