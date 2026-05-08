from langgraph.graph import StateGraph, END
from assembler import AssemblerBase
from nodes import assembler_node, logic_node, assembler_coder_node, increment_node, should_finish, component_architekt_node, final_assembler_node, saver, route_after_saver


workflow = StateGraph(AssemblerBase)

workflow.add_node('manager', assembler_node)
workflow.add_node('selector', logic_node)
workflow.add_node('coder', assembler_coder_node)
workflow.add_node('increment', increment_node)
workflow.add_node('architect', component_architekt_node)
workflow.add_node('final_assemble', final_assembler_node)
workflow.add_node('saver', saver)

workflow.set_entry_point('manager')

workflow.add_edge('manager', 'selector')
workflow.add_edge('selector', 'architect')
workflow.add_edge('architect', 'coder')
workflow.add_edge('coder', 'saver')

workflow.add_conditional_edges(
    "saver",
    route_after_saver,
    {
        "continue": "increment",
        "end": END
    }
)


workflow.add_conditional_edges(
    "increment",
    should_finish,
    {
        'selector': "selector",
        'final_assemble': "final_assemble"
    }
)

workflow.add_edge('final_assemble', 'saver')

app = workflow.compile()

initial_state = {
    "project_goal": """
    Modern AI SaaS Landing Page: 'NEURAL-CORE'. 
    Theme: Futuristic Minimalist Dark Mode.
    
    Design Rules:
    - Background: 'bg-[#030303]' (Absolute Black)
    - Primary Accent: 'indigo-500'
    - Text: Primary 'slate-100', Secondary 'slate-500' (very clean contrast).
    - Cards: 'bg-white/[0.02]' with a thin 'border-white/10' and 'backdrop-blur-xl'.
    
    Structure:
    1. Navbar: Absolute minimalist. Logo on left, 3 links on right, no big borders.
    2. Hero: Huge headline 'Scale your mind' with 'tracking-tighter' and 'font-black'. Subtle indigo glow behind the text.
    3. Features Grid: 3 cards. Use 'mdi:brain', 'mdi:flash', 'mdi:security' icons. Each card must have a very subtle indigo hover border.
    4. Statistics: A horizontal bar showing '99.9% Uptime', '10M+ Requests', '256-bit Encryption'.
    5. CTA Section: A large indigo gradient button with 'shadow-indigo-500/20'.

    Technical Constraints:
    - KRYTYCZNE: Każdy komponent musi być w OSOBNYM PLIKU.
    - App.jsx ma tylko importować i układać komponenty.
    - Używaj tylko @iconify/react.
    - Dodaj 'items = []' dla bezpieczeństwa w mapach.
    """,
    "files_to_create": [],
    "current_file_idx": 0,
    "project_structure": [],
    "current_file": "",
    "iteration_count": 0
}

final_state = app.invoke(initial_state)

for file_info in final_state['project_structure']:
    print(f"Plik: {file_info['name']} ->\n {file_info['code']}")

