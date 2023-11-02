from argparse import ArgumentParser, REMAINDER, SUPPRESS
import sys
import os

from unctl.lib.check.check import ChecksLoader

from unctl.lib.llm.openai import LLM
from unctl.lib.display import Display
from unctl.checks.k8s.service import execute_k8s_cli

from json import dumps as json_dumps
from tempfile import NamedTemporaryFile

from unctl.scanrkube import JobDefinition, Application, KubernetesDataCollector
from unctl.version import check, current

from functools import partial
import concurrent.futures


def execute_recommendations(result):
    """Execute the check's diagnostics logic"""

    diags_list = result.recommendations

    # print(f"Running diagnostics for {result.resource_id}")
    script = NamedTemporaryFile(mode="w+t", delete=False)
    script.write("#!/bin/bash\n")
    for diag in diags_list:
        script.write("echo " + diag + "\n")
        script.write(diag + "\n")
    script.close()
    diagnostics = "bash " + script.name

    print(f"Running diagnostics CLI({diagnostics}) for {result.resource_id}")
    result.recommendations_output = execute_k8s_cli(diagnostics)

    return result.recommendations_output


def unctl_process_args():
    parser = ArgumentParser(prog="unctl")

    description = ""
    description = description + str("\n")
    description = description + str("\t  Welcome to unSkript CLI Interface \n")
    parser.description = description

    parser.add_argument(
        "-s", "--scan", help="Run a k8s scan", action="store_true", default=True
    )
    parser.add_argument(
        "-f", "--failing-only", help="Show only failing checks", action="store_true"
    )
    parser.add_argument(
        "-d",
        "--diagnose",
        help="Run fixed diagnosis",
        action="store_true",
    )
    parser.add_argument(
        "-e",
        "--explain",
        help="Explain failures using AI",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--remediate",
        help="Create remediation plan",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--check",
        help="Run a single check",
        action="store_true",
    )
    parser.add_argument("-v", "--version", action="version", version=current())

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if args.scan is True:
        print("Running scan")
    elif args.diagnose is True:
        print("Running diagnose")
    elif args.explain is True:
        print("Running explain")
    elif args.check is True:
        print("Running single check")
    elif args.remediate is True:
        print("Running remediate")
    else:
        parser.print_help()

    return args


# analyze results
# Find create a dictionary of objects that failed checks


def annotate_failing_objects(results):
    # FIXME: can be improved
    failed_objects_dict = {}
    failure_record_list = []

    for check_name, results in results.items():
        for r in results:
            if r.status == "PASS":
                continue

            failure_record_list.append(r)
            if r.resource_id not in failed_objects_dict:
                failed_objects_dict[r.resource_id] = []
            # else:
            #     failed_objects[r.resource_id].append(r)

    return failed_objects_dict, failure_record_list


# TBD lookup the inventory and make sure this matches up
def get_object_id(object_name):
    return object_name.split("/")[-1]


# Set up and invoke the LLM analysis
def analyze_result(r, llm):
    check_name = r.check_metadata.CheckTitle
    fail_sig = (
        f"{r.resource_id} failed check for {check_name} because ({r.status_extended})"
    )

    # FIXME: remove dicts here and simplify
    check_cli = "\n".join(r.check_cli_output.keys())
    check_cli_output = "\n".join(r.check_cli_output.values())
    d_output = "\n".join(r.diagnostics_cli_output.values())
    d_check_cli_output = "\n" + check_cli + "\n" + check_cli_output + "\n"

    llm_analysis_record = llm.get_recommendations(
        fail_sig, check_cli, d_check_cli_output, d_output
    )

    if llm_analysis_record is None:
        r.llm_analysis_record = None
        return r

    # update the record with the LLM analysis
    r.llm_analysis_record = llm_analysis_record
    r.llm_failure_summary = llm_analysis_record.get("summary")
    r.llm_failure_diagnostics = llm_analysis_record.get("diagnostics")
    r.recommendations = llm_analysis_record.get("diagnostics")

    return r


def analyze_result_postprocess(r, failed_objects):
    check_name = r.check_metadata.CheckTitle

    print(f"\n❌ Failed {check_name}: {r.resource_id} ({r.status_extended})")
    if r.llm_analysis_record is None:
        print(f"🤯 LLM failed to analyze {r.resource_id} check {check_name}")
        return

    diags = "> " + "\n> ".join(r.llm_failure_diagnostics)
    print(f"💬  Summary:\n{r.llm_failure_summary.rstrip()}")
    print(f"🛠️  Diagnostics: \n{diags}")

    # LLM gives a list of possible downstream failures
    # and we run it through the list of known failures
    # this means that LLM list of failures is a superset
    related_objects = []
    for obj in r.llm_analysis_record.get("objects"):
        # FIXME: this needs to be improved, and is assuming that names are unique across types
        object_name = get_object_id(obj)
        if object_name in failed_objects and object_name != r.resource_id:
            related_objects.append(object_name)
            failed_objects[object_name].append(r)

    # note that depends_on stores the object_id
    r.depends_on = related_objects
    if len(r.depends_on) > 0:
        print(f"⚙️  Related objects: {json_dumps(related_objects, indent=2)}")
    failed_objects[r.resource_id].append(r)

    # print(f"Diagnostics\n: {d_output}")
    return r


def analyze_results(results, o):
    # create list of failures on which to call LLM
    failed_objects, failure_record_list = annotate_failing_objects(results)

    # TBD: need some progress display here
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        fetcher = partial(analyze_result, llm=o)
        results = executor.map(fetcher, failure_record_list)

    # FIXME: might need some failure handling here
    for result in results:
        analyze_result_postprocess(result, failed_objects)

    return failed_objects


def get_failure_id(r):
    return (r.resource_id, r.check_metadata.CheckID)


# convert the dict of objects with their failures to a dict of failures with list of objects
def analyze_failure_relationships(failed_objects):
    triage = {}
    for obj, failures in failed_objects.items():
        for f in failures:
            if triage.get(get_failure_id(f)) is None:
                triage[get_failure_id(f)] = [obj]
            else:
                triage[get_failure_id(f)].append(obj)

    # return only the items where multiple failure are related
    return {k: v for k, v in triage.items() if len(v) > 1}


def analyze_related_objects(failing_object_names, objs, failed_objects, o):
    related_failures = {}
    count = 0
    o.start_multi_prompt(failing_object_names)
    for obj in objs:
        for r in failed_objects[obj]:
            check_name = r.check_metadata.CheckTitle
            fail_sig = f"{r.resource_id} failed check for {check_name} because ({r.status_extended})"
            if fail_sig in related_failures:
                # skipping duplicate failures
                continue

            count += 1
            print(f"\t❌ Failed {check_name}: {r.resource_id} ({r.status_extended})")
            related_failures[fail_sig] = True

            # FIXME: manual de-duplication
            if check_name.find("CrashLoopBackOff") >= 0:
                continue

            check_cli = "\n".join(r.check_cli_output.keys())
            check_cli_output = "\n".join(r.check_cli_output.values())
            d_output = "\n".join(r.diagnostics_cli_output.values())
            d_check_cli_output = "\n" + check_cli + "\n" + check_cli_output + "\n"

            o.add_to_multi_prompt(check_cli, d_check_cli_output, d_output)

    (diagnosis, llm_next_steps_record) = o.end_multi_prompt()

    return count, diagnosis, llm_next_steps_record


def unctl():
    # check version and notify if new version released
    check()

    options = unctl_process_args()
    o = None
    if options.explain is True:
        try:
            o = LLM()
        except Exception as e:
            sys.exit("Failed to initialize LLM: " + str(e))

    Display.init(options)

    # Load the checks to be run
    cur_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(cur_dir, os.pardir))
    loader = ChecksLoader(root_dir=root_dir, checks_dir="unctl/checks")
    check_modules = loader.load_all()

    # Create a job definition
    job_definer = JobDefinition(check_modules)
    jobs = job_definer.generate_jobs()
    print(f"✅ Created jobs")

    # collect inventory
    collector = KubernetesDataCollector()
    print(f"✅ Collected Kubernetes data")

    # Run the checks
    run_diags = options.diagnose or options.explain
    app = Application(collector, jobs)
    results = app.execute(run_diags=run_diags)

    if options.explain is False:
        # explanations not needed: print and exit
        Display.display_results_table(results)
        return

    # for each failure, print out the summary
    # and the recommendations
    print(f"\n\n🤔 Analyzing results...\n")
    failed_objects = analyze_results(results, o)
    failing_object_names = ", ".join(list(failed_objects.keys()))
    Display.display_results_table(results, llm_summary=True)

    if options.remediate is False:
        return

    print("\n")
    print("🤔 Trying to find failures with related root cause...\n")

    # convert the list of objects with failures to a list of failures with objects
    triage = analyze_failure_relationships(failed_objects)
    triage_summary = []
    for failure_id, objs in triage.items():
        resource_id, check_id = failure_id

        print(
            f"\n💡 Failures on {objs} are correlated by check {check_id}. Initiating common analysis\n"
        )

        # print(f"✅ Analyzing the following failures together:")
        count, diagnosis, llm_next_steps_record = analyze_related_objects(
            failing_object_names, objs, failed_objects, o
        )

        summary = llm_next_steps_record.get("summary")
        # if summary is not None:
        #     print(f"\n✅ Diagnosis: {summary}✅")
        # else:
        #     print(f"\n✅ Diagnosis: {diagnosis}✅")

        # print(f"Next steps: {llm_next_steps_record.get('objects')}")

        triage_record = {
            "summary": summary,
            "diagnosis": diagnosis,
            "objects": objs,
            "check_id": check_id,
            "next_steps": llm_next_steps_record,
            "count": count,
        }
        triage_summary.append(triage_record)

    print("\n")
    print("💡 Issues to be triaged in order of suggested priority:\n")

    # done with failure clustering
    # received set of next steps for each cluster
    # ask user to select the cluster and start executing next steps

    triage_summary = sorted(triage_summary, key=lambda k: k.get("count"), reverse=True)

    for i, t in enumerate(triage_summary):
        objs = t.get("objects")
        check_id = t.get("check_id")
        summary = t.get("summary")
        count = t.get("count")

        print(f"🧠 Issue {i+1}:\n")
        print(
            f"💬 Summary: {count} failures across objects {objs} are found to be related. {summary}\n"
        )

    selection = input(
        f"🔢 Select the issue to analyze (1-{i+1}) and press enter to continue\n> "
    )
    if selection == "":
        return

    t = triage_summary[int(selection) - 1]
    print(t)

    plan = o.get_next_steps_from_summary(t.get("summary"), failing_object_names)

    print(f"🔬 Next steps: {plan.get('justification')}")
    print(f"1. Root Cause Objects : {plan.get('p1')}")
    print(f"2. Directly Affected Objects {plan.get('p2')}")
    print(f"3. Indirectly Affected Objects {plan.get('p3')}")

    selection = input(
        "🔢 Select the group (1, 2 or 3) that you want to investigate further and press enter to continue\n> "
    )
    print(f"Select object:")
    for i, obj in enumerate(plan.get("p" + selection)):
        print(f"{i+1}. {obj}")

    obj_idx = ""
    while obj_idx == "":
        obj_idx = input("Enter the object number to execute the plan\n> ")
    obj = plan.get("p" + selection)[int(obj_idx) - 1]

    # print(failed_objects[obj])

    print(f"Executing plan {selection} for {obj}")
    for r in failed_objects[obj]:
        if r.resource_id != obj:
            continue
        print(f"🧠 Summary: {r.llm_failure_summary}")
        d = "> " + "\n> ".join(r.llm_failure_diagnostics)
        print(f"Recommended Diagnostics:\n{d}")
        choice = input("Execute diagnostics? (Y/n)\n> ")

        if choice == "n":
            print("Skipping")
            continue

        print(f"Executing diagnostics for {r.resource_id}")
        reco_output = execute_recommendations(r)

        # print(f"Diagnostics output:\n{reco_output}")

        o.get_final_recommendations(r.llm_failure_summary, reco_output)

        # print(f"Details: {r.llm_analysis_record}")

    return
    # failed_objects is a dictionary of objects that failed checks
    # the keys are the object names, and the values are a list of
    # Check_Report_K8S objects

    # for any given failure, find all associated objects and then
    # try to analyze all the failures together

    # above is simply the failure explanations from LLM. These are basic
    # as a next step, we can start trying to relate the failures
    # strategies
    # 1. collect objects in a single namespace
    # 2. collect items in a single investigation
    # 3. collect items in

    # o.get_global_recommendations()

    # second pass
    # should skip objects with depends_on set to non-empty
    print("\n\n---Executing second pass---\n\n")

    for object_name, results in failed_objects.items():
        for r in results:
            if len(r.depends_on) > 0:
                print(
                    f"Skipping {r.resource_id} because it depends on downstream failures {r.depends_on}"
                )
                continue

            check_name = r.check_metadata.CheckTitle

            print(f"❌ Failed {check_name}: {r.resource_id} ({r.status_extended})")
            fail_sig = f"{r.resource_id} failed check for {check_name} because ({r.status_extended})"

            for check_cli in r.check_cli_output:
                check_cli_output = r.check_cli_output[check_cli]

            # execute the recommended diagnostics for the failed objects
            execute_recommendations(r)

            for cli in r.diagnostics_cli_output:
                output = r.diagnostics_cli_output[cli]
                print(f"Diagnostics:\n{cli}")

            for cli in r.recommendations_output:
                reco_output = r.recommendations_output[cli]
                print(f"Diagnostics:\n{cli}")

            output = "\n".join(output.splitlines())
            check_cli_output = "\n".join(check_cli_output.splitlines())
            reco_output = "\n".join(reco_output.splitlines())

            d_output = "\n" + cli + "\n" + output + "\n" + reco_output + "\n"
            d_check_cli_output = "\n" + check_cli + "\n" + check_cli_output + "\n"

            llm_analysis_record = o.get_recommendations(
                fail_sig, check_cli, d_check_cli_output, cli, d_output
            )

            # LLM gives a list of possible downstream failures
            # and we run it through the list of known failures
            # this means that LLM list of failures is a superset
            related_objects = []
            for obj in llm_analysis_record.get("objects"):
                # FIXME: this needs to be improved, and is assuming that names are unique across types
                object_name = obj.split("/")[-1]
                if object_name == r.resource_id:
                    # self referntial failure means this is a leaf node
                    continue
                if object_name in failed_objects and object_name != r.resource_id:
                    related_objects.append(object_name)

            # note that depends_on stores the object_id
            r.depends_on = related_objects
            if len(r.depends_on) > 0:
                print(f"Related objects: {json_dumps(related_objects, indent=2)}")

            # print(f"Diagnostics\n: {d_output}")


from unctl.__main__ import unctl

if __name__ == "__main__":
    sys.exit(unctl())
