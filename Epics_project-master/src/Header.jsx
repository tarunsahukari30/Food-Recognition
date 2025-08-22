import React from 'react';
import logosrc from './logosrc.jpg'; // Adjust the path based on your project structure

const Header = () => (
  <header className="header">
    <div className="logo">
      <img src={logosrc} alt="Logo" className="logo-image" />
     <h1>Food Recognition and Calorie Estimation</h1>
    </div>
    <div className="buttons">
      {/* Buttons here if needed */}
    </div>
  </header>
);

export default Header;
