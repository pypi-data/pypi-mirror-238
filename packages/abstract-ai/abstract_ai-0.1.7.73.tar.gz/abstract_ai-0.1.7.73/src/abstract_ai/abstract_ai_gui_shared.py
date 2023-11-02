from abstract_gui import AbstractBrowser,text_to_key,make_component,ensure_nested_list,expandable
from . import ModelManager
prompt_tab_keys=['request','prompt Data','chunks','query','instructions']
instructions_keys = ["instructions","additional_responses","suggestions","abort","notation","generate_title","additional_instruction",]
def try_title(component):
    try:
        while isinstance(component,list):
            component = component[0]
        title = component.Title
    except:
        title=None
    return title
def generate_bool_text(title,args={}):
    if "key" not in args:
        args["key"]=text_to_key(text=title,section='text')
    return make_component("Frame",title, layout=[[make_component("Multiline",args=args)]],**expandable())
def get_tab_layout(title,layout=None):
    if not layout:
        layout = make_component("Multiline",key=text_to_key(title), **expandable())
    return make_component("Tab",title.upper(),ensure_nested_list(layout))
def get_num_list():
    num_list=[5]
    while num_list[-1] < 95:
        num_list.append(num_list[-1]+5)
    return num_list
model_manager = ModelManager()
all_models = model_manager.all_model_names
def get_tokens_by_model(model_name):
    return model_manager._get_max_tokens_by_model(model_name)
def get_response_types():
    return ['instruction', 'json', 'bash', 'text']
def roles_js():
    return {'assistant':'you are an assistant','Elaborative': 'The model provides detailed answers, expanding on the context or background of the information. E.g., "What is the capital of France?" Answer', 'Socratic': 'The model guides the user to the answer through a series of questions, encouraging them to think critically.', 'Concise': 'The model provides the shortest possible answer to a question.', 'Friendly/Conversational': 'The model interacts in a more relaxed, friendly manner, possibly using casual language or even humor.', 'Professional/Formal': 'The model adopts a formal tone, suitable for professional settings.', 'Role-Playing': 'The model assumes a specific character or role based on user instructions. E.g., "You\'re a medieval historian. Tell me about castles."', 'Teaching': 'The model provides step-by-step explanations or breakdowns, as if teaching a concept to someone unfamiliar with it.', "Debative/Devil's Advocate": 'The model takes a contrarian view to encourage debate or show alternative perspectives.', 'Creative/Brainstorming': 'The model generates creative ideas or brainstorming suggestions for a given prompt.', 'Empathetic/Supportive': 'The model offers emotional support or empathy, being careful not to provide medical or psychological advice without proper disclaimers.'}
def roles_keys():
    return list(roles_js().keys())
def content_type_list():
    return ['application/json','text/plain', 'text/html', 'text/css', 'application/javascript',  'application/xml', 'image/jpeg', 'image/png', 'image/gif', 'image/svg+xml', 'image/webp', 'audio/mpeg', 'video/mp4', 'video/webm', 'audio/ogg', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/octet-stream', 'application/zip', 'multipart/form-data', 'application/x-www-form-urlencoded', 'font/woff', 'font/woff2', 'font/ttf', 'font/otf', 'application/wasm', 'application/manifest+json', 'application/push-options+json']
def get_list_Nums(i,k):
    ls=[]
    while i>0:
        ls.append(i)
        i-=k
    return ls
### model selection
def get_endpoint_selector():
    return make_component("Frame",'Endpoint',[[make_component("Input",key='-ENDPOINT-', readonly=True, enable_events=True,disabled=True)]])
def get_model_selector():
    return make_component("Frame",'Model',[[make_component("Combo",all_models, default_value=all_models[0], key='-MODEL-', enable_events=True)]])
def get_token_display():
    return make_component("Frame",'tokens',[[make_component("Input",get_tokens_by_model(all_models[0]),key='-MAX_TOKENS-', readonly=True, enable_events=True,disabled=True,size=(5,1))]])
def get_model_selection_layout():
    return [[get_endpoint_selector()], [get_model_selector(),get_token_display()]]
def make_default_checkbox(title):
    return make_component("Checkbox",title,key=text_to_key(text=title,section='bool'),enable_events=True,default=True)
def get_tokens_layout():
    return [
        make_component("Column",get_tokens_display())
        ]
def get_tokens_display():
    return [
        get_completion_tokens(),
        get_prompt_tokens(),
        get_chunk_tokens()
    ]
def get_column(layout,args={}):
    return make_component("Column",ensure_nested_list(layout),**args)
def get_tab_group(grouped_tabs,args={}):
    return make_component("TabGroup",ensure_nested_list(grouped_tabs),**args)
### tokens display
def get_tokens_section(tokens_dict):
    layout = []
    for title,default_value in tokens_dict.items():
        frame_title = title.split(' ')[0]
        layout.append(make_component("Text",f'{title.split(" ")[-1]}:', auto_size_text=True))
        layout.append(make_component("Input",key=text_to_key(text=title), default_text=default_value,size=(10,1), readonly=True,enable_events=True))
    return [make_component("Frame",frame_title,layout=[layout])]
def get_completion_percentage_dropdown():
    return ensure_nested_list(make_component("Combo",values=get_num_list(), default_value=40, key=text_to_key(text='completion percentage'), enable_events=True))
def get_prompt_percentage_dropdown():
    return ensure_nested_list(make_component("Combo",values=get_num_list(), default_value=60, key=text_to_key(text='prompt percentage'), enable_events=True))
def get_completion_tokens():
    percentage = 4920
    return get_tokens_section({'completion tokens available':percentage,'completion tokens desired':percentage,'completion tokens used':'0'})
def get_prompt_tokens():
    percentage = 3280
    return get_tokens_section({'prompt tokens available':percentage,'prompt tokens desired':percentage,'prompt tokens used':'0'})
def get_chunk_tokens():
        percentage = 3280
        return get_tokens_section({'max chunk size':percentage,'chunk total':'0','chunk length':'0'})
def get_prompt_tabs(instructions_layout,chunks_layout,args={}):
    layout = []
    layout_specs = {"instructions":instructions_layout,"chunks":chunks_layout}
    for prompt_tab_key in prompt_tab_keys:
        layout.append(get_tab_layout(prompt_tab_key,layout=layout_specs.get(prompt_tab_key)))
    return get_tab_group(layout,args=args)
def get_settings():
    num_list=[5]
    while num_list[-1] < 95:
        num_list.append(num_list[-1]+5)
    response_type = make_component("Combo",get_response_types(), default_value=get_response_types()[0], key='-RESPONSETYPE-', readonly=True)
    completion_percentage=ensure_nested_list(make_component("Combo",values=num_list, default_value=60, key=text_to_key(text='completion percentage'), enable_events=True))
    prompt_percentage=ensure_nested_list(make_component("Combo",values=num_list, default_value=40, key=text_to_key(text='prompt percentage'), enable_events=True))
    env_input=ensure_nested_list(make_component("Input",key=text_to_key(text='api env'), enable_events=True))
    role_combo=ensure_nested_list(make_component("Combo",values=roles_keys(), default_value=roles_keys()[0], key=text_to_key(text='role'), enable_events=True))
    title_bool=make_component("Checkbox",'Title', key=text_to_key("title bool",section="bool"), auto_size_text=True, enable_events=True)
    collate_responses=make_component("Checkbox",'Collate Responses', key=text_to_key("collate responses",section="bool"), enable_events=True)
    title_input=make_component("input",key=text_to_key("title text"), enable_events=True)
    header_input=ensure_nested_list(make_component("input",key=text_to_key("header"), enable_events=True))
    api_key=ensure_nested_list(make_component("Input",key=text_to_key(text='api key'), enable_events=True))
    default_checkboxes=([[make_default_checkbox('generate title'),make_default_checkbox('additional Responses'),make_default_checkbox('Abort')],[make_default_checkbox('additional instruction'),make_default_checkbox('notation'),make_default_checkbox('suggestions')]])
    file_options = ensure_nested_list([[make_component("Checkbox",'auto chunk title',default=True,key=text_to_key('auto chunk title'), enable_events=True),make_component("Checkbox",'reuse chunk data',default=False,key='-REUSE_CHUNK-'),make_component("Checkbox",'append',default=True,key='-APPEND_CHUNK-'),make_component("Checkbox",'all directory',default=True,key='-SCAN_MODE_ALL-')]])
    test_options= ensure_nested_list([[make_component("Checkbox",'Test Run',default=False,key=text_to_key(text='test run'), enable_events=True),make_component("Checkbox",'Test Files',default=False,key=text_to_key(text='test files'), enable_events=True),make_component("Input",key=text_to_key(text='test file'), enable_events=True),make_component("FileBrowse","Files", enable_events=True, key=text_to_key(text='test browse'))]])
    return [
            [make_component("Frame",'comp %',layout=completion_percentage),
             make_component("Frame",'prompt %',layout=prompt_percentage),
             [make_component("Frame",'api key',layout=api_key)],
             [make_component("Frame",'header',layout=header_input)],
             make_component("Frame",'Title',layout=ensure_nested_list([title_bool,title_input]))],[make_component("Frame",'api env key',layout=env_input)],
             [make_component("Frame",'role',layout=role_combo),make_component("Frame","Response Type",[[response_type]])],
            get_tokens_layout(),
            [make_component("Frame","responses",ensure_nested_list(collate_responses))],
            [make_component("Frame","model select",ensure_nested_list(get_model_selection_layout()))],
            [make_component("Frame","enable instruction", layout=default_checkboxes)],
            [make_component("Frame","Test Tools", layout=test_options)],
            [make_component("Frame","file options", layout=file_options)]
        ]
def get_chunked_sections():
    return [
        [make_component("Button",button_text="CREATE CHUNK",key="-CREATE_CHUNK-",auto_size_text=True, enable_events=True),
         make_component("Checkbox",'custom chunk',default=False,key="-CUSTOM_CHUNK-",auto_size_text=True, enable_events=True)],
        [make_component("Push"),make_component("Button",button_text="<-",key=text_to_key("chunk text back"),enable_events=True),
         make_component("input",default_text='0',key=text_to_key("chunk text number"),size=(4,1)),
         make_component("Button",button_text="->",key=text_to_key("chunk text forward"),enable_events=True),make_component("Push")],
        [make_component("Frame",'chunk sectioned data', layout=[[make_component("Multiline",key=text_to_key('chunk sectioned data'),**expandable())]],**expandable())]]
            
def utilities():
    layout = []
    layout.append(make_component("Tab",'SETTINGS', ensure_nested_list(make_component("Column",get_settings(),**expandable(scroll_vertical=True,scroll_horizontal=True))),**expandable(scroll_horizontal=True))),
    layout.append(make_component("Tab",'RESPONSES', abstract_browser_layout(section='responses'),key=text_to_key(text='response tab'),**expandable(size=(50, 100)))),
    layout.append(make_component("Tab",'Files', abstract_browser_layout(section='files'),**expandable(size=(800, 800)),key=text_to_key(text='file tab'))),
    layout.append(make_component("Tab",'urls', get_urls(),**expandable(size=(800, 800)),key=text_to_key(text='url tab')))
    return  make_component("TabGroup",ensure_nested_list(layout),**expandable(size=(800, 800)))
####submit options
def get_output_options():
    return [
        [
         make_component("Button",button_text="SUBMIT QUERY",key="-SUBMIT_QUERY-", disabled=False,enable_evete=True),
         make_component("Button",button_text="CLEAR INPUT",key='-CLEAR_INPUT-', disabled=False,enable_evete=True),
         make_component("Button",button_text="COPY RESPONSE",key='-COPY_RESPONSE-', disabled=False,enable_evete=True),
         make_component("Button",button_text="PASTE INPUT",key='-PASTE_INPUT-', disabled=False,enable_evete=True),
         make_component("Button",button_text="CLEAR CHUNKS",key='-CLEAR_CHUNKS-', disabled=False,enable_evete=True),
         make_component("Button",button_text="UNDO CHUNKS",key='-UNDO_CHUNKS-', disabled=False,enable_evete=True),
         make_component("Button",button_text="REDO CHUNKS",key='-REDO_CHUNKS-', disabled=False,enable_evete=True),
         make_component("Button",button_text="GEN README",key='-GENERATE_README-', disabled=False,enable_evete=True)]
    ]
def get_urls():
    return [
        [make_component("Input",key='-URL-', enable_events=True), make_component("Button",'Add URL',key='-ADD_URL-',enable_events=True), make_component("Listbox",values=[], key='-URL_LIST-', size=(70, 6))],
        [make_component("Button",'GET SOUP',key=text_to_key(text='get soup'),enable_events=True),
         make_component("Button",'GET SOURCE',key=text_to_key(text='get source code'),enable_events=True),
         make_component("Button",'CHUNK_DATA',key=text_to_key(text='add url to chunk'),enable_events=True),
         make_component("Frame",'chunk title',layout=[[make_component("Input",key=text_to_key(text='chunk title',section='url'),size=(20,1))]])],
        [make_component("Multiline",key=text_to_key(text='url text'),**expandable())],
    ]
def abstract_browser_layout(section=None):
    extra_buttons = [make_component("Button",'CHUNK_DATA',key=text_to_key(text='add file to chunk',section=section),enable_events=True),
                     make_component("Frame",'chunk title',layout=[[make_component("Input",key=text_to_key(text='chunk title',section=section),size=(20,1))]])]
    return AbstractBrowser().get_scan_browser_layout(section=section,extra_buttons=extra_buttons)+[[make_component("Multiline",key=text_to_key(text='file text',section=section),**expandable())]]
def get_progress_frame():
    return [
        [
            make_component("Frame", 'PROGRESS', layout=[
                [
                    make_component("InputText", 'Not Sending', key='-PROGRESS_TEXT-', background_color="light blue", auto_size_text=True, size=(10, 20)),
                    make_component("ProgressBar", 100, orientation='h', size=(10, 20), key='-PROGRESS-'),
                    make_component("Input", default_text='0', key=text_to_key("query count"), size=(10, 20), disabled=True, enable_events=True)
                ]
            ]),
            make_component("Frame", 'query title', layout=[
                [
                    make_component("Input", default_text="title of prompt", size=(30, 1), key=text_to_key('title input'))
                ]
            ]),
            make_component('Frame', "response nav", [
                [
                    make_component("Button", button_text="<-", key=text_to_key("response text back"), enable_events=True),
                    make_component("input", default_text='0', key=text_to_key("response text number"), size=(4, 1)),
                    make_component("Button", button_text="->", key=text_to_key("response text forward"), enable_events=True)
                ]
            ])
        ]
    ]
