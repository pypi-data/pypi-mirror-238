"""To overwrite a prompt, subclass BaseOODAPrompts and simply set the desired prompt as the new value."""

from abc import ABC


class AbstractOODAPrompts(ABC):
    FORMULATE = NotImplemented
    ASSESS = NotImplemented
    OBSERVE = NotImplemented
    ORIENT = NotImplemented
    DECIDE = NotImplemented
    ACT = NotImplemented


class BaseOODAPrompts(AbstractOODAPrompts):
    FORMULATE = (
        "Given the user's query, please formulate a clear and concise problem statement and"
        " evaluation objective to best answer it. This will be used to assess how well a given"
        " response meets the criteria."
    )

    ASSESS = (
        "As a reminder, the problem formulation is as follows:\n\n{formulation}\n\n Given the"
        " conversation history, has the user's problem actually been addressed according to the"
        " objective? At the top of your response, include a line that says 'Assessment: True' or"
        " 'Assessment: False' for whether the problem has been solved."
    )

    OBSERVE = (
        "We are in the Observe phase of the OODA loop. The primary objective during this phase is"
        " to collect relevant data and information. If the query is complex, determine whether it"
        " should be broken down into sub-queries. List key facts immediately related to the"
        " question. Your goal is to determine what we know right now about the question, not to"
        " answer it."
    )

    ORIENT = (
        "We are in the Orient phase of the OODA loop. During this phase, the primary objective is"
        " to interpret and make sense of the information collected. Synthesize the facts from the"
        " Observe phase. Determine whether we still need to obtain or do something in order to"
        " answer the user's query."
    )

    DECIDE = (
        "We are now in the Decide phase of the OODA loop. In this phase, you are to evaluate"
        " possible courses of action based on your understanding from the Orient phase. Weigh the"
        " pros and cons of each solution. Your goal is to decide the best approach to answer the"
        " question fully."
    )

    ACT = (
        "We are in the Act phase of the OODA loop. If the query is ready to be answered, construct"
        " your response. If the query needs further decomposition, define parameters for a sub-OODA"
        " loop."
    )
