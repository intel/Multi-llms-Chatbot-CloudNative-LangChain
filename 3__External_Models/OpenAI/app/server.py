from fastapi import FastAPI
from fastapi.responses import RedirectResponse
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain.prompts import PromptTemplate

app = FastAPI()
# Set up CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the specific origin of your frontend in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
template = """You are a very smart and educated assistant to guide the user to understand the concepts. Please Explaining the answer
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Question: {question}

Only return the helpful answer below and nothing else. Give an answer in 1000 characteres at maximum please
Helpful answer:
"""

prompt = PromptTemplate.from_template(template) 

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


#Open AI key stored on a File server or it can be saved on a config map
f = open('/fs_mounted/Models/openai_key.txt')

# Read the contents of the file into a variable
OPENAI_KEY = f.read()

model = ChatOpenAI(openai_api_key=OPENAI_KEY)

add_routes(
    app,
    prompt|model,
    path="/chain_api_openai",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=4000)
