import React from 'react';
import './App.css';
import Header from './Header.jsx';
// import HeroSection from './HeroSection.jsx';
import DashboardPreview from './DashboardPreview.jsx';
// import Footer from './Footer.jsx';
// import ImageUpload from './ImageUpload.jsx';

function App() {
  return (
    <div className="App">
      <Header />
       {/* <HeroSection />  */}
      <DashboardPreview /> 
       {/* <Footer /> */}
       {/* <ImageUpload /> */}
    </div>
  );
}

export default App;
