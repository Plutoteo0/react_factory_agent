from agentbase import AgentBase
from llm_setup import llm
import re
import os

def text_clean(text: str):
    match = re.search(r"```(?:jsx|javascript)?\s+(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def architect_node(state: AgentBase):
    print("---ARCHITECT---")

    spec = state["specification"]

    prompt = f"""Jesteś architektem React. Na podstawie opisu: {spec}
    Przygotuj plan komponentu:
    1. Lista wymaganych propsów.
    2. Struktura HTML (Tagi i klasy Tailwind).
    3. Logika (użycie useState/useEffect).
    Zwróć tylko plan, bez kodu."""

    response = llm.invoke(prompt)

    return{"srecification": f"PLAN: {response.content}", "iteration_count": state["iteration_count"] + 1}

def coder_node(state: AgentBase):
    print("---CODER---")

    plan = state["specification"]

    prompt = f"""Na podstawie planu: {plan}
    Napisz kompletny kod komponentu React (JSX) z Tailwind CSS. 
    Zwróć TYLKO kod, bez Markdowna (bez ```jsx)."""

    response = llm.invoke(prompt)
    clean_text = text_clean(response.content)

    return{"generated_code": clean_text}

def reviewer_node(state: AgentBase):
    print("---REVIEWER---")

    code = state["generated_code"]

    prompt = f"""Jesteś testerem QA. Sprawdź poniższy kod React:
    {code}
    
    Czy kod zawiera:
    1. Export default?
    2. Import React?
    3. Poprawne klasy Tailwind?
    
    Jeśli kod jest poprawny, napisz tylko słowo 'POZYTYWNY'. 
    Jeśli są błędy, wypisz je w punktach."""

    response = llm.invoke(prompt)

    return {'critique': [response.content]}

def saver_node(state: AgentBase):

    save_dir = 'generated_components'
    if not save_dir:
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, 'GeneratedComponent2.jsx')

    code = state["generated_code"]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)

    print(f'Plik zapisany w {file_path}')
    return {"iteration_count": state["iteration_count"]}

    

