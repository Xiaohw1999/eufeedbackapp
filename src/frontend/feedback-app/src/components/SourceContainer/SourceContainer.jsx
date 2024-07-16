import React from "react";
import "./style.css";

const SourceContainer = ({ sources }) => {
  return (
    <div className="source-container">
      <h3>Sources</h3>
      <ul>
        {sources.map((source, index) => (
          <li key={index}>{source.text}</li>
        ))}
      </ul>
    </div>
  );
};

export default SourceContainer;
