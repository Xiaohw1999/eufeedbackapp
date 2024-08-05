import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Button from '@mui/material/Button';
import './style.css'; // Make sure to import the CSS file

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

const firstOptions = ['Ten', 'Twenty', 'Thirty'];
const secondOptions = ['Forty', 'Fifty', 'Sixty'];
const thirdOptions = ['Seventy', 'Eighty', 'Ninety'];

function getStyles(option, selectedOptions, theme) {
  return {
    fontWeight:
      selectedOptions.indexOf(option) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
}

export default function SidebarContainer() {
  const theme = useTheme();
  const [first, setFirst] = React.useState([]);
  const [second, setSecond] = React.useState([]);
  const [third, setThird] = React.useState([]);

  const handleFirstChange = (event) => {
    const {
      target: { value },
    } = event;
    setFirst(typeof value === 'string' ? value.split(',') : value);
  };

  const handleSecondChange = (event) => {
    const {
      target: { value },
    } = event;
    setSecond(typeof value === 'string' ? value.split(',') : value);
  };

  const handleThirdChange = (event) => {
    const {
      target: { value },
    } = event;
    setThird(typeof value === 'string' ? value.split(',') : value);
  };

  return (
    <div className="sidebar-container">
      <div className="title">Settings</div>
      <div className='select-box'>
        <FormControl className="form-control">
          <InputLabel id="first-select-label">First</InputLabel>
          <Select
            labelId="first-select-label"
            id="first-select"
            multiple
            value={first}
            onChange={handleFirstChange}
            input={<OutlinedInput label="First" />}
            MenuProps={MenuProps}
          >
            {firstOptions.map((option) => (
              <MenuItem
                key={option}
                value={option}
                style={getStyles(option, first, theme)}
              >
                {option}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl className="form-control">
          <InputLabel id="second-select-label">Second</InputLabel>
          <Select
            labelId="second-select-label"
            id="second-select"
            multiple
            value={second}
            onChange={handleSecondChange}
            input={<OutlinedInput label="Second" />}
            MenuProps={MenuProps}
          >
            {secondOptions.map((option) => (
              <MenuItem
                key={option}
                value={option}
                style={getStyles(option, second, theme)}
              >
                {option}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl className="form-control">
          <InputLabel id="third-select-label">Third</InputLabel>
          <Select
            labelId="third-select-label"
            id="third-select"
            multiple
            value={third}
            onChange={handleThirdChange}
            input={<OutlinedInput label="Third" />}
            MenuProps={MenuProps}
          >
            {thirdOptions.map((option) => (
              <MenuItem
                key={option}
                value={option}
                style={getStyles(option, third, theme)}
              >
                {option}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button className="submit-button" variant="contained" color="primary">
          Submit
        </Button>
      </div>   
    </div>
  );
}
