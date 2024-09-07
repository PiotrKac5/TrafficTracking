// import React from "react";
import React, {useEffect, useState} from 'react';
import ReactMarkdown from 'react-markdown';
import aboutContent from './About.md';
import "./About.css"
import SampleVid from "./SampleVid";

const About = () => {
  const [markdown, setMarkdown] = useState('');

  // Fetch the content of the Markdown file
  useEffect(() => {
    fetch(aboutContent)
      .then((response) => response.text())
      .then((text) => {
        setMarkdown(text);
      });
  }, []);

  return (
    <div className="about-page">
      <div className="description">
        <ReactMarkdown
          children={markdown}
          components={{
            a: ({ node, ...props }) => (
              <a {...props} className="custom-link">
                {props.children}
              </a>
            ),
          }}
        />
      </div>
      <SampleVid className="sample_video"/>
    </div>
  );
};

export default About;
