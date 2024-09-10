import React, { useState } from 'react';
import { useTheme } from '@mui/material/styles';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import './style.css';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      maxwidth: 200,
      width: 100,
    },
  },
};

const topic_dict = {
    "AGRI": "Agriculture and rural development",
    "FINANCE": "Banking and financial services",
    "BORDERS": "Borders and security",
    "BUDGET": "Budget",
    "BUSINESS": "Business and industry",
    "CLIMA": "Climate action",
    "COMP": "Competition",
    "CONSUM": "Consumers",
    "CULT": "Culture and media",
    "CUSTOMS": "Customs",
    "DIGITAL": "Digital economy and society",
    "ECFIN": "Economy, finance and the euro",
    "EAC": "Education and training",
    "EMPL": "Employment and social affairs",
    "ENER": "Energy",
    "ENV": "Environment",
    "ENLARG": "EU enlargement",
    "NEIGHBOUR": "European neighbourhood policy",
    "FOOD": "Food safety",
    "FOREIGN": "Foreign affairs and security policy",
    "FRAUD": "Fraud prevention",
    "HOME": "Home affairs",
    "HUMAN": "Humanitarian aid and civil protection",
    "INST": "Institutional affairs",
    "INTDEV": "International cooperation and development",
    "JUST": "Justice and fundamental rights",
    "MARE": "Maritime affairs and fisheries",
    "ASYL": "Migration and asylum",
    "HEALTH": "Public health",
    "REGIO": "Regional policy",
    "RESEARCH": "Research and innovation",
    "SINGMARK": "Single market",
    "SPORT": "Sport",
    "STAT": "Statistics",
    "TAX": "Taxation",
    "TRADE": "Trade",
    "TRANSPORT": "Transport",
    "YOUTH": "Youth"
};

const chainOptions = [
  {value: 'conversational', label: 'Conversational Retrieval Chain'},
  {value: 'retrievalqa', label: 'QA Retrieval Chain'}
];

const modelOptions = [
  { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
  { value: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
  { value: 'gpt-4o-mini', label: 'GPT-4o Mini' },
  { value: 'gpt-4o', label: 'GPT-4o' },
];

const searchTypeOptions = [
  { value: 'similarity', label: 'Similarity' },
  { value: 'mmr', label: 'MMR (Maximal Marginal Relevance)' },
  // { value: 'similarity_score_threshold', label: 'Similarity Score Threshold' },
];

const fetchKOptions = [20, 30, 40];

export default function SidebarContainer({ setSelectedTopic, setSelectedChain, setSelectedModel, setSearchOptions }) {
  const theme = useTheme();
  const [first, setFirst] = useState('');
  const [chain, setChain] = useState('conversational');
  const [model, setModel] = useState('gpt-3.5-turbo');
  const [searchType, setSearchType] = useState('similarity');
  const [k, setK] = useState(5);
  const [fetchK, setFetchK] = useState(20);
  const [lambdaMult, setLambdaMult] = useState(0.5);
  const [scoreThreshold, setScoreThreshold] = useState(0.8);
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const firstOptions = ['Any', ...Object.values(topic_dict)];
  
  const handleFirstChange = (event) => {
    setFirst(event.target.value);
  };

  const handleChainChange = (event) => {
    setChain(event.target.value);
  }

  const handleModelChange = (event) => {
    setModel(event.target.value);
  };

  const handleSearchTypeChange = (event) => {
    setSearchType(event.target.value);
  };

  const handleSubmit = () => {
    const topic = first === 'Any' ? null : first;
    setSelectedTopic(topic);
    setSelectedChain(chain);
    setSelectedModel(model);
    setSearchOptions({
      searchType,
      search_kwargs: {
        k,
        fetch_k: searchType === 'mmr' ? fetchK : undefined,
        lambda_mult: searchType === 'mmr' ? lambdaMult : undefined,
        score_threshold: searchType === 'similarity_score_threshold' ? scoreThreshold : undefined,
      }
    });
    setOpenSnackbar(true); // open Snackbar
  };

  const handleCloseSnackbar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenSnackbar(false); // close Snackbar
  };

  return (
    <div className="sidebar-container">
      <div className="title">Settings</div>
      <div className='select-box'>
        {/* Topic */}
        <FormControl className="form-control">
          <InputLabel id="first-select-label">Topics</InputLabel>
          <Select
            labelId="first-select-label"
            id="first-select"
            value={first}
            onChange={handleFirstChange}
            input={<OutlinedInput label="Topics" />}
            MenuProps={MenuProps}
          >
            {firstOptions.map((option) => (
              <MenuItem key={option} value={option}>
                {option}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        {/* Chain */}
        <FormControl className="form-control">
          <InputLabel id="chain-select-label">Retrieval Chain</InputLabel>
          <Select
            labelId="chain-select-label"
            id="chain-select"
            value={chain}
            onChange={handleChainChange}
            input={<OutlinedInput label="Retrieval Chain" />}
            MenuProps={MenuProps}
          >
            {chainOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        {/* Model */}
        <FormControl className="form-control">
          <InputLabel id="model-select-label">Model</InputLabel>
          <Select
            labelId="model-select-label"
            id="model-select"
            value={model}
            onChange={handleModelChange}
            input={<OutlinedInput label="Model" />}
            MenuProps={MenuProps}
          >
            {modelOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        {/* Search Type */}
        <FormControl className="form-control">
          <InputLabel id="search-type-select-label">Search Type</InputLabel>
          <Select
            labelId="search-type-select-label"
            id="search-type-select"
            value={searchType}
            onChange={handleSearchTypeChange}
            input={<OutlinedInput label="Search Type" />}
            MenuProps={MenuProps}
          >
            {searchTypeOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {(searchType === 'similarity' || searchType === 'mmr' || searchType === 'similarity_score_threshold') && (
          <TextField
            label="Number of Results (k)"
            type="number"
            value={k}
            onChange={(e) => setK(parseInt(e.target.value))}
            fullWidth
            margin="normal"
          />
        )}

        {searchType === 'mmr' && (
          <>
            <FormControl className="form-control">
              <InputLabel id="fetch-k-select-label">Fetch K (MMR)</InputLabel>
              <Select
                labelId="fetch-k-select-label"
                id="fetch-k-select"
                value={fetchK}
                onChange={(e) => setFetchK(parseInt(e.target.value))}
                input={<OutlinedInput label="Fetch K (MMR)" />}
                MenuProps={MenuProps}
              >
                {fetchKOptions.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              label="Lambda Mult (MMR)"
              type="number"
              value={lambdaMult}
              onChange={(e) => setLambdaMult(parseFloat(e.target.value))}
              fullWidth
              margin="normal"
            />
          </>
        )}

        {searchType === 'similarity_score_threshold' && (
          <TextField
            label="Score Threshold"
            type="number"
            value={scoreThreshold}
            onChange={(e) => setScoreThreshold(parseFloat(e.target.value))}
            fullWidth
            margin="normal"
          />
        )}
        <Button className="submit-button" variant="contained" color="primary" onClick={handleSubmit}>
          Submit
        </Button>
      </div>   

      {/* snackbar */}
      <Snackbar 
        open={openSnackbar} 
        autoHideDuration={1200} 
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity="success" sx={{ width: '100%' }}>
          Successfully submitted!
        </Alert>
      </Snackbar>
    </div>
  );
}
