class MessageParser {
  constructor(actionProvider) {
    this.actionProvider = actionProvider;
  }

  parse(message) {
    console.log(message);
    const lowercase = message.toLowerCase();

    if (lowercase.includes("optimized")) {
      this.actionProvider.setOptimizedState();
    } else if (lowercase.includes("external")) {
      this.actionProvider.setExternalState();
    } else if (lowercase.includes("start")) {
      this.actionProvider.startAgain();
    } else if (lowercase.includes("local")) {
      this.actionProvider.setLocalState();
        
    } else {
      this.actionProvider.chatToModelTrigger(lowercase);
    }
  }
}

export default MessageParser;

