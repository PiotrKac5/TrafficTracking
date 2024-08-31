import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Plots.css';

const Plots = () => {
  const [plots, setPlots] = useState({});

  useEffect(() => {
    const fetchPlots = async () => {
      try {
        const response = await axios.get('http://localhost:5000/plots');
        setPlots(response.data);
      } catch (error) {
        console.error('Error fetching plots:', error);
      }
    };

    fetchPlots();
  }, []);

  return (
    <div className="plots-container">
      <h1>Plots from Backend</h1>
      <div>
        <h2>Plot 1</h2>
        {plots.plot1 && <img src={plots.plot1} alt="Plot 1" />}
      </div>
    </div>
  );
};

export default Plots;
