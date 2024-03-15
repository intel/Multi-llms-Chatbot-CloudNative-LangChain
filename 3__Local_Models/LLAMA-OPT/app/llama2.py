from transformers import pipeline, LlamaTokenizer
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from intel_extension_for_transformers.transformers import AutoModelForCausalLM
model_path = "/fs_mounted/Models/Llama-7b-hf-OPTIM"
local_model = AutoModelForCausalLM.from_pretrained(
    model_path,
    use_neural_speed=False,
)
local_tokenizer = LlamaTokenizer.from_pretrained(model_path)

pipe= pipeline(task="text-generation", model=local_model, tokenizer=local_tokenizer,
                         trust_remote_code=True, max_new_tokens=100,
                         repetition_penalty=1.1, model_kwargs={"max_length": 1200, "temperature": 0.01})

#Pipeline to be consumed by Langserve API
llm_pipeline = HuggingFacePipeline(pipeline=pipe)