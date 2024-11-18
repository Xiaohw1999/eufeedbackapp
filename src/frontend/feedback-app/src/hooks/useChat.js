import useVoiceRecognition from "./useVoiceRecognition";
import useInput from "./useInput";
import useChatMessages from "./useChatMessages";

const useChat = () => {
  const { inputValue, setInputValue, textareaRef, handleInputChange } = useInput("");
  const { isListening, handleVoiceInput } = useVoiceRecognition(setInputValue);
  const { messages, startedChat, handleSend, handleSuggestionClick, loading, error, sources, scores, terminateOutput } = useChatMessages();

  const sendMessage = (inputValue, selectedTopic, selectedUserType, selectedChain, selectedModel, searchOptions) => {
    handleSend(inputValue, selectedTopic, selectedUserType, selectedChain, selectedModel, searchOptions);
    setInputValue("");
  };

  return {
    inputValue,
    setInputValue,
    isListening,
    handleVoiceInput,
    messages,
    startedChat,
    textareaRef,
    handleInputChange,
    handleSend: sendMessage,
    handleSuggestionClick,
    loading,
    error,
    sources,
    scores,
    terminateOutput
  };
};

export default useChat;
