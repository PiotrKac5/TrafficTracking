import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Plots from "./Plots";
import Show from "./Vidshow";
// import SampleVid from "./SampleVid";
import About from "./About";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
        <div className="container">
          <App />
          <Routes>
              <Route path='/' element={<Show/>}></Route>
              <Route path='/plots/:duration' element={<Plots/>}></Route>
              <Route path='/about' element={<About/>}></Route>
          </Routes>
        </div>
    </Router>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
