from typing import List
import untruncate_json
import os
from pathlib import Path
from llama_cpp import Llama, LlamaGrammar

PATH = Path(__file__).parent.resolve()

LLM_REPO_ID = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
LLM_FILENAME = "mistral-7b-instruct-v0.2.Q2_K.gguf" # smallest version so my laptop doesn't cry

def mistral_inst_prompt(prompt):
    return f"[INST] {prompt} [/INST]"
    

def load_llm():
    print("Loading LLM")
    llm = Llama.from_pretrained(
        repo_id=LLM_REPO_ID,
        filename=LLM_FILENAME,
        n_ctx=2048,
        n_gpu_layers=-1,
        chat_format="mistral-instruct"
    )
    
    return llm


def annotate_text(query : str): # Possibly stream this too?
    llm = load_llm()    # in practice, the llm would be loaded on startup and kept in memory
    print("LLM loaded")
    
    # load grammar
    with open(PATH / "grammar.gbnf", "r") as f:
        grammar_text = f.read()
        grammar = LlamaGrammar.from_string(grammar_text)
    
    with open(PATH / "llm_additional_system_prompt_info.txt", "r", encoding="utf-8") as f:
        extra_info = f.read()

    system_message = f"""
    You are a helpful AI that can extract information from electronic health records.
    Given an electronic health record, extract the relevant information to produce a JSON with the following fields:
    {extra_info}
    Event type must be either of Adverse_event or Potential_therapeutic_effect.
    If a annotaion field is not present, don't include it in the JSON.
    Ensure the JSON is valid and contains the correct data types.
    """
    
    
    #Annotate the text
    output = llm.create_chat_completion(
        messages=[
            {
                "role" : "user",
                "content" : system_message + '7978578_1 Response of a promethazine-induced coma to flumazenil.'
            },
            {
                "role" : "assistant",
                "content" : '{"id":"7978578_1","context":"Response of a promethazine-induced coma to flumazenil.","events":[{"type":"Adverse_event","annotations":[{"annotation":"Trigger","text":"induced"},{"annotation":"Treatment","text":"promethazine"},{"annotation":"Treatment.Drug","text":"promethazine"},{annotation":"Effect","text":"coma"}]},{"type":"Potential_therapeutic_event","annotations":[{"annotation":"Trigger","text":"Response"},{"annotation":"Treatment","text":"flumazenil"},{"annotation":"Treatment.Disorder","text":"promethazine-induced coma"},{"annotation":"Treatment.Drug","text":"flumazenil"}]}]}',
            },
            {
                "role" : "user",
                "content" : '16728538_2 Drug-induced hepatitis in an acromegalic patient during combined treatment with pegvisomant and octreotide long-acting repeatable attributed to the use of pegvisomant.'
            },
            {
                "role" : "assistant",
                "content" : '{"id":"16728538_2","context":"Drug-induced hepatitis in an acromegalic patient during combined treatment with pegvisomant and octreotide long-acting repeatable attributed to the use of pegvisomant.","events":[{"type":"Adverse_event","annotations":[{"annotation":"Trigger","text":"induced"},{"annotation":"Effect","text":"hepatitis"},{"annotation":"Treatment","text":"combined treatment with pegvisomant and octreotide long-acting repeatable"},{"annotation":"Treatment.Disorder","text":"acromegalic"},{"annotation":"Treatment.Drug","text":"pegvisomant"},{"annotation":"Treatment.Drug","text":"octreotide"},{"annotation":"Treatment.Combination.Trigger","text":"and"},{"annotation":"Treatment.Combination.Drug","text":"pegvisomant"},{"annotation":"Treatment.Combination.Drug","text":"octreotide"},{"annotation":"Subject","text":"an acromegalic patient"},{"annotation":"Subject.Disorder","text":"acromegalic"}]}]}'
            },
            {
                "role" : "user",
                "content" : query
            },
        ],
        max_tokens=4096,
        temperature=0.5,
        stop=["</s>"],
        grammar=grammar # Format outputs with a grammar
    )
    
    result = output["choices"][0]["message"]["content"].replace("\n", "").replace('\\', '')
    result = untruncate_json.complete(result)
    return result


def annotate_bulk(queries: List[str]):
    llm = load_llm()    # in practice, the llm would be loaded on startup and kept in memory
    print("LLM loaded")
    
    # load grammar
    with open(PATH / "grammar.gbnf", "r") as f:
        grammar_text = f.read()
        grammar = LlamaGrammar.from_string(grammar_text)
    
    with open(PATH / "llm_additional_system_prompt_info.txt", "r", encoding="utf-8") as f:
        extra_info = f.read()

    system_message = f"""
    You are a helpful AI that can extract information from electronic health records.
    Given an electronic health record, extract the relevant information to produce a JSON with the following fields:
    {extra_info}
    Event type must be either of Adverse_event or Potential_therapeutic_effect.
    If a annotaion field is not present, don't include it in the JSON.
    Ensure the JSON is valid and contains the correct data types.
    """
    
    results = []
    
    for id, query in enumerate(queries, start=1000):
        #Annotate the text
        output = llm.create_chat_completion(
            messages=[
                {
                    "role" : "user",
                    "content" : system_message + '7978578_1 Response of a promethazine-induced coma to flumazenil.'
                },
                {
                    "role" : "assistant",
                    "content" : '{"id":"7978578_1","context":"Response of a promethazine-induced coma to flumazenil.","events":[{"type":"Adverse_event","annotations":[{"annotation":"Trigger","text":"induced"},{"annotation":"Treatment","text":"promethazine"},{"annotation":"Treatment.Drug","text":"promethazine"},{annotation":"Effect","text":"coma"}]},{"type":"Potential_therapeutic_event","annotations":[{"annotation":"Trigger","text":"Response"},{"annotation":"Treatment","text":"flumazenil"},{"annotation":"Treatment.Disorder","text":"promethazine-induced coma"},{"annotation":"Treatment.Drug","text":"flumazenil"}]}]}',
                },
                {
                    "role" : "user",
                    "content" : '16728538_2 Drug-induced hepatitis in an acromegalic patient during combined treatment with pegvisomant and octreotide long-acting repeatable attributed to the use of pegvisomant.'
                },
                {
                    "role" : "assistant",
                    "content" : '{"id":"16728538_2","context":"Drug-induced hepatitis in an acromegalic patient during combined treatment with pegvisomant and octreotide long-acting repeatable attributed to the use of pegvisomant.","events":[{"type":"Adverse_event","annotations":[{"annotation":"Trigger","text":"induced"},{"annotation":"Effect","text":"hepatitis"},{"annotation":"Treatment","text":"combined treatment with pegvisomant and octreotide long-acting repeatable"},{"annotation":"Treatment.Disorder","text":"acromegalic"},{"annotation":"Treatment.Drug","text":"pegvisomant"},{"annotation":"Treatment.Drug","text":"octreotide"},{"annotation":"Treatment.Combination.Trigger","text":"and"},{"annotation":"Treatment.Combination.Drug","text":"pegvisomant"},{"annotation":"Treatment.Combination.Drug","text":"octreotide"},{"annotation":"Subject","text":"an acromegalic patient"},{"annotation":"Subject.Disorder","text":"acromegalic"}]}]}'
                },
                {
                    "role" : "user",
                    "content" : f"{id} {query}"
                },
            ],
            max_tokens=4096,
            temperature=0.5,
            stop=["</s>"],
            grammar=grammar # Format outputs with a grammar
        )
        output_formatted = output["choices"][0]["message"]["content"].replace("\n", "").replace('\\', '')
        output_formatted = untruncate_json.complete(output_formatted)
        results.append(output_formatted)

    return results

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
    