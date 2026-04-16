"""
NovaOS LangGraph Workflow
-------------------------
Defines the state machine that drives the agent loop:

    START → perceive → plan → confirm → act → remember → END

Each node is a pure function that receives and returns an AgentState dict.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from novaos.core.agent import AgentState, NovaAgent

logger = logging.getLogger(__name__)


def build_workflow(agent: NovaAgent):
    """
    Build and compile the LangGraph workflow.

    Returns a compiled graph that can be invoked with an initial AgentState.
    """
    try:
        from langgraph.graph import StateGraph, END  # type: ignore
    except ImportError:
        logger.warning("langgraph not installed — using simple sequential runner.")
        return _SimpleWorkflow(agent)

    graph = StateGraph(AgentState)

    # ---- Node definitions ------------------------------------------------

    def perceive(state: AgentState) -> AgentState:
        """Capture screen state if the command requires vision."""
        if agent._needs_vision(state["command"]):
            state["screen_state"] = agent.vision.analyze_screen()
        state["context"] = agent.memory.search(state["command"])
        return state

    def plan(state: AgentState) -> AgentState:
        plan_json = agent._plan(
            state["command"], state["context"], state.get("screen_state")
        )
        state["plan"] = plan_json.get("plan", "")
        state["actions"] = plan_json.get("actions", [])
        return state

    def confirm(state: AgentState) -> AgentState:
        from novaos.config import config
        if config.SAFE_MODE and state["actions"]:
            approved = agent._request_confirmation(
                {"plan": state["plan"], "actions": state["actions"]}
            )
            state["confirmed"] = approved
        else:
            state["confirmed"] = True
        return state

    def act(state: AgentState) -> AgentState:
        if state.get("confirmed", True):
            result = agent._execute_plan(
                {"plan": state["plan"], "actions": state["actions"]}
            )
            state["result"] = result
        else:
            state["result"] = "Action cancelled by user."
        return state

    def remember(state: AgentState) -> AgentState:
        agent.memory.store(state["command"], state.get("result", ""))
        return state

    # ---- Wire the graph --------------------------------------------------

    graph.add_node("perceive", perceive)
    graph.add_node("plan", plan)
    graph.add_node("confirm", confirm)
    graph.add_node("act", act)
    graph.add_node("remember", remember)

    graph.set_entry_point("perceive")
    graph.add_edge("perceive", "plan")
    graph.add_edge("plan", "confirm")
    graph.add_edge("confirm", "act")
    graph.add_edge("act", "remember")
    graph.add_edge("remember", END)

    return graph.compile()


class _SimpleWorkflow:
    """Fallback sequential runner when langgraph is not available."""

    def __init__(self, agent: NovaAgent) -> None:
        self.agent = agent

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        result = self.agent.process_command(state["command"])
        state["result"] = result
        return state
