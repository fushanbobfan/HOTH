import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Product.css';

const Product = () => {
  const [quote, setQuote] = useState("");
  const fetchQuote = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/random_quote"); 
      setQuote(response.data.quote);
    } catch (error) {
      console.error("Error fetching quote:", error);
    }
  };
  useEffect(() => {
    fetchQuote();
  }, []);
  return (
    <section className="product-section">
      <h3>Daily Word Of Kindness</h3>
      <ul>
        <li>{quote}</li>
      </ul>
    </section>
  );
};

export default Product;
