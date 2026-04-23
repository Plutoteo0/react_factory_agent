from langgraph.graph import StateGraph, END
from nodes import architect_node, coder_node, reviewer_node, saver_node
from agentbase import AgentBase

def can_continue(state: AgentBase):
    last_critique = state['critique'][-1]
    if 'POZYTYWNY' in last_critique or state['iteration_count'] > 3:
        print('WSZYTKO GRA')
        return 'saver'
    return 'coder'

workflow = StateGraph(AgentBase)

workflow.add_node('architect', architect_node)
workflow.add_node('coder', coder_node)
workflow.add_node('reviewer', reviewer_node)
workflow.add_node('saver', saver_node)


workflow.set_entry_point('architect')

workflow.add_edge('architect', 'coder')
workflow.add_edge('coder', 'reviewer')
workflow.add_edge('reviewer', 'saver')

workflow.add_conditional_edges(
    'reviewer',
    can_continue,
    {
        "coder": 'coder',
        'saver': 'saver'
    }
)

initial_state: AgentBase = {
    'specification': 'Zrob 2 przykladowe przyciski z uzyciem stylu Tailwind',
    'generated_code': '',
    'critique': [],
    'iteration_count': 0,
}

app = workflow.compile()
result = app.invoke(initial_state)
print(result['generated_code'])
