from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Optional
from agents.researcher import run_researcher, ResearchOutput
from agents.writer import run_writer, WriterOutput
from agents.fact_checker import run_fact_checker, FactCheckerOutput
from memory import get_memory, load_session, save_session, THREAD_ID

class AgentState(TypedDict):
    query: str
    research: Optional[ResearchOutput]
    written: Optional[WriterOutput]
    final: Optional[FactCheckerOutput]
    history: list

def researcher_node(state: AgentState) -> AgentState:
    print("Researcher Agent is gathering facts...")
    memory = get_memory()
    result = run_researcher(
        query=state["query"],
        memory=memory,
        thread_id=THREAD_ID,
        history=state["history"]
    )
    return {**state, "research": result}

def writer_node(state: AgentState) -> AgentState:
    print("Writer Agent is structuring the summary...")
    memory = get_memory()
    result = run_writer(
        research=state["research"],
        memory=memory,
        thread_id=THREAD_ID,
    )
    return {**state, "written": result}

def fact_checker_node(state: AgentState) -> AgentState:
    print("Fact Checker Agent is verifying claims...")
    memory = get_memory()
    result = run_fact_checker(
        written=state["written"],
        memory=memory,
        thread_id=THREAD_ID,
    )
    return {**state, "final": result}

def save_history_node(state: AgentState) -> AgentState:
    new_messages = [
        {"role": "user", "content": state["query"]},
        {"role": "assistant", "content": state["final"].verified_summary}
    ]
    save_session(new_messages)
    return state

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.add_node("fact_checker", fact_checker_node)
    graph.add_node("save_history", save_history_node)

    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "fact_checker")
    graph.add_edge("fact_checker", "save_history")
    graph.add_edge("save_history", END)
    
    
    
    return graph.compile()

def run_pipeline(query: str) -> FactCheckerOutput:
    history = load_session()
    graph = build_graph()



    initial_state: AgentState = {
        "query": query,
        "research": None,
        "written": None,
        "final": None,
        "history": history
    }


    final_state = graph.invoke(initial_state)
    return final_state["final"]