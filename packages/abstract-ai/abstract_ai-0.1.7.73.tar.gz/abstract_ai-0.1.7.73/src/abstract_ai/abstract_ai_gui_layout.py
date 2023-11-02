from .abstract_gui_shared import *   
def get_feedback():
    layout=[[]]
    for i,title in enumerate(['abort','additional_responses','suggestions', 'notation','other']):
        if title in ['abort','additional_responses']:
            component = make_component("Input",key=text_to_key(text=title,section='feedback'),size=(None, 1))
            layout[0].append(make_component('Frame',title, layout=[[component]]))
        else:
            component = make_component("Multiline",key=text_to_key(text=title,section='feedback'),**expandable(size=(30, 5)))
            layout.append([make_component('Frame',title, layout=[[component]],**expandable(size=(None,None)))])
    return layout
def generate_tab(title,layout):
    return make_component("Tab",ensure_nested_list(layout),**expandable())
def get_instructions():
    layout = []
    sub_layout = []
    i = 0
    for instruction_key in instructions_keys:
        if instruction_key == 'instructions':
            layout.append([generate_bool_text(instruction_key,args={**expandable(size=(None,5))})])
        else:
            component = generate_bool_text(instruction_key,args={**expandable(size=(20,5))})
            if i%3==float(0) and i != 0:
                layout.append(sub_layout)
                sub_layout=[component]
            else:
                sub_layout.append(component)
    return [layout]
def get_instructions():
    layout= [[],[],[]]
    for i,instruction_key in enumerate(instructions_keys):
        component = generate_bool_text(instruction_key,args={**expandable(size=(20,5))})
        if instruction_key == 'instructions':
            layout[0].append(generate_bool_text(instruction_key,args={**expandable(size=(None,5))}))
        
        elif i<len(instructions_keys)-3:
            layout[1].append(component)
        else:
            layout[2].append(component)
    return layout
def get_total_layout():
    output_layout = make_component('Multiline',key=text_to_key(text='-RESPONSE-'),**expandable(size=(70, None)))
    output= make_component("Column",ensure_nested_list(output_layout))

    feedback = make_component("Column",ensure_nested_list(get_feedback()))
    
    output = make_component("Frame",'Response',layout=[[output,feedback]])
    prompt_tabs= get_prompt_tabs(get_instructions(),get_chunked_sections(),args={**expandable(size=(800, 800))})
    return [
        [get_progress_frame()],
        [get_output_options()],
        [get_column([[output],[prompt_tabs]]),get_column(utilities())]
        ]

