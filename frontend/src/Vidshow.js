import React, {useEffect, useState} from 'react';
import io from 'socket.io-client';
import './Vidshow.css'

const socket = io('/');

// const socket = io('http://localhost:5000');

function Show() {
    const [frame, setFrame] = useState('');

    useEffect(() => {
        socket.on('connect', () => {
            console.log('Connected to server');
            socket.emit('request_frame');
        });

        socket.on('new_frame', (data) => {
            setFrame(`data:image/jpeg;base64,${data}`);
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });

        return () => {
            socket.off('connect');
            socket.off('new_frame');
            socket.off('disconnect');
        };
    }, []);


    return (
        <div className="main-content">
            <header className="App-header">
                {/*<h1>Live Tracking</h1>*/}
                {frame && <img src={frame} alt="Video Stream" style={{maxWidth: '100%', height: 'auto'}}/>}
            </header>
        </div>
    )
}

export default Show