import React, { useState } from 'react';
import { useTheme } from '@mui/material/styles';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
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

export default function SidebarContainer({ setSelectedTopic }) {
  const theme = useTheme();
  const [first, setFirst] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const firstOptions = ['Any', ...Object.values(topic_dict)];
  
  const handleFirstChange = (event) => {
    setFirst(event.target.value);
  };

  const handleSubmit = () => {
    const topic = first === 'Any' ? null : first;
    setSelectedTopic(topic);
    setOpenSnackbar(true); // 打开 Snackbar
  };

  const handleCloseSnackbar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenSnackbar(false); // 关闭 Snackbar
  };

  return (
    <div className="sidebar-container">
      <div className="title">Settings</div>
      <div className='select-box'>
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
