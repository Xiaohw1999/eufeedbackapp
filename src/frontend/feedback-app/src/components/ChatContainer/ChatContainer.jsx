// build interface for chatting 

import React from "react";
import { VuesaxBulkMenu1 } from "../../icons/VuesaxBulkMenu1";
import { VuesaxTwotoneMicrophone1 } from "../../icons/VuesaxTwotoneMicrophone1";
import { OutlineArrowCircleUp } from "../../icons/OutlineArrowCircleUp";
import "./style.css";
import { RiRobot2Line } from "react-icons/ri";
import SourceContainer from "../SourceContainer/SourceContainer";

const ChatContainer = ({ 
  inputValue, 
  handleInputChange, 
  handleVoiceInput, 
  handleSend, 
  isListening, 
  textareaRef, 
  messages,
  loading,
  error,
  sources
}) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    handleSend(inputValue);
  };

  return (
    <div className="chat">
      <div className="top">
        <div className="search-bar">
          <div className="search-bar-content">
            <textarea
              ref={textareaRef}
              value={inputValue}
              onChange={handleInputChange}
              className="text-wrapper-2"
              placeholder="Tell me something about..."
              rows={1}
            />
          </div>
          <button onClick={handleVoiceInput} className="voice-button">
            <VuesaxTwotoneMicrophone1 className="icon-instance-node" />
          </button>
          <button onClick={handleSubmit} className="send-button">
            <OutlineArrowCircleUp className="outline-arrow-circle-up" color='var(--black)' />
          </button>
        </div>
      </div>
      <div className="main-content">
        <div className="left-content"></div>
        <div className="chat-content">
          <div className="messages-container">
            <div className="messages-content">
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.type}`}>
                    {message.type === "bot" && (
                        <div className="icon-wrapper">
                            <RiRobot2Line color="white" size="20px" className="robot-icon" />
                        </div>
                    )}
                    <div className="message-text">{message.text}</div>
                    </div>
                ))}
                {loading && (
                    <div className="message bot">
                    <div className="icon-wrapper">
                        <RiRobot2Line color="white" size="20px" className="robot-icon" />
                    </div>
                    <div className="message-text">Loading...</div>
                    </div>
                )}
                {error && (
                    <div className="message bot">
                    <div className="icon-wrapper">
                        <RiRobot2Line color="white" size="20px" className="robot-icon" />
                    </div>
                    <div className="message-text">{error}</div>
                    </div>
                )}
            </div>
          </div>
        </div>
        <div className="right-content">
          <SourceContainer sources={sources} />
        </div>
      </div>
    </div>
  );
};

export default ChatContainer;