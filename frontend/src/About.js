import React, {useEffect, useState} from 'react';
import ReactMarkdown from 'react-markdown';
import aboutContent from './About.md';
import "./About.css"

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
      <ReactMarkdown>{markdown}</ReactMarkdown>
    </div>
  );
};

export default About;
