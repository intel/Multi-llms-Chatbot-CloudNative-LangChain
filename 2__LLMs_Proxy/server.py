from fastapi import FastAPI,HTTPException
from langserve import RemoteRunnable
from langchain.prompts.chat import ChatPromptTemplate
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Header
import kubernetes
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import config


def kubernetes_ipv4_address_for_service(service_name, namespace='default'):
    # Load the incluster configuration
    config.load_incluster_config()

    with kubernetes.client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = kubernetes.client.CoreV1Api(api_client)

        try:
            # Retrieve the service information
            service_info = api_instance.read_namespaced_service(name=service_name, namespace=namespace)
        except ApiException as e:
            raise Exception(f"Error reading service information: {e}")

        service_cluster_ip = service_info.spec.cluster_ip

        return service_cluster_ip

# Get services ip
openai_svc = kubernetes_ipv4_address_for_service("openai-service")
llama_non_svc = kubernetes_ipv4_address_for_service("llama7b-non-optimized-service")
llama_optim_svc = kubernetes_ipv4_address_for_service("llama7b-optimized-service")

class Data(BaseModel):
    question: str

app = FastAPI()

# Allow all origins with necessary methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],  # Add comma here
    allow_headers=["*"],  # Add comma here
    allow_credentials=False,
)
openai_llm = RemoteRunnable("http://"+openai_svc+":80/chain_api_openai").with_types(input_type=str)
llama_chain = RemoteRunnable("http://"+llama_non_svc+":80/chain_llama_non").with_types(input_type=str)
llama_optim_chain = RemoteRunnable("http://"+llama_optim_svc+":80/chain_llama_optim").with_types(input_type=str)

@app.post("/api_local_llama_optim")
async def process_text_data(question: Data,user_agent: str = Header(None)):
    try:
        user_question= question.question

        result=llama_optim_chain.invoke({"question": user_question})
        
        return result
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        raise HTTPException(stacdus_code=500, detail=error_msg)
    
@app.post("/api_local_llama_non")
async def process_text_data(question: Data,user_agent: str = Header(None)):
    try:
        user_question= question.question

        result=llama_chain.invoke({"question": user_question})
        
        return result
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    
@app.post("/api_openai")
async def process_text_data(question: Data,user_agent: str = Header(None)):
    try:
        #user_question= str(question.question)
        
        #prompt = ChatPromptTemplate.from_messages(
        #    [
        #        (
        #            "system",
        #           "You are a highly educated person who loves to use big words. "
        #            + "You are also concise. Never answer in more than three sentences.",
        #        ),
        #        ("human", user_question),
        #    ]       
        #).format_messages()     
        
        user_question= question.question

        result=openai_llm.invoke({"question": user_question})
                # Pass the extracted question
        #result=openai_llm.invoke(prompt)
        
        return result.content
    
    except Exception as e:
        print("Entering ERROR block...")
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


if __name__=='__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000) # nosec B104
