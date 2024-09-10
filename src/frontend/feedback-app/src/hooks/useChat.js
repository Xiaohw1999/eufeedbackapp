import useVoiceRecognition from "./useVoiceRecognition";
import useInput from "./useInput";
import useChatMessages from "./useChatMessages";

const useChat = () => {
  const { inputValue, setInputValue, textareaRef, handleInputChange } = useInput("");
  const { isListening, handleVoiceInput } = useVoiceRecognition(setInputValue);
  const { messages, startedChat, handleSend, handleSuggestionClick, loading, error, sources } = useChatMessages();

  return {
    inputValue,
    setInputValue,
    isListening,
    handleVoiceInput,
    messages,
    startedChat,
    textareaRef,
    handleInputChange,
    handleSend: (inputValue, selectedTopic, selectedChain, selectedModel, selectedOptions) => 
      handleSend(inputValue, selectedTopic, selectedChain, selectedModel, selectedOptions, setInputValue),
    handleSuggestionClick,
    loading,
    error,
    sources
  };
};

export default useChat;
