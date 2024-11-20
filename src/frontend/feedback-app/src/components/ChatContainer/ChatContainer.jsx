// build interface for chatting 

import React, {useEffect, useRef} from "react";
import { VuesaxBulkMenu1 } from "../../icons/VuesaxBulkMenu1";
import { VuesaxTwotoneMicrophone1 } from "../../icons/VuesaxTwotoneMicrophone1";
import { OutlineArrowCircleUp } from "../../icons/OutlineArrowCircleUp";
import StopCircleOutlinedIcon from '@mui/icons-material/StopCircleOutlined';
import CircularProgress from '@mui/material/CircularProgress';
import "./style.css";
import { RiRobot2Line } from "react-icons/ri";
import SourceContainer from "../SourceContainer/SourceContainer";
import RatingContainer from "../RatingContainer/RatingContainer";
import ReactMarkdown from "react-markdown";

const parseMessageText = (text) => {
  return <ReactMarkdown children={text} />;
  // const lines = text.split("\n").filter((line) => line.trim() !== ""); // Split by line and filter empty lines
  // return lines.map((line, index) => {
  //   if (line.startsWith("# ")) {
  //     return <h1 key={index} className="message-title">{line.replace("# ", "")}</h1>;
  //   } else if (line.startsWith("## ")) {
  //     return <h2 key={index} className="message-title">{line.replace("## ", "")}</h2>;
  //   }  else if (line.startsWith("### ")) {
  //     return <h3 key={index} className="message-title">{line.replace("### ", "")}</h3>;
  //   }  else if (line.startsWith("#### ")) {
  //     return <h4 key={index} className="message-subtitle">{line.replace("#### ", "")}</h4>;
  //   } else if (line.startsWith("- ")) {
  //     return <li key={index} className="message-list-item">{line.replace("- ", "")}</li>;
  //   } else {
  //     // Process bold text (e.g., **bold**)
  //     const formattedLine = line.replace(/\*\*(.*?)\*\*/g, (match, p1) => `<strong>${p1}</strong>`);
  //     return <p key={index} dangerouslySetInnerHTML={{ __html: formattedLine }} />;
  //   }
  // });
};

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
  sources,
  scores,
  terminateOutput
}) => {
  // control scroll

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!loading) {
      handleSend();
    }
  };

  // enter key to send query, shift enter to add new line
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!loading) {
        handleSend();
      }
    }
  }

  return (
    <div className="chat">
      <div className="top">
        <div className="search-bar">
          <div className="search-bar-content">
            <textarea
              ref={textareaRef}
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              className="text-wrapper-2"
              placeholder="Tell me something about..."
              rows={1}
              disabled={loading}
            />
          </div>
          <button onClick={handleVoiceInput} className="voice-button" disabled={loading}>
            <VuesaxTwotoneMicrophone1 className="icon-instance-node" />
          </button>
          <button onClick={handleSubmit} className="send-button" disabled={loading}>
            <OutlineArrowCircleUp className="outline-arrow-circle-up" color='var(--black)' />
          </button>
          {/* <button 
            onClick={loading ? terminateOutput : handleSubmit} 
            className="send-button"
            title={loading ? "Stop" : "Send"}
          >
            {loading ? (
              <StopCircleOutlinedIcon style={{ color: "gray" }} />
            ) : (
              <OutlineArrowCircleUp className="outline-arrow-circle-up" color='var(--black)' />
            )}
          </button> */}
        </div>
      </div>
      <div className="main-content">
        <div className="left-content">
          {/* <RatingContainer scores={scores} /> */}
        </div>
        <div className="chat-content">
          <div className="messages-container">
            <div className="empty-content"></div>
            <div className="messages-content">
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.type}`}>
                    {message.type === "bot" && (
                        <div className="icon-wrapper">
                            <RiRobot2Line size="20px" className="robot-icon" />
                        </div>
                    )}
                    <div className="message-text">
                      {/* {message.text} */}
                      <ReactMarkdown>{message.text}</ReactMarkdown>
                    </div>
                  </div>
                ))}
                {loading && (
                    <div className="message bot">
                      <div className="icon-wrapper">
                          <RiRobot2Line size="20px" className="robot-icon" />
                      </div>
                      <div className="loading-text">
                        <CircularProgress size={30} />
                        <p>Searching for Relevant Public Opinions ...</p>
                      </div>
                    </div>
                )}
                {error && (
                    <div className="message bot">
                      <div className="icon-wrapper">
                          <RiRobot2Line size="20px" className="robot-icon" />
                      </div>
                      <div className="message-text">{error}</div>
                    </div>
                )}
            </div>
          </div>
        </div>
        <div className="right-content">
          <SourceContainer sources={sources} loading={loading} />
        </div>
      </div>
    </div>
  );
};

export default ChatContainer;