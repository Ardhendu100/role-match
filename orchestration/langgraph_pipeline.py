# orchestration/langgraph_pipeline.py
"""
Defines the LangGraph workflow (graph), connects nodes, and runs the pipeline.
"""

from langgraph.graph import StateGraph, MessagesState, START, END
from orchestration.nodes import fetch_jobs_node, match_jobs_node, notify_node
from orchestration.context import create_initial_context

# Build the graph
graph = StateGraph(dict)  # Use dict for your context/state
graph.add_node("fetch_jobs", fetch_jobs_node)
graph.add_node("match_jobs", match_jobs_node)
graph.add_node("notify", notify_node)

graph.add_edge(START, "fetch_jobs")
graph.add_edge("fetch_jobs", "match_jobs")
graph.add_edge("match_jobs", "notify")
graph.add_edge("notify", END)

workflow = graph.compile()

if __name__ == "__main__":
    context = create_initial_context()
    result = workflow.invoke(context)
    print("Workflow result:", result)

# to run this use python -m orchestration.langgraph_pipeline