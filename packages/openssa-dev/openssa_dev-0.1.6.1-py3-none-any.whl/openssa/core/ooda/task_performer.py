import json

import openai
from openssa.core.ooda.ooda import OODAExecutor, OODAResources
from openssa.core.ooda.notifier import AbstractNotifier, MessageType
from llama_index.indices.query.base import BaseQueryEngine
from loguru import logger


class TASK_STATE:
    USER_INPUT = "USER_INPUT"
    NORMAL = "NORMAL"
    FINISHED = "FINISHED"


class TaskPerformer:
    """
    Performs a task.
    """

    def __init__(
        self,
        verbose: bool = False,
        query_engine: BaseQueryEngine = None,
        notifier: AbstractNotifier = None,
    ):
        self.verbose = verbose
        self.query_engine = query_engine
        self.notifier = notifier
        self.task_results = []  # Results of subtasks

    def requires_subtasks(self, task: str, resources: OODAResources) -> bool:
        # if "the picc" in task.lower():
        #     return True

        if "cryocooler" in task.lower():
            return False

        if "helium" in task.lower():
            return True

        # Enhanced prompt for task evaluation.
        prompt = (
            f"Let's evaluate the task: '{task}'.\n"
            f"Available Resources: {resources.get_summary()}\n"
            "Our objective is to determine whether this task can be executed directly or requires further breakdown into subtasks. "
            "Avoid suggesting a breakdown unless it is absolutely necessary for task completion.\n"
            "Please respond in JSON format:\n"
            '- If the task is directly executable, respond with \'{"answer": "directly executable"}\'.\n'
            '- If the task necessitates further decomposition, respond with \'{"answer": "needs breakdown"}\'.'
        )

        # OpenAI Chat completion with GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Using the GPT-4 model for response generation.
            messages=[
                {
                    "role": "system",  # System message to set the role of the assistant.
                    "content": "You are a helpful problem-solving assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },  # User message containing the enhanced prompt.
            ],
            max_tokens=500,  # Allotted token limit for the response. Adjusted for potential longer responses.
        )

        # Extracting answer from JSON structured response
        try:
            response_content = json.loads(response.choices[0].message["content"])
            return response_content.get("answer", "").lower() == "needs breakdown"
        except json.JSONDecodeError:
            self.notifier.send_update(
                MessageType.NOTIFICATION, "Failed to decode the response as JSON."
            )
            return False
        except Exception as e:
            return False

    def decompose_into_subtasks(self, task, resources: OODAResources) -> list:
        """Breaks down a large problem into N distinct smaller tasks/problems"""

        if "helium" in task.lower():
            return [
                "ask_user: Check the helium hose connections",
                # "ask_user: I need some more information to answer that question. Check the helium hose connections: This fault could cause helium to escape, leading to a decrease in pressure inside the tank. Are there leaks in the hoses?"
                # "ask_user: Check the cryogen compressor: The compressor plays a critical role in maintaining the gas pressure. If it malfunctions, it might fail to keep up the necessary pressure level in the helium tank leading to low pressure. Is the cryogen compressor malfunctioning?"
                "ask_user: Check the cryogen compressor",
            ]

        # Construct a prompt to decompose the problem.
        prompt = (
            f"Given the resources we have at our disposal {resources.get_summary()}, "
            f"we need to break down the task '{task}' into 2 smaller, manageable subtasks that can "
            "effectively utilize these resources. "
            "Please provide the subtasks in a list format in JSON, "
            'like this: \'{"tasks": ["subtask1", "subtask2"]}\'. Make sure your '
            "response is in valid JSON format."
        )

        # logger.debug(f"\n decompose prompt:\n {prompt}\n")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=300,  # Adjust as needed
            temperature=0.5,
        )

        # Assuming the returned content is a JSON string, we parse it.
        # For example, the output might be: '{"tasks": ["task1", "task2", ...]}'
        response_content = response.choices[0].message.content.strip()
        decomposed_tasks = json.loads(response_content)
        # self.notifier.send_update(MessageType.SUBTASKS, decomposed_tasks)
        return decomposed_tasks["tasks"]

    def set_initial_resourse(self, resourses: OODAResources, task):
        resourses.set_extracted_info(task)

    def run(
        self,
        message: str,
        state: str = "",
        data: dict = {},
        task_id: str = "1",
        task_order: int = 1,
    ):
        return self.run2(message, task_id, task_order, data, state)

    def run2(
        self,
        task: str,
        task_id: str = "1",
        task_order: int = 1,
        data: dict = {},
        state: str = "",
    ):
        if state == TASK_STATE.USER_INPUT:
            resources = OODAResources(
                query_engine=self.query_engine, notifier=self.notifier
            )
            logger.debug(f"data in user input: {data}")
            tasks = data.get("tasks", [])
            task = tasks.pop(0)
            data["tasks"] = tasks
            executor = OODAExecutor(resources, self.verbose, notifier=self.notifier)
            result = executor.execute(task, self.task_results)
            if len(tasks) <= 1:
                state = TASK_STATE.FINISHED
            self.notifier.send_update(MessageType.TASK_RESULT, result)
            return result, state, data

        if state == TASK_STATE.FINISHED:
            resources = OODAResources(
                query_engine=self.query_engine, notifier=self.notifier
            )
            executor = OODAExecutor(resources, self.verbose, notifier=self.notifier)
            tasks = data.get("tasks", [])
            task = tasks.pop(0)
            result = executor.execute_final(task, self.task_results)
            self.notifier.send_update(MessageType.TASK_RESULT, result)
            return result, TASK_STATE.NORMAL, {}

        else:
            resources = OODAResources(
                query_engine=self.query_engine, notifier=self.notifier
            )
            self.set_initial_resourse(resources, task)

            if task_order == 1:
                logger.debug(f"========== first run task: {task} ==========")

                if "status" in task.lower():
                    logger.debug("========== status task ==========")
                    executor = OODAExecutor(
                        resources, self.verbose, notifier=self.notifier
                    )
                    status_task = "Request status from sensor"
                    result = executor.execute_sensor_agent(status_task)
                    self.notifier.send_update(MessageType.TASK_RESULT, result)
                    return self.get_output(task, result, data)

                logger.debug("Checking if task requires subtasks...")
                if self.requires_subtasks(task, resources):
                    logger.debug(
                        f"Task {task_id}. '{task}' requires subtasks.",
                    )
                    try:
                        tasks = self.decompose_into_subtasks(task, resources)
                    except Exception as e:
                        tasks = []
                        logger.debug(e)
                    tasks = tasks[:2]
                    # add task to last of tasks
                    tasks.append(task)
                    # tasks.append(task)
                    data["tasks"] = tasks
                    for n, t in enumerate(tasks, start=1):
                        state = (
                            TASK_STATE.USER_INPUT
                            if "ask_user" in t
                            else TASK_STATE.NORMAL
                        )
                        subtask_result, subtask_state, subtask_data = self.run2(
                            t,
                            f"{task_id}.{n}",
                            task_order=task_order + 1,
                            data=data,
                            state=state,
                        )
                        if state == TASK_STATE.USER_INPUT:
                            return subtask_result, subtask_state, subtask_data
                        ts = f"task: {t} - answer: {subtask_result}"
                        self.task_results.append(ts)
                else:
                    logger.debug(f"Task {task_id}. '{task}' does NOT require subtasks.")

        # Now we can execute the task as an OODA loop
        executor = OODAExecutor(resources, self.verbose, notifier=self.notifier)
        self.notifier.send_update(MessageType.EXECUTING, f"{task_id}. {task}")
        if task_order == 1:
            logger.debug(f"========== last run task: {task} ==========")
            result = executor.execute_final(task, self.task_results)
            self.notifier.send_update(MessageType.TASK_RESULT, result)
        else:
            result = executor.execute(task, self.task_results)
        return self.get_output(task, result, data)

    def get_output(self, task, result: dict, data: dict) -> tuple:
        output = result.get("Output", "")
        state = "PROCESSING"
        memory = data.get("memory", [])
        memory.append("user: " + task)
        memory.append("ai: " + output)
        data["memory"] = memory
        return output, state, data
