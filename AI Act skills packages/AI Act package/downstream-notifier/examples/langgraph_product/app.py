from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    input: str
    output: str
    safety_score: float  # New security metric

def model_node(state: State):
    return { 'output': f'Processed: {state["input"]}', 'safety_score': 0.9 }

def safety_moderator(state: State):
    # Functional Change: Added safety filtering layer
    if state.get('safety_score', 0) < 0.8:
        return { 'output': 'Blocked: Security Risk' }
    return state

workflow = StateGraph(State)
workflow.add_node('model', model_node)
workflow.add_node('moderator', safety_moderator) # New security node

workflow.add_edge(START, 'model')
workflow.add_edge('model', 'moderator')
workflow.add_edge('moderator', END)

app = workflow.compile() # Note: Latency impact due to extra moderation step
