import React from "react";

import "./Options.css";

const Options = (props) => {
  const options = [
    {
      text: "Use Local LLaMa2 (Non optimized)",
      handler: props.actionProvider.setLocalState,
      id: 1,
    },
    
    { text: "Use Local LLaMa2 (Optimized)", 
      handler: props.actionProvider.setOptimizedState, 
      id: 2 
    },

    { text: "Use external API", handler: props.actionProvider.setExternalState , id: 3 },
  ];

  const buttonsMarkup = options.map((option) => (
    <button key={option.id} onClick={option.handler} className="option-button">
      {option.text}
    </button>
  ));

  return <div className="options-container">{buttonsMarkup}</div>;
};

export default Options;