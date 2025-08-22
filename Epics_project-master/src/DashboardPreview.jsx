import React from 'react';
import sidefood from './sidefood.jpg'; // Update the path to the image
import ImageUpload from './ImageUpload';
import grape from './grape.png'; // Update the path to the image
import iwatch from './iwatch.png'; // Update the path to the

const DashboardPage = () => (
  <div className="dashboard-page">
    <div className="left-image">
      <img src={grape} alt="Dashboard Preview" className="dashboard-image" />    </div>
    
    
    <div className="text-section">
      <h1>Be Healthy for Life!</h1>
    </div>
    <div className="iwatch-image">
  <img src={iwatch} alt="Dashboard iwatch"/>
</div>
    <div className="image-upload">
    <ImageUpload />  
    </div>
    <div className="image-section">
    
      <img src={sidefood} alt="Dashboard Preview" className="dashboard-image" />
      
    </div>
    
  </div>
  
);

export default DashboardPage;
