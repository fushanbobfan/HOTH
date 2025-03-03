import React from 'react';
import './Hero.css';
import heroImage from '../assets/Hands+Heart.jpg'; // Add your image to /src/assets/

const Hero = () => {
  return (
    <section className="hero">
      <img src={heroImage} alt="Kindness" />
    </section>
  );
};

export default Hero;
