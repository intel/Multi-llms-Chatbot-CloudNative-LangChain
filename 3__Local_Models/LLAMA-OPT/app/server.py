from fastapi import FastAPI
from langchain.prompts import PromptTemplate 
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from app.llama2 import llm_pipeline

app = FastAPI()

# Set up CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the specific origin of your frontend in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
template = """Use the following pieces of information to answer the user's question. Explaining the answer
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Question: {question}

Only return the helpful answer below and nothing else. Give an answer in 1000 characteres at maximum please
Helpful answer:
"""

prompt = PromptTemplate.from_template(template)
print("model LOADED)")
@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

add_routes(app, 
           prompt|llm_pipeline,
           path='/chain_llama_optim')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
