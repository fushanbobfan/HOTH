import React from 'react';
import './About.css';
import heroImage from '../assets/WechatIMG9.jpeg'; 

const About = () => {
  return (
    <section className="about-section">
      <h2>WHAT WE BELIEVE IN</h2>
      <p>Our mission is to cultivate a world where kindness is the foundation of every interaction...</p>

      <div className="about-content">
        <h3>Who we are</h3>
        <img src={heroImage} className="responsive-img" alt="Who we are"/>
        <p>From Left to Right:</p>
        <p>
          Hanson Zhao - 1st year, data theory <br />
          Bob Fan - 1st year, data theory <br />
          Michelle Wang - 1st year, environmental science <br />
          Eileen Xue - 4th year, data science
        </p>
      </div>
    </section>
  );
};

export default About;
