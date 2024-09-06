import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './Plots.css'

const Plots = () => {
  const [plotUrl, setPlotUrl] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const {duration} = useParams()

  useEffect(() => {
    // Fetch the plot image from the backend
    const fetchPlot = async () => {
      try {
        const response = await fetch(`http://localhost:5000/plots/${duration}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const imageBlob = await response.blob();
        const imageUrl = URL.createObjectURL(imageBlob);
        setPlotUrl(imageUrl);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching the plot:', error);
        setError(error);
        setLoading(false);
      }
    };

    fetchPlot();
  }, [duration]);

  if (loading) {
    return <p>Loading plot...</p>;
  }

  if (error) {
    return <p>Error loading plot: {error.message}</p>;
  }

  return (
    <div className="plot">
      {plotUrl && <img src={plotUrl} alt="Matplotlib Plot" />}
    </div>
  );
};

export default Plots;
