import { useState } from "react";
import axios from "axios";

const useChatMessages = () => {
  const [messages, setMessages] = useState([]);
  const [startedChat, setStartedChat] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sources, setSources] = useState([]);
  const [scores, setScores] = useState([]);

  const handleSend = async (inputValue, selectedTopic, selectedUserType, selectedChain, selectedModel, searchOptions) => {
    if (inputValue.trim() !== "") {
      setStartedChat(true);
      const newMessage = { type: "user", text: inputValue.trim() };
      setMessages(prevMessages => [...prevMessages, newMessage]);

      setLoading(true);
      setError(null);

      try {
        // send inputValue to backend
        const res = await axios.post("https://eej22ko8bc.execute-api.eu-north-1.amazonaws.com/newstage/query", {
          query: inputValue.trim(),
          topic: selectedTopic, // topic
          userType: selectedUserType, // user type
          chain_type: selectedChain, // chain
          model_name: selectedModel, // model
          search_type: searchOptions.searchType, // search type
          search_kwargs: searchOptions.search_kwargs, // search parameters
        });

        const responseMessage = { type: "bot", text: res.data.response };
        setMessages(prevMessages => [...prevMessages, responseMessage]);
        setSources(res.data.sources || []);
        setScores(res.data.scores || null);

      } catch (error) {
        console.error("Error fetching data:", error);
        setError("Error fetching data. Please try again.");
      } finally {
        setLoading(false);
      }
    }
  };

  const handleSuggestionClick = async (question) => {
    setStartedChat(true);
    const newMessage = { type: "user", text: question };
    setMessages(prevMessages => [...prevMessages, newMessage]);

    setLoading(true);
    setError(null);

    try {
      const res = await axios.post("https://eej22ko8bc.execute-api.eu-north-1.amazonaws.com/newstage/query", {
        query: question,
      });

      const responseMessage = { type: "bot", text: res.data.response };
      setMessages(prevMessages => [...prevMessages, responseMessage]);
      setSources(res.data.sources || []);
      setScores(res.data.scores || null);
    } catch (error) {
      console.error("Error fetching data:", error);
      setError("Error fetching data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return {
    messages,
    startedChat,
    handleSend,
    handleSuggestionClick,
    loading,
    error,
    sources,
    scores,
  };
};

export default useChatMessages;