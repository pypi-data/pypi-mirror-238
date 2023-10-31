from abc import ABC, abstractmethod

from .ooda_expert import AbstractOODAExpert, BaseOODAExpert
from .ooda_prompts import AbstractOODAPrompts, BaseOODAPrompts


class AbstractOODAExecutor(ABC):
    @property
    @abstractmethod
    def prompts(self) -> AbstractOODAPrompts:
        """The prompts that the system uses to guide the problem-solving process."""
        pass

    @property
    @abstractmethod
    def expert(self) -> AbstractOODAExpert:
        """The expert that the system consults for help."""
        pass

    @property
    @abstractmethod
    def tools(self) -> dict:
        """A list of tools that the system can use to solve problems."""
        pass

    @property
    @abstractmethod
    def history(self) -> list:
        """The history of the conversation."""
        pass

    @property
    @abstractmethod
    def formulation(self) -> str:
        """The problem formulation."""
        pass

    @abstractmethod
    def log(self, role, content):
        """Log a message to the history."""
        pass

    @abstractmethod
    def execute(self, input):
        """Execute the problem-solving loop."""
        pass

    @abstractmethod
    def formulate(self):
        """Formulate a problem and an objective from the user's message."""
        pass

    @abstractmethod
    def assess(self) -> bool:
        """Assess whether the problem has been solved."""
        pass

    @abstractmethod
    def use(self, name, input):
        """Call a function with given parameters."""
        pass

    @abstractmethod
    def observe(self):
        """Collect observations according to the prompt and the conversation history."""
        pass

    @abstractmethod
    def orient(self):
        """Interpret and make sense of the information collected."""
        pass

    @abstractmethod
    def decide(self):
        """Evaluate possible courses of action based on the understanding from the orient phase."""
        pass

    @abstractmethod
    def act(self):
        """Construct a response or formulate function calls to execute."""
        pass


class BaseOODAExecutor(AbstractOODAExecutor):
    def __init__(self, tools=None):
        self._prompts = BaseOODAPrompts()
        self._expert = BaseOODAExpert()
        self._history = []
        self._tools = tools
        self._formulation = None

    """PROPERTIES"""

    @property
    def prompts(self) -> AbstractOODAPrompts:
        return self._prompts

    @prompts.setter
    def prompts(self, prompts: AbstractOODAPrompts):
        self._prompts = prompts

    @property
    def expert(self) -> AbstractOODAExpert:
        return self._expert

    @expert.setter
    def expert(self, expert: AbstractOODAExpert):
        self._expert = expert

    @property
    def tools(self) -> dict:
        return self._tools

    @tools.setter
    def tools(self, tools: dict):
        self._tools = tools

    @property
    def history(self) -> list:
        return self._history

    @history.setter
    def history(self, history: list):
        self._history = history

    @property
    def formulation(self) -> str:
        return self._formulation

    @formulation.setter
    def formulation(self, formulation: str):
        self._formulation = formulation

    """BASE FUNCTIONS"""

    def log(self, role, content):
        self.history.append({"role": role, "content": content})

    def execute(self, input, max_iterations=5):
        """
        Takes in a user's message and executes a problem-solving loop on it. During execution,
        tools may be called upon to help solve the problem. The system's full history of thoughts and
        actions is returned.

        :param input: The user's message.
        :return: The system's history during solving the problem.
        """

        # reset history for this new problem and add the user's input to the history
        self.history = []
        self.log("user", input)

        # formulate a problem and objective from the user input, update history
        self.formulate()

        iterations = 0
        while self.assess() is False and iterations < max_iterations:
            self.observe()
            self.orient()
            self.decide()
            self.act()
            iterations += 1
        print(f"Completed in {iterations} iterations.")

    def formulate(self):
        """Formulate a problem and an objective from the user's message."""
        self.log("system", self.prompts.FORMULATE)
        self.formulation = self.expert.query(self.history)
        self.log("assistant", self.formulation)

    def assess(self) -> bool:
        """Assess whether the problem has been solved."""
        self.log("system", self.prompts.ASSESS.format(formulation=self.formulation))
        assessment = self.expert.query(self.history)
        self.log("assistant", assessment)
        assessment = "true" in assessment.split("\n")[0].lower()
        return assessment

    def use(self, name, input):
        """
        Call a function with given parameters. Tools are functions that take in a string and return
        a string. Each tool is responsible for parsing the input string for parameters and returning
        a string that reports back the output.

        :param name: The name of the tool to use.
        :param input: The input to the tool.
        :return: The output of the tool.
        """
        # choose from the list of functions in self.tools the one with the given name
        tool = next(filter(lambda x: x.__name__ == name, self.tools))

        # call the function with the given parameters
        response = eval(f"{tool.__name__}({input})")

        # add the function call to the history
        self.history.append({"role": "function", "name": tool.__name__, "content": response})

        return response

    """OODA LOOP FUNCTIONS"""

    def observe(self):
        self.log("system", self.prompts.OBSERVE)
        response = self.expert.query(self.history)
        self.log("assistant", response)

    def orient(self):
        self.log("system", self.prompts.ORIENT)
        response = self.expert.query(self.history)
        self.log("assistant", response)

    def decide(self):
        self.log("system", self.prompts.DECIDE)
        response = self.expert.query(self.history)
        self.log("assistant", response)

    def act(self):
        self.log("system", self.prompts.ACT)
        response = self.expert.query(self.history)
        self.log("assistant", response)
