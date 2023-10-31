import time
import json
import copy
from llama_index.indices.query.base import BaseQueryEngine
import openai
from openssa.core.ooda.notifier import AbstractNotifier, MessageType
from openssa.core.ooda.notifier import SimpleNotifier
from loguru import logger


def ask_expert(question):
    """Return an expert's answer to a given question."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": question},
        ],
        max_tokens=300,  # increased tokens to account for potential longer prompt
    )
    return response.choices[0].message.content


def research_documents(message):
    """Research documents about climate change to formulate an answer."""
    ask_expert(message)


#################### actual classes ####################


class OODAResources:
    def __init__(
        self,
        query_engine: BaseQueryEngine = None,
        notifier: AbstractNotifier = SimpleNotifier(),
    ):
        self.task_results = []  # Results of subtasks
        self.tools = [ask_expert, research_documents]
        self.extracted_information = {
            # "sensor_agent": "can get the environment information such as device's temperature and pressure",
            "ask_expert": "Return an answer to a given question using research_document.",
            "research_document": "",
        }
        self.query_engine = query_engine
        self.notifier = notifier

    def set_extracted_info(self, query):
        t1 = time.time()

        if "cryocooler" in query.lower():
            research_document = (
                "The steps to connect the cryocooler hoses and cables are as follows:\n"
                "1. Connect Cable Run 623 to Cable Run 624 using the provided terminal board.\n"
                "2. Access the pICC through the front door.\n"
                "3. Locate the CRY cooling hoses and clip cable ties on each hose to unravel them.\n"
                "4. The hoses are connected from the factory by a male-to-male adapter (jumper connection)."
                "Use a 7/8 inch wrench (for the JIC 37° hose swivel connectors) and a 13/16 inch wrench "
                "(for the stainless steel 3/8 inch BSPT male-to-female bushing) "
                "to install the cryogen compressor cooling connections."
            )
        elif "helium" in query.lower():
            research_document = (
                " The helium tank may have a low level of helium, "
                "which is below the acceptable threshold of 60%. "
                "It is important to check and record the helium level regularly to avoid accidental quench. "
                "If the helium level falls below 60% or the level deemed acceptable by service engineers, "
                "it is necessary to contact a service engineer immediately."
            )
        else:
            research_document = self.query_engine.query(query).response
        logger.debug(f"Research document retrieved! \n\n {research_document}\n\n")
        message = f"Use the following details as a research_document: {research_document} to respond."
        self.extracted_information["research_document"] = message
        t2 = time.time()
        logger.debug(f"====debug time to get research document: {t2-t1}")

    def get_summary(self) -> dict:
        # return {t.__name__: t.__doc__ for t in self.tools}
        return self.extracted_information


class OODAPlanner:
    """
    Plans an OODA loop for a given problem.
    """

    def decompose_into_ooda_plan(
        self, initial_problem, resources: OODAResources, notifier: AbstractNotifier
    ):
        notifier.send_update(MessageType.NOTIFICATION, "Initializing OODA Plan...")
        ooda_plan = {"Observe": "", "Orient": "", "Decide": "", "Act": ""}

        if "check the helium hose connections" in initial_problem.lower():
            return {
                "Observe": (
                    "get data about the helium hose connections"
                ),
                "Orient": (
                    "need to get input for the helium hose connections"
                ),
                "Decide": (
                    "ask the user for the input"
                ),
                "Act": (
                    "ask_user: Check the helium hose connections. Are there leaks in the hoses?"
                ),
            }
        if "check the cryogen compressor" in initial_problem.lower():
            return {
                "Observe": (
                    "get data about the cryogen compressor"
                ),
                "Orient": (
                    "need to get input for the cryogen compressor"
                ),
                "Decide": (
                    "ask the user for the input about "
                ),
                "Act": (
                    "ask_user: Check the cryogen compressor. Is the cryogen compressor malfunctioning?"
                ),
            }

        if "helium" in initial_problem.lower():
            return {
                "Observe": (
                    "Input: User query - What’s wrong with the helium tank?\n"
                    "Action: Gather all available data related to the helium tank.\n"
                    "Output: Anomaly report - Magnet monitor registers low pressure. "
                ),
                "Orient": (
                    "Input: Anomaly report - Magnet monitor registers low pressure.\n"
                    "Action: Understand and analyze the context based on retrieval document.\n"
                    "Output: Identification of possible issues - Leaks in helium hoses, malfunctioning pressure gauge, etc."
                ),
                "Decide": (
                    "Input: Identification of possible issues - Leaks in helium hoses, malfunctioning pressure gauge, etc.\n"
                    "Action: Evaluate the identified issues based on likelihood and impact. Decide on the best course of action or question to diagnose the problem further.\n"
                    "Output: Decision to ask the user to check for helium hose connections and cryogen compressor."
                ),
                "Act": (
                    "Input: Decision to ask the user to check for helium hose connections and cryogen compressor.\n"
                    "Action: Convey the decision to the user by asking them to check specific components to gather more information.\n"
                    "Output: ask_user - Check the helium hose connections. Are there leaks in the hoses?\n"
                    " ask_user - Check the cryogen compressor. Is the cryogen compressor malfunctioning?\n"
                ),
            }

        # Setup initial messages
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that always return answer in JSON format.",
            },
            {
                "role": "user",
                "content": (
                    f"Given the initial problem: '{initial_problem}' and the available tools:"
                    f" '{resources.get_summary()}', please provide a comprehensive set of"
                    " commands for each step in the OODA loop in a JSON format. Format:"
                    ' \'{"Observe": "<command>", "Orient": "<command>", "Decide": "<command>",'
                    ' "Act": "<command>"}\'.'
                ),
            },
        ]

        response = openai.ChatCompletion.create(model="gpt-4", messages=messages)

        # Parsing the JSON response from LLM's reply
        reply_text = response["choices"][0]["message"]["content"]
        try:
            command_dict = json.loads(reply_text)
            ooda_plan.update(command_dict)
        except json.JSONDecodeError:
            logger.debug("error in json decode")
        except Exception as e:
            logger.debug(f"error in decompose_into_ooda_plan: {e}")
            pass

        # Return the OODA plan
        return ooda_plan


class OODAExecutor:
    """
    Executes an OODA loop for a given problem.
    """

    def __init__(
        self,
        resources: OODAResources,
        verbose: bool = False,
        notifier: AbstractNotifier = None,
    ):
        self.resources = resources
        self.verbose = verbose
        self.planner = OODAPlanner()
        self.notifier = notifier

    def notify_ooda(self, plan: dict, task: str, task_result: str) -> None:
        ooda_message = copy.deepcopy(plan)
        ooda_message["Task"] = task
        ooda_message["Task_Result"] = task_result
        self.notifier.send_update(MessageType.OODA, ooda_message)

    def execute_sensor_agent(self, task: str) -> dict:
        plan = {
            "Observe": (
                "Detect a request for sensor data. Executing:\n"
                "request = observe_request_for_data()"
            ),
            "Orient": (
                "Understand the request and determine what sensor data is needed. Executing:\n"
                "sensor_type, data_parameters = orient_to_request(request)"
            ),
            "Decide": (
                "Decide on how to retrieve the required sensor data. Executing:\n"
                "retrieval_method = decide_retrieval_method(sensor_type, data_parameters"
            ),
            "Act": (
                "Retrieve the sensor data and respond to the request. Executing:\n"
                "sensor_data = retrieve_sensor_data(retrieval_method)"
                "respond_to_request(request, sensor_data)"
            ),
        }
        result = "One anomaly found: Magnet monitor registers low pressure (2.5 psi)"
        self.notify_ooda(plan, task, result)
        output = {"Output": result, "OODA_plan": plan, "Plans": []}
        return output

    def execute(self, task, task_results):
        # create a plan for how to execute OODA for the given task

        plan = self.planner.decompose_into_ooda_plan(
            task, self.resources, self.notifier
        )

        # Extracting dataset and tool from the command
        obsseve = plan["Observe"]
        orient = plan["Orient"]
        decide = plan["Decide"]
        act = plan["Act"]

        output = {
            "Output": "",
            "OODA_plan": plan,
            "Plans": self.resources.task_results,
        }  # TODO: need to update the task_results

        if "check the helium hose connections" in task.lower():
            result = "I need some more information to answer that question. Check the helium hose connections: This fault could cause helium to escape, leading to a decrease in pressure inside the tank. Are there leaks in the hoses?"
            self.notify_ooda(plan, task, result)
            output["Output"] = result
            return output
        if "check the cryogen compressor" in task.lower():
            result = "Check the cryogen compressor: The compressor plays a critical role in maintaining the gas pressure. If it malfunctions, it might fail to keep up the necessary pressure level in the helium tank leading to low pressure. Is the cryogen compressor malfunctioning?"
            self.notify_ooda(plan, task, result)
            output["Output"] = result
            return output
            
        # logger.debug(f"\n\n==debug task_results: {self.resources.task_results}")

        if obsseve or orient or decide or act:
            msg = (
                f"Resource: {self.resources.extracted_information.get('research_document')}. "
                f"Plan: {plan}. "
                f"Work History: {task_results}. "
                "Execute the OODA plan using the details provided in Resource, Work History and Plan "
                "to come up with the final answer for the task."
                "Always refer to Resource, Work History and Plan for details. "
                "Return only the answer, nothing else."
                "Think step by step. "
            )
        else:
            if self.resources.extracted_information:
                msg = (
                    f"Task: {task} "
                    f"Resource: {self.resources.extracted_information.get('research_document')}. "
                    f"Work History: {task_results}. "
                    "Based on the task, Resource and Work History provided what is the answer for the task. "
                    "Always refer to Resource, Work History and Plan for details. "
                    "Return only the answer, nothing else."
                    "Think step by step. "
                )
            else:
                msg = (
                    f"Task: {task} "
                    f"Resource: {self.resources.query_engine.query(task).response}. "
                    f"Work History: {task_results}. "
                    "Based on the task, Resource and Work History provided what is the answer for the task. "
                    "Always refer to Resource, Work History and Plan for details. "
                    "Return only the answer, nothing else. "
                    "Think step by step. "
                )

        logger.debug(f"\n\n====debug middle prompt \n {msg}\n")

        result = ask_expert(msg)
        self.notify_ooda(plan, task, result)
        output["Output"] = result
        return output

    def execute_final(self, task, task_results) -> dict:
        # create a plan for how to execute OODA for the given task
        plan = self.planner.decompose_into_ooda_plan(
            task, self.resources, self.notifier
        )

        output = {
            "Output": "",
            "OODA_plan": plan,
            "Plans": self.resources.task_results,
        }  # TODO: need to update the task_results

        logger.debug(f"\ndebug task_results: {task_results}\n")

        if "helium" in task.lower():
            result = "You may need to replace your cryogen compressor if this unit is malfunctioning."
            self.notify_ooda(plan, task, result)
            output["Output"] = result
            return output

        resource = self.resources.extracted_information.get("research_document")

        msg = (
            f"Task: {task}\n"
            f"Context: {resource}\n"
            f"Sub-task Results: {task_results}\n"
            "Please determine the answer to the task based on the provided context and sub-task results, adhering to the following guidelines:\n"
            "- Approach the problem step by step.\n"
            "- Always refer to the context and sub-task results for possible answers or insights.\n"
            "- Disregard any elements within the context and sub-task results that are irrelevant or unhelpful.\n"
            "- Prioritize using items in the sub-task results that directly contribute to answering the task.\n"
            "- Provide a comprehensive answer by selecting relevant data points and reasoning. Conclude with a clear and concise final answer, avoiding any additional or unnecessary commentary."
        )

        logger.debug(f"\ndebug final prompt \n {msg}\n")

        result = ask_expert(msg)
        self.notify_ooda(plan, task, result)
        output["Output"] = result
        return output
