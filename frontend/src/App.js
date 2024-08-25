import React, {useState} from 'react';
import './App.css';  // Ensure you have this file
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
      // window.location.href = 'https://www.youtube.com';
      navigate('/');
      window.location.href = `plot/${duration}`;
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

function App() {
    const navigate = useNavigate();
    const [isSidebarExpanded, setSidebarExpanded] = useState(false);

    const toggleSidebar = () => {
        setSidebarExpanded(!isSidebarExpanded);
    };

    const handleButtonClick = (buttonId) => {
        // console.log(`Button ${buttonId} clicked`);
        // window.location.href = 'https://localhost:3000';
        navigate('/');
        // Add logic for button click actions here
    };

    return (
        <div className="App">
            <div className={`sidebar ${isSidebarExpanded ? 'expanded' : ''}`}>
                <button className="toggle-button" onClick={toggleSidebar}>
                    {isSidebarExpanded ? '<' : '>'}
                </button>
                {isSidebarExpanded && (
                    <>
                        <button onClick={() => handleButtonClick(1)}>
                            {/*<span className="icon">📁</span>*/}
                            <span className="text">Live Tracking</span>
                        </button>
                        <ExpandableButton onClick={() => handleButtonClick(2)}>
                            {/*<span className="icon">📂</span>*/}
                            <span className="text">Plots</span>
                        </ExpandableButton>
                    </>
                )}
            </div>
        </div>
    );
}

export default App;
