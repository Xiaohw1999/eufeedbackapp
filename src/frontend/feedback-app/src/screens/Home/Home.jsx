import React, { useState } from "react";
import { Title } from "../../components/Title";
import { Property1Gym } from "../../icons/Property1Gym";
import { Property1Headphone } from "../../icons/Property1Headphone";
import { Property1Noise } from "../../icons/Property1Noise";
import { VuesaxBulkMenu1 } from "../../icons/VuesaxBulkMenu1";
import { VuesaxLinearFlash5 } from "../../icons/VuesaxLinearFlash5";
import { AiIcon } from "../../icons/AiIcon";
import { VuesaxTwotoneMicrophone1 } from "../../icons/VuesaxTwotoneMicrophone1";
import { OutlineArrowCircleUp } from "../../icons/OutlineArrowCircleUp";
import "./style.css";
import ChatContainer from "../../components/ChatContainer/ChatContainer";
import useChat from "../../hooks/useChat";
import useDynamicProperty from "../../hooks/useDynamicProperty";

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
    error
  } = useChat();
  const properties = ["default", "variant-2", "variant-3", "variant-4"];
  const property = useDynamicProperty(properties);

  const handleSubmit = async (event) => {
    event.preventDefault();
    await handleSend(inputValue);
    setInputValue("");
  };

  return (
    <div className="home">
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
        />
      ) : (
        <div className="top">
          <div className="navigation-bar">
            <VuesaxBulkMenu1 className="vuesax-bulk-menu" />
          </div>
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
                <AiIcon className="icon-instance-node" color="url(#paint0_linear_8_232)" />
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
                <OutlineArrowCircleUp className="outline-arrow-circle-up" />
              </button>
            </div>
            <div className="bottom">
              <div className="text-wrapper-3">You may ask</div>
              <div className="boxes">
                <div className="suggestion-card" onClick={() => handleSuggestionClick("What is the role of the European Rural Parliament (ERP) in shaping the vision for rural areas in Europe?")}>
                  <Property1Gym className="icons" />
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
                  <Property1Headphone className="icons" />
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
                  <Property1Noise className="icons" />
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
        </div>
      )}
    </div>
  );
};

