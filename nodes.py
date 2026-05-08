from langgraph.graph import END

from agentbase import AgentBase
from llm_setup import llm
import re
import os
from assembler import AssemblerBase

def text_clean(text: str):
    match = re.search(r"```(?:jsx|javascript|css)?\s+(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def route_after_saver(state: AssemblerBase):

    last_file_name = state['project_structure'][-1]['name']
    print(f'[DEBUG] Last saved file {last_file_name}')

    if 'App' in last_file_name:
        return "end"
    else:
        return "continue" 


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

    return{"specification": f"PLAN: {response.content}", "iteration_count": state["iteration_count"] + 1}

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

    file_path = os.path.join(save_dir, 'GeneratedComponent4.jsx')

    code = state["generated_code"]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)

    print(f'Plik zapisany w {file_path}')
    return {"iteration_count": state["iteration_count"]}

    
def assembler_node(state: AssemblerBase):
    print("---Planowanie struktury projektu")
    goal = state['project_goal']

    prompt = f"""Jesteś Project Managerem IT. Użytkownik chce projekt: {goal}.
    1. Rozbij projekt na 3-4 komponenty React (.jsx).
    2. Na końcu listy ZAWSZE dodaj dwa pliki: index.css
    
    Zwróć TYLKO nazwy plików oddzielone przecinkami.
    Przykład: Header.jsx, Hero.jsx, Footer.jsx, index.css"""

    response = llm.invoke(prompt)

    to_create = [f.strip() for f in response.content.split(',')]

    print(f'PLAN: {to_create}')


    return {
        "files_to_create": to_create,
        'current_file_idx': 0,
        'iteration_count': 0
    }


def logic_node(state: AssemblerBase):
    files_to_create = state['files_to_create']
    current_idx = state['current_file_idx']

    
    file = files_to_create[current_idx]

    print(f'---PRACUJE NAD PLIKIEM: {file}')

    return {
        'current_file': file
    }

def component_architekt_node(state: AssemblerBase):
    file = state['current_file']

    goal = state['project_goal']

    if file.endswith('.css'):
        prompt = f"KRYTYCZNE: Nie twórz własnych klas CSS w pliku index.css (np. .navbar). Używaj wyłącznie czystych klas Tailwind CSS bezpośrednio w plikach .jsx. Plik index.css powinien zawierać tylko podstawowe dyrektywy @tailwind. Jesteś architektem CSS. Zaplanuj kolory i style dla pliku {file} dla projektu: {goal}. Użyj Tailwind CSS (@tailwind base itp.)."
    else:
        prompt = f"KRYTYCZNE: Każdy komponent musi być atomowy. Sidebar.jsx powinien zawierać WYŁĄCZNIE nawigację boczną. Nie wrzucaj logiki TaskBoard ani ActivityFeed do pliku Sidebar.Jesteś architektem React. Zaplanuj strukturę dla komponentu {file} dla projektu: {goal}..."


    response = llm.invoke(prompt)

    return {
        'specification': text_clean(response.content)
    }

def assembler_coder_node(state: AssemblerBase):
    spec = state['specification']
    file = state['current_file']

    if file.endswith('.css'):
        prompt = f"Napisz czysty kod CSS dla pliku {file} na podstawie tej specyfikacji: {spec}. Użyj dyrektyw @tailwind base; @tailwind components; @tailwind utilities;"
    else:        
        prompt = f"""
        KRYTYCZNE: Budujemy projekt w czystym Vite + React, a NIE w Next.js. NIGDY nie używaj bibliotek takich jak @next/font, next/link czy next/image. 
        Jeśli chcesz użyć czcionki Inter, załóż, że jest ona skonfigurowana globalnie w CSS lub użyj standardowej klasy Tailwind font-sans.
        KRYTYCZNE: Nie twórz własnych klas typu 'glass-card'. Używaj wyłącznie standardowych klas Tailwind CSS (np. bg-white/10, backdrop-blur itp.), 
        KRYTYCZNE: Jeśli tworzysz plik main.jsx dla Vite, używaj wyłącznie React 18+ syntax.Importuj ReactDOM z 'react-dom/client'.Używaj ReactDOM.createRoot
        KRYTYCZNE: Nie twórz własnych klas CSS w pliku index.css (np. .navbar). Używaj wyłącznie czystych klas Tailwind CSS bezpośrednio w plikach .jsx. Plik index.css powinien zawierać tylko podstawowe dyrektywy @tailwind.”
        (document.getElementById('root')).render(...) zamiast starego ReactDOM.render.
        aby uzyskać pożądany efekt wizualny.
        Jesteś programistą React. Napisz kod dla {file} 
        na podstawie: {spec}.
        Użyj Tailwind CSS do stylizacji (kolory, spacing, layout). 
        Zwróć tylko kod."""

    response = llm.invoke(prompt)

    return{
        'project_structure': [{'name': file, 'code': text_clean(response.content)}]
    }

def increment_node(state: AssemblerBase):
    return{
        'current_file_idx': state['current_file_idx'] + 1
    }

def should_finish(state: AssemblerBase):
    current_file_idx = state['current_file_idx']
    total = len(state['files_to_create'])
    files = state['files_to_create']

    if current_file_idx < total:
        return 'selector'
    else:
        return 'final_assemble'
    

def final_assembler_node(state: AssemblerBase):
    print('---Skladamy projek na podstawie komponentow---')

    full_context = "\n".join([f"Plik: {f['name']}\nKod:\n{f['code']}" for f in state['project_structure']])


    

    goal = state['project_goal']

    prompt = f"""
    KRYTYCZNE: Jeśli w kodzie App.jsx używasz komponentu <Icon>, MUSISZ dodać na górze import: import { 'Icon' } from '@iconify/react';. 
    KRYTYCZNE: Jeśli komponenty, które importujesz, wymagają propsów (jak sidebarItems czy tasks), MUSISZ zdefiniować 
    przykładowe dane (mock data) wewnątrz App.jsx przed ich przekazaniem.
    Nigdy nie używaj zmiennych, których wcześniej nie zdefiniowałeś.
    Zawsze sprawdzaj, czy wszystkie użyte komponenty są zaimportowane
    Jesteś Senior React Developerem. 
    Poniżej znajduje się kod komponentów, które właśnie stworzyliśmy dla projektu: {goal}.
    
    {full_context}
    
    Twoje zadanie:
    Napisz plik App.jsx, który:
    1. Importuje te komponenty.
    2. Układa je w logiczną strukturę strony.
    3. Przekazuje im POPRAWNE propsy (sprawdź w kodzie powyżej, jakich propsów oczekują!).
    4. Dopasuj style Tailwind
    
    Zwróć TYLKO kod pliku App.jsx."""

    response = llm.invoke(prompt)

    return {
        'project_structure': [{"name": "App.jsx", "code": text_clean(response.content)}]
    }

def saver(state: AssemblerBase):

    file = state['project_structure'][-1]
    name = file['name']
    code = file['code']

    root_dir = 'project'
    src_folder = os.path.join(root_dir, 'src')

    os.makedirs(src_folder, exist_ok=True)

    file_path = os.path.join(src_folder, name)
    with open(file_path, 'w' ,encoding='utf-8') as f:
        f.write(code)

    if name == "App.jsx":

        main_code = """import React from 'react';
        import ReactDOM from 'react-dom/client';
        import App from './App';
        import './index.css';

        ReactDOM.createRoot(document.getElementById('root')).render(
            <React.StrictMode>
                <App />
            </React.StrictMode>
        );"""

        with open(os.path.join(src_folder, 'main.jsx'),'w', encoding='utf-8') as f:
            f.write(main_code)

    return state


    