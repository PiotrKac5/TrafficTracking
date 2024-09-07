import React, {useEffect, useRef, useState} from 'react';
import './SampleVid.css';

const SampleVid = () => {
  const [isClicked, setIsClicked] = useState(false);
  const [playbackTime, setPlaybackTime] = useState(0);
  const videoRef = useRef(null);

  // Function to handle button click and toggle video source
  const handleButtonClick = () => {
    if (videoRef.current) {
      setPlaybackTime(videoRef.current.currentTime); // Save current playback time
      setIsClicked(!isClicked); // Toggle video source
    }
  };

  // Function to handle video load event and set playback time
  const handleVideoLoaded = () => {
    if (videoRef.current) {
      videoRef.current.currentTime = playbackTime; // Restore playback time
    }
  };

  // Effect to handle video source change
  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.load(); // Force video element to reload
    }
  }, [isClicked]);

  return (
    <div className="video-container">
      <video
        className="sample_video"
        autoPlay
        loop
        muted
        ref={videoRef}
        onLoadedData={handleVideoLoaded}
      >
        <source src={isClicked ? "/videos/sample_with_mask.mp4" : "/videos/sample_without_mask.mp4"} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <button className="adding mask" onClick={handleButtonClick}>
        {isClicked ? 'Remove mask' : 'Add mask'}
      </button>
    </div>
  );
};

export default SampleVid;
