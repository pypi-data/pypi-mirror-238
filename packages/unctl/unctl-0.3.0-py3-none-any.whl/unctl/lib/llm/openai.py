import os
import openai
import backoff


from tiktoken import get_encoding
from json import loads as json_loads
from json import load as json_load
from json import dumps as json_dumps
from json import dump as json_dump


def count_tokens(text):
    encoding = get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)


class LLM:
    def __init__(self):
        if os.getenv("OPENAI_API_KEY") is None:
            raise Exception("OPENAI_API_KEY is not set")

        openai.api_key = os.getenv("OPENAI_API_KEY")

        # deduplicate outputs
        self._known_outputs = {}

        self._big_prompt_data = []
        self._big_prompt_failures = []

        self._big_prompt_len = 0
        self._big_prompt_failures_len = 0

        self._multi_prompt = []

    def _convert_string_list_to_prompt(self, messages, role):
        prompt = []
        for m in messages:
            prompt.append({"role": role, "content": m})
        return prompt

    def _convert_string_list_to_system_prompt(self, messages):
        return self._convert_string_list_to_prompt(messages, "system")

    def _add_to_big_prompt(self, messages):
        self._big_prompt_data.extend(messages)

    def _add_to_big_failures_only_prompt(self, messages):
        self._big_prompt_failures.extend(messages)

    def _get_cached_completion(self, messages):
        # Check if response is cached in local file
        cache_key = json_dumps(messages)
        cache_file_path = "openai_cache.json"
        if os.path.exists(cache_file_path):
            with open(cache_file_path, "r") as f:
                cache = json_load(f)
            if cache_key in cache:
                return cache[cache_key]

        print("Cache miss")
        return None

    def _put_cached_completion(self, messages, completion):
        cache_file_path = "openai_cache.json"
        cache_key = json_dumps(messages)
        if os.path.exists(cache_file_path):
            with open(cache_file_path, "r") as f:
                cache = json_load(f)
            cache[cache_key] = completion
        else:
            cache = {cache_key: completion}
        with open(cache_file_path, "w") as f:
            json_dump(cache, f)

        return

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def _completions_with_backoff(self, **kwargs):
        return openai.ChatCompletion.create(**kwargs)

    def _get_completion_from_messages(
        self, messages, model="gpt-4-0613", temperature=0
    ):
        if openai.api_key is None:
            print("Error: OPENAI_API_KEY is not set")
            return

        # if self._get_cached_completion(messages) is not None:
        #     return self._get_cached_completion(messages)

        try:
            # Make API call and cache response
            response = self._completions_with_backoff(
                model=model,
                messages=messages,
                temperature=temperature,
            )

        except openai.error.InvalidRequestError as e:
            print(f"Error: {e}")
            print(
                "Error: Failed to get response from OpenAI API for the following prompt:"
            )
            for m in messages:
                print(f" 💬 {m.get('content')}")
            return ""

        completion = response.choices[0].message["content"]
        # self._put_cached_completion(messages, completion)

        return completion

    def start_multi_prompt(self, failing_objects):
        messages_system = [
            "You are kubernetes expert help with diagnosing a problem.",
            # "You are given a list of k8s objects with known failures.",
            "You are given a set of commands outputs, delimited by ```",
            "Your task is to analyze these outputs together and establish a root cause for the failures.",
            "Provide a JSON object with following fields",
            "summary: summary of the problem and possible root cause",
            f"objects: subset of items from this list that are of interest: [{failing_objects}]",
            # "diagnostics: list of specific kubectl commands to execute as next steps of investigation - these need to be readonly steps",
            # "remediation: list of kubectl commands to execute to remediate - these can be readonly steps or can be admin steps too",
        ]

        # reset the multi prompt
        self._multi_prompt = []

        for m in messages_system:
            self._multi_prompt.append({"role": "system", "content": m})

        # self._multi_prompt.append({"role": "user", "content": f"failing objects: {failing_objects}"})
        self._multi_prompt.append({"role": "user", "content": "```"})

    def add_to_multi_prompt(self, check_cli, d_check_cli_output, d_output):
        messages_user = [
            # f'The output of "{check_cli}" was flagged as failure and is provided below delimited by ```',
            f"{d_check_cli_output}",
            # f"The diagnostics CLI outputs are provided below delimited by ```",
            f"{d_output}",
        ]

        for m in messages_user:
            self._multi_prompt.append({"role": "user", "content": m})
            # print(m)

    def end_multi_prompt(self):
        self._multi_prompt.append({"role": "user", "content": "```"})

        # print("---Multi prompt---")
        # for m in self._multi_prompt:
        #     print(m.get("content"))

        response = (
            self._get_completion_from_messages(self._multi_prompt).lstrip().rstrip()
        )
        # print(response)

        diagnosis = response
        if response.find("```json") >= 0:
            diagnosis = response[: response.find("```json")]
            response = response[response.find("```json") + 7 :]
        if response.find("```") >= 0:
            response = response[: response.find("```")]

        return (diagnosis, json_loads(response))

    def get_next_steps_from_summary(self, summary, failing_objs):
        messages_user = [
            f"{summary}\n",
            f"The list of failing objects is [{failing_objs}].\n"
            # "Give me just the list of objects sorted by priority of investigation",
            "Give me the list of objects sorted by priority of investigation.",
            "To sort the objects by priority of investigation, focus on the root cause of the issue and then look at the objects that are directly affected by it.",
            "Provide the answer as a json object with the following keys",
            "p1: Highest priority - Root Cause",
            "p2: Medium priority - Directly Affected Objects",
            "p3: Low priority - Indirectly Affected/Dependent Objects",
            "justification: justification for the priority order",
        ]

        prompt = []
        for m in messages_user:
            prompt.append({"role": "user", "content": m})
            # print(m)

        response = (
            self._get_completion_from_messages(prompt, temperature=0).lstrip().rstrip()
        )

        # print(response)
        return json_loads(response)

    def _clean_response(self, response):
        if response.find("```json") >= 0:
            response = response[response.find("```json") + 7 :]
        if response.find("```") >= 0:
            response = response[: response.find("```")]

        return response

    def get_recommendations(self, obj, check_cli, d_check_cli_output, d_output):
        messages_system = [
            "You are kubernetes expert helping me with troubleshooting a problem.",
        ]
        messages_user = [
            f'The output of "{check_cli}" was flagged as failure and is provided below delimited by ```',
            f"```{d_check_cli_output}```",
            f"The diagnostics CLI outputs are provided below delimited by ```",
            f"```{d_output}```",
            "Provide a JSON object with following fields",
            "summary: summary of the problem",
            "objects: list of kubernetes resource names that this failure depends upon",
            "diagnostics: list of kubectl commands to execute as next steps - these need to be readonly steps",
            # "remediation: list of kubectl commands to execute to remediate - these can be readonly steps or can be admin steps too",
        ]

        messages = []
        for m in messages_system:
            messages.append({"role": "system", "content": m})

        for m in messages_user:
            messages.append({"role": "user", "content": m})

        response = self._get_completion_from_messages(messages)
        # print(f"Remediation recommendations: {check_cli}")
        # print(response)

        # remove the ```json and ``` from the response
        json_response = self._clean_response(response)
        try:
            if json_loads(json_response) is not None:
                return json_loads(json_response)
        except:
            print(f"💣 Error: Failed to parse response from OpenAI API:")
            print(f"💣 Error: Failed to parse response from OpenAI API: {response}")
            for m in messages:
                print(f"  {m.get('content')}")
            input()

        return None

        self._big_prompt_failures_len += count_tokens(d_check_cli_output)
        self._big_prompt_len += count_tokens(d_output)

        if check_cli not in self._known_outputs:
            self._add_to_big_prompt(
                [
                    {"role": "user", "content": f'"""{obj}"""'},
                    {"role": "user", "content": f"```{d_check_cli_output}```"},
                ]
            )

            self._add_to_big_failures_only_prompt(
                [
                    {"role": "user", "content": f'"""{obj}"""'},
                    {"role": "user", "content": f"```{d_check_cli_output}```"},
                ]
            )

            self._known_outputs[check_cli] = True
        else:
            print(f"Skipping {check_cli} as it is already known")

        # for m in messages:
        #     print(m.get("content"))

        response = self._get_completion_from_messages(messages)
        # print(f"Remediation recommendations: {check_cli}")
        # print(response)

        return json_loads(response)

    def get_global_recommendations(self):
        return

        _big_cluster_prompt = [
            "You are kubernetes expert helping me with troubleshooting a problem.",
            "You are given a set of commands outputs, delimited by ```",
            'The name of the failing objects are provided on a separate line delimited by """',
            "Please analyze the provided failures and cluster them considering both their failure signature and the relationships or commonalities in object names. I would like an integrated analysis that combines insights from both methods.",
            "For each cluster, provide a JSON object with the following fields",
            "summary: summary of the problem",
            "diagnostics: list of commands to execute as next steps - these need to be readonly steps",
            "remediation: list of commands to execute to remediate - these can be readonly steps or can be admin steps too",
            "confidence: your confidence in the validity of this cluster of failures",
            "Also suggest which cluster should be investigated first.",
            "Also suggest which other outputs will help select the cluster to diagnose first.",
        ]

        _big_cluster_prompt_failures_only = [
            "You are kubernetes expert helping me with troubleshooting a problem.",
            "You can given a set of commands output, delimited by ```",
            'The name of the failing objects are provided in a separate line delimited by """',
            "Please analyze the provided failures and cluster them considering both their failure signature and the relationships or commonalities in object names. I would like an integrated analysis that combines insights from both methods.",
            "For each cluster, provide a JSON object with the following fields",
            "summary: summary of the problem",
            "diagnostics: list of commands to execute as next steps - these need to be readonly steps",
            "remediation: list of commands to execute to remediate - these can be readonly steps or can be admin steps too",
            "confidence: your confidence in the validity of this cluster of failures",
            "Also suggest which cluster should be investigated first.",
            "Also suggest which other outputs will help select the cluster to diagnose first.",
        ]

        print("---Big cluster prompt---")
        p = (
            self._convert_string_list_to_system_prompt(_big_cluster_prompt)
            + self._big_prompt_data
        )
        for m in p:
            print(m.get("content"))
        print("---Big failures signature prompt end---")

        print("Connecting to OpenAI API...")
        if self._big_prompt_len < 8192:
            response = self._get_completion_from_messages(p)
            # Print the responses
            print("Remediation recommendations:")
            print(response)
            return

        # try a few things
        # 1. use the failures only prompt
        # 2. for each failure, provide set of all failures and failure diagnostics in the hope that the diagnostics will correlate with an existing failing object

        if self._big_prompt_failures_len > 8192:
            print("Combined length of just all failures is too long, can't use LLM")
            return

        print("Big prompt is too long, trying to use failures only prompt")
        p = (
            self._convert_string_list_to_system_prompt(
                _big_cluster_prompt_failures_only
            )
            + self._big_prompt_failures
        )
        response = self._get_completion_from_messages(p)

        # Print the responses
        print("Remediation recommendations:")
        print(response)

    def get_final_recommendations(self, problem, recommended_output):
        messages_system = [
            "You are kubernetes expert helping me with troubleshooting a problem.",
            f"We are troubleshooting a problem with the following summary: {problem}",
            "Diagnostic output for this problem are delimited by ```",
            "What would be your recommendation for next steps towards fixing this problem?",
        ]
        messages_user = [
            f"```{recommended_output}```",
        ]

        messages = []
        for m in messages_system:
            messages.append({"role": "system", "content": m})

        for m in messages_user:
            messages.append({"role": "user", "content": m})

        response = self._get_completion_from_messages(messages)
        print(response)

        # # remove the ```json and ``` from the response
        # json_response = self._clean_response(response)
        # try:
        #     if json_loads(json_response) is not None:
        #         return json_loads(json_response)
        # except:
        #     print(f"💣 Error: Failed to parse response from OpenAI API:")
        #     print(f"💣 Error: Failed to parse response from OpenAI API: {response}")
        #     for m in messages:
        #         print(f"  {m.get('content')}")
        #     input()

        return None
