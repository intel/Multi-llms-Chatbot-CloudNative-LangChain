from transformers import pipeline,LlamaForCausalLM, LlamaTokenizer
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

model_path="/fs_mounted/Models/llama-2-7b-chat-hf"
local_model =  LlamaForCausalLM.from_pretrained(model_path, return_dict=True, trust_remote_code=True)
local_tokenizer = LlamaTokenizer.from_pretrained(model_path)

pipe= pipeline(task="text-generation", model=local_model, tokenizer=local_tokenizer, 
                         trust_remote_code=True, max_new_tokens=100, 
                         repetition_penalty=1.1, model_kwargs={"max_length": 1200, "temperature": 0.01})  

#Pipeline to be consumed by Langserve API
llm_pipeline = HuggingFacePipeline(pipeline=pipe)

