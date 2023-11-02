import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pydantic import BaseModel, ValidationError
from unctl.lib.logger import logger
from json import load as json_load
from re import findall as find_substrings
from unctl.checks.k8s.service import execute_k8s_cli
from tempfile import NamedTemporaryFile


class Code(BaseModel):
    """Check's remediation information using IaC like CloudFormation, Terraform or the native CLI"""

    NativeIaC: str
    Terraform: str
    CLI: str
    Other: str


class Recommendation(BaseModel):
    """Check's recommendation information"""

    Text: str
    Url: str


class Remediation(BaseModel):
    """Check's remediation: Code and Recommendation"""

    Code: Code
    Recommendation: Recommendation


class Check_Metadata_Model(BaseModel):
    """Check Metadata Model"""

    Enabled: bool = field(default=True)

    # target system - k8s, aws etc
    Provider: str
    CheckID: str

    # Name of the check
    CheckTitle: str
    CheckType: list[str]
    ServiceName: str
    SubServiceName: str
    ResourceIdTemplate: str
    Severity: str
    ResourceType: str
    Description: str
    Risk: str
    RelatedUrl: str
    Remediation: Remediation
    Categories: list[str]
    DependsOn: list[str]
    RelatedTo: list[str]
    Notes: str

    # Cli to be typed to get the same check implemented
    Cli: str

    # Healthy Pattern: presence of this pattern indicates healthy items
    PositiveMatch: str

    # Unhealthy Pattern: presence of this pattern indicates unhealthy items
    NegativeMatch: str

    # For unhealthy items, what further outputs can be collected
    DiagnosticClis: list[str]

    # When did it start failing MM-DD-YYYY-HH-MM-SS
    # LastPassTimestamp: str
    # LastFailTimestamp: str


class Check(ABC, Check_Metadata_Model):
    def __init__(self, **data):
        """Check's init function. Calls the CheckMetadataModel init."""
        # Parse the Check's metadata file
        metadata_file = (
            os.path.abspath(sys.modules[self.__module__].__file__)[:-3] + ".json"
        )

        # Store it to validate them with Pydantic
        data = Check_Metadata_Model.parse_file(metadata_file).dict()

        # Calls parents init function
        super().__init__(**data)
        # print(f"loading check {self.CheckID}")

        self._metadata_file = metadata_file

    def metadata(self) -> dict:
        """Return the JSON representation of the check's metadata"""
        return self.json()

    @abstractmethod
    def execute(self):
        """Execute the check's logic"""

    def _find_substrings(self, input_str) -> list[str]:
        # Regular expression pattern for matching substrings within double curly braces
        pattern = r"\{\{([^}]+)\}\}"
        matches = find_substrings(pattern, input_str)
        return matches if len(matches) > 0 else []

    def _create_diag_cli(self, cli, params):
        """Create the diagnostic CLI"""

        for p in self._find_substrings(cli):
            if getattr(params, p) is None or len(getattr(params, p)) == 0:
                print(f"Error: {p} is None for {params.resource_id}")
                break
            cli = cli.replace("{{" + p + "}}", params.__dict__[p])

        if len(self._find_substrings(cli)) != 0:
            print(f"Error: {cli} has unresolved parameters for {params.resource_id}")
            return None

        return cli

    def execute_diagnostics(self, result):
        """Execute the check's diagnostics logic"""

        check_cli = self._create_diag_cli(self.Cli, result)
        if check_cli is None:
            return

        result.check_cli_output[check_cli] = execute_k8s_cli(check_cli)

        # print(f"Running diagnostics for {result.resource_id}")
        diags_list = []
        for cli in self.DiagnosticClis:
            diagnostics = self._create_diag_cli(cli, result)
            if diagnostics is None:
                # should we continue or break?
                continue
            diags_list.append(diagnostics)

        if len(diags_list) > 1:
            script = NamedTemporaryFile(mode="w+t", delete=False)
            script.write("#!/bin/bash\n")
            for diag in diags_list:
                script.write("echo " + diag + "\n")
                script.write(diag + "\n")
            script.close()
            diagnostics = "bash " + script.name
            # print(
            #     f"Running diagnostics CLI({diagnostics}) for {result.resource_id}")
            result.diagnostics_cli_output[diagnostics] = execute_k8s_cli(diagnostics)
        else:
            diagnostics = diags_list[0]
            # print(
            #     f"Running diagnostics CLI({diagnostics}) for {result.resource_id}")
            result.diagnostics_cli_output[diagnostics] = (
                diagnostics + "\n" + execute_k8s_cli(diagnostics)
            )

        return


@dataclass
class Check_Report:
    """Contains the Check's finding information."""

    status: str
    status_extended: str
    check_metadata: Check_Metadata_Model

    resource_id: str
    resource_name: str
    resource_details: str
    resource_tags: list
    resource_configmap: str

    # TBD: convert to string
    check_cli_output: dict
    diagnostics_cli_output: dict
    recommendations_output: str

    llm_failure_summary: str
    llm_failure_diagnostics: list
    llm_analysis_record: dict = field(default_factory=dict)

    depends_on: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)

    def __init__(self, metadata):
        self.status = ""
        self.check_metadata = Check_Metadata_Model.parse_raw(metadata)
        self.status_extended = ""
        self.resource_details = ""
        self.resource_id = ""
        self.resource_name = ""
        self.resource_tags = []
        self.resource_configmap = ""


@dataclass
class Check_Report_K8S(Check_Report):
    """Contains the AWS Check's finding information."""

    resource_namespace: str = field(default="")
    resource_pod: str = field(default="")
    resource_node: str = field(default="")
    resource_cluster: str = field(default="")
    resource_service: str = field(default="")
    resource_pvc: str = field(default="")
    resource_container: str = field(default="")
    resource_selector: str = field(default="")
    resource_dep_type: str = field(default="")
    resource_dep_name: str = field(default="")
    resource_configmap: str

    def __init__(self, metadata):
        super().__init__(metadata)

        self.check_cli_output = {}
        self.diagnostics_cli_output = {}
        self.recommendations_output = {}
