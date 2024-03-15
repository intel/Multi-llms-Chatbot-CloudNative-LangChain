const connection = require('node-fetch');

class ActionProvider {
  constructor(createChatBotMessage, setState,createClientMessage,state) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setState;
    this.state = state;
  }
  
  // check conditions her 
  chatToModelTrigger =  async (message) => {
    
    console.log(this.state.rag_mode);
    if (this.state.rag_mode){
      this.chatToRag(message);
    }else if (this.state.external_mode){
      this.chatToExternal(message);
    }else if (this.state.local_mode){
      this.chatToLocal(message);
    }else if (this.state.opt_model){
      this.chatToLlamaOptLocal(message);
    } else {
      // If none of the conditions are met, display a message
      const message = this.createChatBotMessage("Please specify the type of model you want to talk to.");
      this.addMessageToState(message);
    }

  };
 
  chatToExternal= async (message) => {
    try {
      console.log('Message sent to External API');  
      // Message sent to API created by Langchain API
      const response = await connection('http://localhost:8000/api_openai', {
        method: 'POST',
        headers: {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: message,
          config: {},
          kwargs: {}
      }),
    });

      if (!response.ok) {
        throw new Error('Failed to send message to the API');
      }

      const result = await response.text();
      console.log('Message sent successfully:', result);

      const chatbotMessage = this.createChatBotMessage(result);
      this.addMessageToState(chatbotMessage);
    } catch (error) {
      console.error('Error in chatToExternal:', error.message);
    }
  };
  chatToLlamaOptLocal = async (message) => {
    try {
      console.log('Message sent to local LLaMa2');  
      const response = await fetch('http://localhost:8000/api_local_llama_optim', {
        method: 'POST',
        headers: {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: message,
          config: {},
          kwargs: {}
      }),
    });

      if (!response.ok) {
        throw new Error('Failed to send message to the API');
      }

      const result = await response.text();
      console.log('Message sent successfully:', result);

      const chatbotMessage = this.createChatBotMessage(result);
      this.addMessageToState(chatbotMessage);
    } catch (error) {
      console.error('Error in chatToLlamaOptLocal:', error.message);
    }
  };
  
  chatToLocal = async (message) => {
    try {
      console.log('Message sent to local LLaMa2');  
      const response = await fetch('http://localhost:8000/api_local_llama_non', {
        method: 'POST',
        headers: {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: message,
          config: {},
          kwargs: {}
      }),
    });

      if (!response.ok) {
        throw new Error('Failed to send message to the API');
      }

      const result = await response.text();
      console.log('Message sent successfully:', result);

      const chatbotMessage = this.createChatBotMessage(result);
      this.addMessageToState(chatbotMessage);
    } catch (error) {
      console.error('Error in chatToLocal:', error.message);
    }
  };

  setExternalState = () => {
    const message = this.createChatBotMessage("Great! Please make your question to the External API (OpenAI");
      this.addMessageToState(message);

    this.setState((prev) => ({
      ...prev,
      external_mode: true,
      
    }));
  };

  setOptimizedState = () => {
    const message = this.createChatBotMessage("Great! Please add your question to the Local Optimized LLaMa2 model)");
      this.addMessageToState(message);

    this.setState((prev) => ({
      ...prev,
      opt_model: true,
      
    }));
  };

  setLocalState = () => {
    const message = this.createChatBotMessage("Great! Please add your question to the Local LLaMa2 model");
      this.addMessageToState(message);

    this.setState((prev) => ({
      ...prev,
      local_mode: true,
      
    }));
  };

  startAgain = () => {
    const message = this.createChatBotMessage("Great! Let's start again! Let me know to which model you want to talk.");
      this.addMessageToState(message);

    this.setState((prev) => ({
      ...prev,
      external_mode: false,
      
    }));
    this.setState((prev) => ({
      ...prev,
      local_mode: false,
      
    }));
    this.setState((prev) => ({
      ...prev,
      rag_mode: false,
      
    }));
    this.setState((prev) => ({
      ...prev,
      opt_model: false,
    }));
    
  };

  addMessageToState = (message) => {
    this.setState((prevState) => ({
      ...prevState,
      messages: [...prevState.messages, message],
    }));
  };
}

export default ActionProvider;
  
  
  
