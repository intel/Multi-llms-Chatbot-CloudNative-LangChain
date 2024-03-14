import React from "react";
import { createChatBotMessage } from "react-chatbot-kit";
import Options from "../components/Options/Options";

const config = {
  botName: "LangChain in Kubernetes DEMO ",
  initialMessages: [createChatBotMessage(`Hello, I'm your assistant. Please let me know what you would like to to do:`,{
    widget:"Options"
  }),
  ],
  state: {
    rag_mode:false,
    opt_mode:false,
    external_mode:false,
    local_mode:false
  },
  widgets: [
    {
      widgetName : "Options",
      widgetFunc: (props) => <Options {...props} />,
    }
  ],  
};

export default config;