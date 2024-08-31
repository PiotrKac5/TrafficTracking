import React, { useState, useEffect } from 'react';

const Plots = () => {
  const [plotUrl, setPlotUrl] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch the plot image from the backend
    const fetchPlot = async () => {
      try {
        const response = await fetch('http://localhost:5000/plots');
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
  }, []);

  if (loading) {
    return <p>Loading plot...</p>;
  }

  if (error) {
    return <p>Error loading plot: {error.message}</p>;
  }

  return (
    <div>
      <h1>Matplotlib Plot</h1>
      {plotUrl && <img src={plotUrl} alt="Matplotlib Plot" />}
    </div>
  );
};

export default Plots;
