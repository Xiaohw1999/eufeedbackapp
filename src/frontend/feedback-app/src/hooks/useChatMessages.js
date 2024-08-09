import { useState } from "react";
import axios from "axios";

const useChatMessages = () => {
  const [messages, setMessages] = useState([]);
  const [startedChat, setStartedChat] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sources, setSources] = useState([]);

  const handleSend = async (inputValue, selectedTopic, setInputValue) => {
    if (inputValue.trim() !== "") {
      setStartedChat(true);
      const newMessage = { type: "user", text: inputValue.trim() };
      setMessages(prevMessages => [...prevMessages, newMessage]);
      setInputValue("");

      setLoading(true);
      setError(null);

      try {
        // send inputValue to backend
        const res = await axios.post("https://eej22ko8bc.execute-api.eu-north-1.amazonaws.com/newstage/query", {
          query: inputValue.trim(),
          topic: selectedTopic // topic
        });

        const responseMessage = { type: "bot", text: res.data.response };
        setMessages(prevMessages => [...prevMessages, responseMessage]);
        setSources(res.data.sources || []);
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
        topic: selectedTopic
      });

      const responseMessage = { type: "bot", text: res.data.response };
      setMessages(prevMessages => [...prevMessages, responseMessage]);
      setSources(res.data.sources || []);
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
    sources
  };
};

export default useChatMessages;
