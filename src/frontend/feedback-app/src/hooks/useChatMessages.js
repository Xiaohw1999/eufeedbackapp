// hooks for simulate get response with chat messages

import { useState } from "react";
import axios from "axios";

const useChatMessages = () => {
  const [messages, setMessages] = useState([]);
  const [startedChat, setStartedChat] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSend = async (inputValue, setInputValue) => {
    if (inputValue.trim() !== "") {
      setStartedChat(true);
      const newMessage = { type: "user", text: inputValue.trim() };
      setMessages(prevMessages => [...prevMessages, newMessage]);
      setInputValue("");

      setLoading(true);
      setError(null);

      try {
        const res = await axios.post("http://16.171.132.28/query", {
          query: inputValue.trim(),
        });

        const responseMessage = { type: "bot", text: res.data.response };
        setMessages(prevMessages => [...prevMessages, responseMessage]);
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
      const res = await axios.post("http://16.171.132.28/query", {
        query: question,
      });

      const responseMessage = { type: "bot", text: res.data.response };
      setMessages(prevMessages => [...prevMessages, responseMessage]);
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
  };
};

export default useChatMessages;
