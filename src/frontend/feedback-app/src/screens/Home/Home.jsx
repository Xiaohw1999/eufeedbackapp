import React, { useState } from "react";
import { Title } from "../../components/Title";
import { VuesaxBulkMenu1 } from "../../icons/VuesaxBulkMenu1";
import { VuesaxLinearFlash5 } from "../../icons/VuesaxLinearFlash5";
import { VuesaxTwotoneMicrophone1 } from "../../icons/VuesaxTwotoneMicrophone1";
import { OutlineArrowCircleUp } from "../../icons/OutlineArrowCircleUp";
import "./style.css";
import ChatContainer from "../../components/ChatContainer/ChatContainer";
import useChat from "../../hooks/useChat";
import useDynamicProperty from "../../hooks/useDynamicProperty";
import { RiRobot2Line } from "react-icons/ri";
import {IconButton, Popover} from "@mui/material";
import NaviContainer from "../../components/NaviContainer/NaviContainer";
import { styled } from "@mui/system";


export const Home = () => {
  const { 
    inputValue, 
    setInputValue, 
    isListening, 
    handleVoiceInput, 
    messages, 
    startedChat, 
    textareaRef, 
    handleInputChange, 
    handleSend, 
    handleSuggestionClick,
    loading,
    error,
    sources
  } = useChat();
  const properties = ["default", "variant-2", "variant-3", "variant-4"];
  const property = useDynamicProperty(properties);

  const handleSubmit = async (event) => {
    event.preventDefault();
    await handleSend(inputValue);
    setInputValue("");
  };

  const [anchorEl, setAnchorEl] = useState(null);
  const handleMenuClick = (event) => {
    event.stopPropagation();
    event.preventDefault();
    setAnchorEl(event.currentTarget);
  }
  const handleMenuClose = (event) => {
    event.stopPropagation();
    event.preventDefault();
    setAnchorEl(null);
  };
  const open = Boolean(anchorEl);

  return (
    <div className="home">
      <div className="top">
          <div className="navigation-bar">
            <IconButton edge="start" color="inherit" onClick={handleMenuClick}>
              <VuesaxBulkMenu1 className="vuesax-bulk-menu" />
            </IconButton>
            <Popover
              anchorEl={anchorEl}
              open={open}
              onClose={handleMenuClose}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'center',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'center',
              }}
            >
              <NaviContainer handleClose={handleMenuClose} />
            </Popover>
          </div>
          {startedChat ? (
            <ChatContainer
              inputValue={inputValue}
              handleInputChange={handleInputChange}
              handleVoiceInput={handleVoiceInput}
              handleSend={handleSend}
              isListening={isListening}
              textareaRef={textareaRef}
              messages={messages}
              loading={loading}
              error={error}
              sources={sources}
            />
          ) : (     
          <div className="contents">
            <div className="div">
              <Title
                className="title-instance"
                property1={property}
                text="Civic Feedback Enhancer"
                visible={true}
              />
              <div className="subtitle">
                <p className="text-wrapper">
                  Ask me freely about EU laws and initiatives, this chatbot will present citizens' opinions about them.
                </p>
              </div>
            </div>
            <div className="frame" />
            <div className="search-bar">
              <div className="content">
                <RiRobot2Line size="20px" className="robot-icon" />
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
                <OutlineArrowCircleUp className="outline-arrow-circle-up" color='var(--black)'/>
              </button>
            </div>
            <div className="bottom">
              <div className="text-wrapper-3">You may ask</div>
              <div className="boxes">
                <div className="suggestion-card" onClick={() => handleSuggestionClick("What is the role of the European Rural Parliament (ERP) in shaping the vision for rural areas in Europe?")}>
                  <p className="suggestion-question">
                    <span className="span">What is the role of the European Rural Parliament (ERP) </span>
                    <span className="text-wrapper-4">in shaping the vision for rural areas in Europe?</span>
                  </p>
                  <div className="frame-2">
                    <div className="text-wrapper-5">Ask this</div>
                    <VuesaxLinearFlash5 className="vuesax-linear-flash" />
                  </div>
                </div>
                <div className="suggestion-card" onClick={() => handleSuggestionClick("Can you explain the significance of localism and empowerment in the ERP's vision for rural Europe?")}>
                  <p className="suggestion-question">
                    <span className="text-wrapper-6">Can you explain the significance of localism and </span>
                    <span className="text-wrapper-7">empowerment in the ERP's vision for rural Europe?</span>
                  </p>
                  <div className="frame-2">
                    <div className="text-wrapper-5">Ask this</div>
                    <VuesaxLinearFlash5 className="vuesax-linear-flash" />
                  </div>
                </div>
                <div className="suggestion-card" onClick={() => handleSuggestionClick("Why does the ERP emphasize the need for flexible policies tailored to diverse rural areas?")}>
                  <p className="suggestion-question">
                    <span className="text-wrapper-8">Why does the ERP emphasize the need for </span>
                    <span className="text-wrapper-7">flexible policies tailored to diverse rural areas?</span>
                  </p>
                  <div className="frame-2">
                    <div className="text-wrapper-5">Ask this</div>
                    <VuesaxLinearFlash5 className="vuesax-linear-flash" />
                  </div>
                </div>
              </div>
            </div>
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
          </div>
          )}
      </div>
    </div>
  );
};

