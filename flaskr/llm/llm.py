from llama_cpp import Llama, LogitsProcessorList, LlamaGrammar
from lmformatenforcer import JsonSchemaParser, CharacterLevelParser
from lmformatenforcer.integrations.transformers import build_transformers_prefix_allowed_tokens_fn
from lmformatenforcer.integrations.llamacpp import build_llamacpp_logits_processor, build_token_enforcer_tokenizer_data
from .schema import Record

LLM_REPO_ID = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
LLM_FILENAME = "mistral-7b-instruct-v0.2.Q2_K.gguf" # smallest version so my laptop doesn't cry

def mistral_inst_prompt(prompt):
    return f"[INST] {prompt} [/INST]"
    

def load_llm():
    print("Loading LLM")
    llm = Llama.from_pretrained(
        repo_id=LLM_REPO_ID,
        filename=LLM_FILENAME,
        n_ctx=4096,
        n_gpu_layers=-1,
    )
    
    return llm


def annotate_text(query : str): # Possibly stream this too?
    llm = load_llm()    # in practice, the llm would be loaded on startup and kept in memory
    print("LLM loaded")
    
    # Format enforcer
    tokenizer_data = build_token_enforcer_tokenizer_data(llm)
    parser = JsonSchemaParser(Record.model_json_schema())
    logits_processors = LogitsProcessorList([build_llamacpp_logits_processor(tokenizer_data, parser)])
    
    # load grammar
    with open("flaskr/llm/grammar.gbnf", "r") as f:
        grammar_text = f.read()
        grammar = LlamaGrammar.from_string(grammar_text)
    
    extra_info = ""
    with open("flaskr/llm/llm_additional_system_prompt_info.txt", "r", encoding="utf-8") as f:
        extra_info = f.read()
    
    # Removed schema from prompt {str(Record.schema_json())}
    system_message = f"""
You are a helpful AI that can extract information from electronic health records.
Given an electronic health record, extract the relevant information to produce a JSON of the following schema:

{extra_info}
Start is the starting index of where that annotation appears within the text.
Event type must be either of Adverse_event or Potential_therapeutic_effect.
If an optional field is not present, it should be entirely omitted from the JSON. Required fields must not be empty.
Ensure the JSON is valid and contains the correct data types.
"""
    
    
    # Annotate the text
    output = llm.create_chat_completion(
        messages=[
            {
                "role" : "user",
                "content" : system_message + '12962465_2 Gynaecomastia is a rarely reported adverse drug reaction due to isoniazid therapy.'
            },
            {
                "role" : "assistant",
                "content" : "{'id': '12962465_2', 'context': 'Gynaecomastia is a rarely reported adverse drug reaction due to isoniazid therapy.', 'is_mult_event': False, 'annotations': [{'events': [{'event_id': 'E1', 'event_type': 'Adverse_event', 'Trigger': {'text': [['adverse drug reaction']], 'start': [[35]], 'entity_id': ['T4']}, 'Treatment': {'text': [['isoniazid therapy']], 'start': [[64]], 'entity_id': ['T3'], 'Drug': {'text': [['isoniazid']], 'start': [[64]], 'entity_id': ['T6']}, 'Effect': {'text': [['Gynaecomastia']], 'start': [[0]], 'entity_id': ['T5']}}]}]}"
            },
            {
                "role" : "user",
                "content" : '7986915_2 We describe a patient with a liver abscess due to Entamoeba histolytica, in whom metronidazole therapy (total dose, 21 g over 14 days) was complicated by reversible deafness, tinnitus, and ataxia and who relapsed 5 months later with a splenic abscess.'
                
            },
            {
                "role" : "assistant",
                "content" : '{"id": "7986915_2", "context": "We describe a patient with a liver abscess due to Entamoeba histolytica, in whom metronidazole therapy (total dose, 21 g over 14 days) was complicated by reversible deafness, tinnitus, and ataxia and who relapsed 5 months later with a splenic abscess.", "is_mult_event": false, "annotations": [{"events": [{"event_id": "E1", "event_type": "Adverse_event", "Trigger": {"text": [["complicated"]], "start": [[139]], "entity_id": ["T13"]}, "Subject": {"text": [["a patient with a liver abscess due to Entamoeba histolytica"]], "start": [[12]], "entity_id": ["T11"]}, "Treatment": {"text": [["metronidazole therapy (total dose, 21 g over 14 days)"]], "start": [[81]], "entity_id": ["T12"], "Drug": {"text": [["metronidazole"]], "start": [[81]], "entity_id": ["T17"]}, "Dosage": {"text": [["21 g"]], "start": [[116]], "entity_id": ["T18"]}, "Duration": {"text": [["14 days"]], "start": [[126]], "entity_id": ["T19"]}, "Disorder": {"text": [["liver abscess"], ["Entamoeba histolytica"]], "start": [[29], [50]], "entity_id": ["T20", "T21"]}}, "Effect": {"text": [["reversible deafness, tinnitus, and ataxia and who relapsed 5 months later with a splenic abscess"]], "start": [[154]], "entity_id": ["T14"]}}]}]}'
            },
            {
                "role" : "user",
                "content" : query
            },
        ],
        max_tokens=4096,
        temperature=0.5,
        stop=["</s>"],
        # response_format={ # Using built-in llama cpp response format is not strict and introduces fields that are not in the schema
        #     "type": "json_object",
        #     "schema" : Record.schema_json(),
        # },
        # logits_processor=logits_processors  # Format enforcer
        grammar=grammar # Try format outputs with a grammar
    )
    
    print(output)
    return output["choices"][0]["message"]["content"]


def chat_with_llm(prompt):
    llm = load_llm()
    
    return llm.create_chat_completion( # Non-streaming
        messages=[
            {
                "role" : "user",
                "content" : "<s>" + mistral_inst_prompt(prompt)
            },
        ],
        max_tokens=4096,
        temperature=0.5,
        stop=["</s>"],
    )["choices"][0]["message"]["content"]
    
    # Streaming version
    # output = llm.create_chat_completion(
    #     messages=[
    #         {
    #             "role" : "user",
    #             "content" : prompt
    #         },
    #     ],
    #     max_tokens=4096,
    #     temperature=0.5,
    #     stop=["</s>"],
    #     stream=True,
    # )
    # for chunk in output: # https://github.com/abetlen/llama-cpp-python/discussions/319
    #     delta = chunk['choices'][0]['delta']
    #     if 'role' in delta:
    #         print(delta['role'], end=': ')
    #     elif 'content' in delta:
    #         print(delta['content'], end='')
            
    # figure out how to stream the response back to the user
