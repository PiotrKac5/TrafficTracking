import React, { useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';
import './Vidshow.css';

const socket = io('/'); // Connect to the server

function Show() {
    const [frame, setFrame] = useState('');
    const [isReady, setIsReady] = useState(false); // State to track readiness
    const [countdown, setCountdown] = useState(15); // Countdown timer for first connection
    const [isFirstConnection, setIsFirstConnection] = useState(false); // Track first-time connection
    const [showLoadingScreen, setShowLoadingScreen] = useState(true); // Show loading screen

    const bufferSize = 110 * 25; // 110 seconds * 25 FPS = 2750 frames
    const frameDisplayInterval = 40; // 40 ms per frame (25 FPS)

    const frameBuffer = useRef(new Array(bufferSize).fill(null)); // Fixed-size buffer
    const writeIndex = useRef(0); // Index for writing frames
    const readIndex = useRef(0); // Index for reading frames

    useEffect(() => {
        // Check if this is the first connection
        const hasConnectedBefore = localStorage.getItem('hasConnectedBefore');
        if (!hasConnectedBefore) {
            // First connection: start countdown
            setIsFirstConnection(true);
            const countdownInterval = setInterval(() => {
                setCountdown((prevCountdown) => {
                    if (prevCountdown > 1) {
                        return prevCountdown - 1;
                    } else {
                        clearInterval(countdownInterval);
                        setIsReady(true);
                        setShowLoadingScreen(false);
                        // Mark the first connection in localStorage
                        localStorage.setItem('hasConnectedBefore', 'true');
                        return 0;
                    }
                });
            }, 1000); // Decrease countdown every second
        } else {
            // Not the first connection: skip countdown
            setIsReady(true);
            setShowLoadingScreen(false);
        }

        let frameDisplayIntervalId; // For storing the interval ID

        // Function to display frames at 25 FPS
        const displayFrames = () => {
            if (!isReady) return; // Only display frames if ready

            const currentFrame = frameBuffer.current[readIndex.current]; // Get the frame at the read index

            if (currentFrame) {
                setFrame(`data:image/jpeg;base64,${currentFrame}`);
                // Move the read index forward, wrap around if at the end
                readIndex.current = (readIndex.current + 1) % bufferSize;
            }
        };

        // Start frame display using setInterval to ensure it runs every 40ms
        frameDisplayIntervalId = setInterval(displayFrames, frameDisplayInterval);

        // Socket events
        socket.on('connect', () => {
            console.log('Connected to server');
            socket.emit('request_frame'); // Request the first frame
        });

        socket.on('new_frame', (data) => {
            // Store the frame in the buffer at the current write index
            frameBuffer.current[writeIndex.current] = data;

            // Move the write index forward, wrap around if at the end
            writeIndex.current = (writeIndex.current + 1) % bufferSize;
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });

        // Cleanup on unmount
        return () => {
            clearInterval(frameDisplayIntervalId); // Stop frame display when component unmounts
            socket.off('connect');
            socket.off('new_frame');
            socket.off('disconnect');
        };
    }, [isReady, frameBuffer]); // Rerun the effect whenever isReady or frameBuffer changes

    return (
        <div className="main-content">
            {showLoadingScreen ? (
                // Show loading screen with countdown
                <div className="loading-screen">
                    <h2>Loading, please wait...</h2>
                    <p>{`Time remaining: ${countdown} seconds`}</p>
                </div>
            ) : (
                // Show the video stream once ready
                <header className="App-header">
                    {frame && <img src={frame} alt="Video Stream" style={{ maxWidth: '100%', height: 'auto' }} />}
                </header>
            )}
        </div>
    );
}

export default Show;
