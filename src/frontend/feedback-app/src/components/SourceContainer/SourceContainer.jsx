import React, { useState } from "react";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import "./style.css";

const parseSourceText = (text) => {
  const titleMatch = text.match(/Title:\s*([^;]*);/);
  const contentMatch = text.match(/Content:\s*([^;]*);/);
  const userTypeMatch = text.match(/UserType:\s*([^;]*);/);
  const countryMatch = text.match(/Country:\s*([^;]*);/);
  const organizationMatch = text.match(/Organization:\s*([^;]*);/);

  return {
    title: titleMatch ? titleMatch[1].trim() : "N/A",
    content: contentMatch ? contentMatch[1].trim() : "N/A",
    userType: userTypeMatch ? userTypeMatch[1].trim() : "N/A",
    country: countryMatch ? countryMatch[1].trim() : "N/A",
    organization: organizationMatch ? organizationMatch[1].trim() : "N/A",
  };
};

const SourceContainer = ({ sources }) => {
  const [page, setPage] = useState(1);
  const itemsPerPage = 1; // 每页显示一个 source

  const handleChange = (event, value) => {
    setPage(value);
  };

  const paginatedSources = sources.slice(
    (page - 1) * itemsPerPage,
    page * itemsPerPage
  );

  return (
    <div className="container">
      <h3>SOURCES</h3>
      <Stack spacing={2} alignItems="center" marginTop={2} className="pagination-container">
        <Pagination
          count={Math.ceil(sources.length / itemsPerPage)}
          page={page}
          onChange={handleChange}
          shape="rounded"
        />
      </Stack>
      <div className="source-container">
        {paginatedSources.map((source, index) => {
          const parsedSource = parseSourceText(source.text);
          return (
            <div key={index} className="source-item">
              <p><strong>Title:</strong> {parsedSource.title}</p>
              <p><strong>Content:</strong> {parsedSource.content}</p>
              <p><strong>User Type:</strong> {parsedSource.userType}</p>
              <p><strong>Country:</strong> {parsedSource.country}</p>
              <p><strong>Organization:</strong> {parsedSource.organization}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default SourceContainer;
