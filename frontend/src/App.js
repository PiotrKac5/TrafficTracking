import React, {useState} from 'react';
import './App.css';
import { useNavigate } from 'react-router-dom';

function ExpandableButton() {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const navigate = useNavigate();

  const handleClick = () => {
    setIsExpanded(!isExpanded);
  };

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  }


  const handleButtonClick = (duration) => {
      navigate('/');
      window.location.href = `plots/${duration}`;
  };

  return (
    <div
        className="expandable-button-container"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}>
      <button
        className={`main-button ${isExpanded ? 'expanded' : ''}`}
        onClick={handleClick}
      >
        Plots
      </button>
      {(isExpanded || isHovered) && (
        <div className="additional-buttons">
          <button className="additional-button" onClick={() => handleButtonClick('Yesterday')}>
              Yesterday
          </button>
          <button className="additional-button" onClick={() => handleButtonClick('OneWeek')}>
              Last Week
          </button>
          <button className="additional-button" onClick={() => handleButtonClick('OneMonth')}>
              Last Month
          </button>
        </div>
      )}
    </div>
  );
}


function Navbar() {
  const navigate = useNavigate();

  return (
    <div className="navbar">
      <button className="nav-button" onClick={() => navigate('/')}>
        Home
      </button>
      <ExpandableButton>
        Plots
      </ExpandableButton>
      <button className="nav-button" onClick={() => navigate('/about')}>
        About
      </button>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <Navbar />
    </div>
  );
}
export default App;
