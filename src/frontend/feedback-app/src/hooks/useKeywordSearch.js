import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import debounce from 'lodash/debounce';

function useKeywordSearch() {
  const [keyword, setKeyword] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedResult, setSelectedResult] = useState(null);

  const handleKeywordChange = (newValue) => {
    setKeyword(newValue);
  };

  const handleKeywordSearch = useCallback(async () => {
    if (!keyword.trim()) {
      setError('Please enter a keyword to search.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.get(
        'https://eej22ko8bc.execute-api.eu-north-1.amazonaws.com/newstage/search_keywords', 
        { params: { keyword } }
      );
      setSearchResults(response.data);

      if (response.data.length === 0) {
        setError('No matching documents found.');
        setTimeout(() => {
          setError(null);
        }, 2000); // 2 seconds delay before clearing the error message
      }

    } catch (error) {
      console.error("Error fetching search results:", error);
      setError(error.response?.data?.detail || error.message || 'An error occurred');
      setTimeout(() => {
        setError(null);
      }, 2000); // 2 seconds delay before clearing the error message
    } finally {
      setIsLoading(false);
    }
  }, [keyword]);

  const debouncedSearch = useCallback(debounce(handleKeywordSearch, 1000), [handleKeywordSearch]);

  useEffect(() => {
    if (keyword.trim()) {
      debouncedSearch();
    }
    return () => {
      debouncedSearch.cancel();
    };
  }, [keyword, debouncedSearch]);

  useEffect(() => {
    if (selectedResult) {
      setKeyword(selectedResult.shortTitle || String(selectedResult.id));
    }
  }, [selectedResult]);

  return {
    keyword,
    searchResults,
    isLoading,
    error,
    handleKeywordChange,
    handleKeywordSearch,
    selectedResult,
    setSelectedResult,
  };
}

export default useKeywordSearch;
