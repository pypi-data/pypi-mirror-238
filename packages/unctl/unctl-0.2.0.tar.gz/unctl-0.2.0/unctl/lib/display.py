import re
import shutil
from collections import defaultdict
import os
from colorama import init, Fore, Style
from prettytable import PrettyTable
import textwrap

from unctl.lib.check.check import ChecksLoader

import textwrap


class Display:
    """Handles display-related functionalities."""

    term_width = 80
    options = None

    @staticmethod
    def init(o):
        """Displays the results of the checks in a formatted table."""
        # Initialize colorama for terminal colored output
        init(autoreset=True)

        # Calculate terminal width for dynamic UI formatting
        Display.term_width = os.get_terminal_size().columns
        Display.options = o

    @staticmethod
    def find_substrings(input_str):
        """Find substrings wrapped in double curly braces in a given string."""
        pattern = r"\{\{([^}]+)\}\}"
        matches = re.findall(pattern, input_str)
        return matches if matches else None

    @staticmethod
    def display_progress_bar_header():
        # Display the progress bar header
        print(
            "\n"
            + Fore.YELLOW
            + Style.BRIGHT
            + "─" * Display.term_width
            + Style.RESET_ALL
        )
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "Running Kubernetes Checks".center(Display.term_width)
            + Style.RESET_ALL
        )
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "─" * Display.term_width
            + Style.RESET_ALL
            + "\n"
        )

    @staticmethod
    def display_progress_bar(percentage, check_name, bar_length=80):
        """Displays a progress bar with the specified percentage completion."""
        blocks = int(round(bar_length * percentage))
        block_char = "▶"

        if percentage < 1:
            filled_part = Fore.LIGHTRED_EX + block_char * blocks + Style.RESET_ALL
            percent_color = Fore.LIGHTRED_EX
        else:
            filled_part = Fore.LIGHTGREEN_EX + block_char * blocks + Style.RESET_ALL
            percent_color = Fore.LIGHTGREEN_EX

        empty_part = " " * (bar_length - blocks)
        progress_string = f"\r{Fore.BLUE + Style.BRIGHT}In progress: {check_name}{Style.RESET_ALL}  |{filled_part + empty_part}| {percent_color + Style.BRIGHT}{percentage*100:.1f}%{Style.RESET_ALL}"

        # Move the cursor up by one line and then clear that line
        move_up_and_clear_line = "\033[A" + "\r" + " " * (Display.term_width - 1) + "\r"
        print(move_up_and_clear_line, end="", flush=True)

        print(progress_string, end="", flush=True)

    @staticmethod
    def check_progress_bar(checks_list, title):
        """Main function to manage the progress bar and checks."""
        results = []

        print("\n" + Fore.YELLOW + Style.BRIGHT + "=" * 50 + Style.RESET_ALL)
        print(Fore.YELLOW + Style.BRIGHT + title.center(50) + Style.RESET_ALL)
        print(Fore.YELLOW + Style.BRIGHT + "=" * 50 + Style.RESET_ALL + "\n")

        total_checks = len(checks_list)
        completed_checks = 0

        # Print an initial progress bar of 0%
        Display.display_progress_bar(0, checks_list[0][0])

        for check_name, check_func in checks_list:
            check_result = check_func()
            completed_checks += 1

            # Update the progress bar
            next_check_name = (
                checks_list[completed_checks][0]
                if completed_checks < total_checks
                else "Done"
            )
            Display.display_progress_bar(
                completed_checks / total_checks, next_check_name
            )

            if check_result[0]:
                results.append(
                    [check_name, Fore.GREEN + "Passed" + Style.RESET_ALL, "N/A", "N/A"]
                )
            else:
                results.append(
                    [
                        check_name,
                        Fore.RED + "Failed" + Style.RESET_ALL,
                        check_result[1].name,
                        check_result[2],
                    ]
                )

        print()  # New line after the progress bar completion
        print()  # Another new line for separation

        return results

    def display_check_results_table(
        results, check_title, check_details, llm_summary=False
    ):
        print()
        # Commenting out the following line to prevent double printing of ❌
        # print(
        #     Fore.WHITE
        #     + Style.BRIGHT
        # + "\t"
        # + f"{check_counter}. Check name: "
        #     + Fore.RED
        #     + f"❌ {check_title}"
        # )

        # Initialize the table for the failed resources under this check
        if llm_summary:
            table = PrettyTable(
                [
                    "Resource Namespace",
                    "Resource ID",
                    "Status",
                    "Severity",
                    "LLM Explanation",
                ]
            )
            table._max_width = {"LLM Explanation": 70}
        else:
            table = PrettyTable(
                [
                    "Resource Namespace",
                    "Resource ID",
                    "Status",
                    "Severity",
                    "Status Extended",
                ]
            )

        # Set table appearance to use solid lines for borders
        table.horizontal_char = "─"
        table.vertical_char = "|"
        table.junction_char = "─"
        table.border = True
        table.frame = True

        failed_resources = [
            detail for detail in check_details if detail.status == "FAIL"
        ]

        if failed_resources:  # Only if there are failed resources
            print(
                Fore.WHITE
                + Style.BRIGHT
                + Fore.RED
                + f"❌ Failure for {failed_resources[0].resource_id} in {failed_resources[0].resource_namespace}"
            )
        else:
            return

        for detail in failed_resources:
            severity_color = (
                Fore.RED
                if detail.check_metadata.Severity == "critical"
                else (
                    Fore.YELLOW
                    if detail.check_metadata.Severity == "severe"
                    else Fore.WHITE
                )
            )
            severity = severity_color + detail.check_metadata.Severity + Style.RESET_ALL
            if llm_summary and hasattr(detail, "llm_failure_summary"):
                status_extended = "🧠 " + detail.llm_failure_summary
                status_extended = (
                    "\n".join(textwrap.wrap(status_extended, width=70))
                    + Style.RESET_ALL
                )

            else:
                status_extended = (
                    "\n".join(textwrap.wrap(detail.status_extended, width=70))
                    + Style.RESET_ALL
                )
            status = Fore.RED + detail.status + Style.RESET_ALL
            resource_id = detail.resource_id
            resource_namespace = detail.resource_namespace
            table.add_row(
                [
                    resource_namespace,
                    resource_id,
                    status,
                    severity,
                    status_extended,
                ],
                divider=True,
            )
        # Color the headers in yellow
        table_string = table.get_string()
        for field_name in table.field_names:
            table_string = table_string.replace(
                field_name,
                Fore.LIGHTBLUE_EX + Style.BRIGHT + field_name + Style.RESET_ALL,
                1,
            )
        print(table_string)

    @staticmethod
    def organize_results_by_resource(results):
        """Organize results by ResourceNamespace and ResourceID."""
        organized_results = defaultdict(lambda: defaultdict(list))

        for check_name, checks in results.items():  # Unpack results dictionary
            for result in checks:  # Iterate over each list of Check_Report_K8S objects
                resource_namespace = result.resource_namespace
                resource_id = result.resource_id

                # Append the result to the appropriate list
                organized_results[resource_namespace][resource_id].append(result)

        return organized_results

    @staticmethod
    def display_results_table(results, llm_summary=False):
        """Displays the results of the checks in a formatted table."""

        term_width = Display.term_width

        print("\n" + Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL)
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "Checks Scan Report".center(term_width)
            + Style.RESET_ALL
        )
        print(Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL + "\n")
        print()

        # Organize results by ResourceNamespace and ResourceID
        organized_results = Display.organize_results_by_resource(results)

        # Iterate through the organized results and display
        for resource_namespace, resources in organized_results.items():
            for resource_id, check_details in resources.items():
                # Print the primary header for the resource
                # print(
                #     f"Pod : {resource_id} in Namespace: {resource_namespace}"
                # )

                # Extract the details and display
                statuses = [detail.status for detail in check_details]

                if all(status == "PASS" for status in statuses):
                    if Display.options.failing_only:
                        continue
                    print()
                    print(
                        Fore.WHITE
                        + Style.BRIGHT
                        + Fore.GREEN
                        + f"✅ All checks passed for {resource_id} in {resource_namespace}"
                    )
                    continue

                else:
                    Display.display_check_results_table(
                        results, "", check_details, llm_summary
                    )

        print("\n" + Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL)
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "End of Scan Report".center(term_width)
            + Style.RESET_ALL
        )
        print(Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL + "\n")
        print()

    @staticmethod
    def debug_results_structure(results):
        unique_combinations = set()

        for result in results:
            sub_service = result.check_metadata.SubServiceName
            check_title = result.check_metadata.CheckTitle

            unique_combinations.add((sub_service, check_title))

        for combo in unique_combinations:
            print(combo)
