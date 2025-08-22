import React, { useRef, useState } from 'react';
import camera from './camera.jpg';
import CalorieDisplay from './CalorieDisplay';

function Image({ onFileChange }) {
  const fileInputRef = useRef(null);
  const [selectedImage, setSelectedImage] = useState(null);

  function handleImageClick() {
    fileInputRef.current.click();
  }

  function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setSelectedImage(imageUrl);
      onFileChange(imageUrl);
    }
  }

  return (
    <div className='image-container'>
      <img 
        src={camera} 
        alt='Camera' 
        onClick={handleImageClick} 
        className='camera-image' 
      />
      <span className='placeholder-text' onClick={handleImageClick}>Click to choose a file</span>
      <input 
        type="file" 
        ref={fileInputRef} 
        onChange={handleFileChange} 
        style={{ display: 'none' }} 
      />
    </div>
  );
}

function ImageUpload() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [calorieData, setCalorieData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (fileUrl) => {
    setSelectedImage(fileUrl);
    setError('');
  };

  const handleSubmit = async () => {
    if (!selectedImage) return;

    setLoading(true);
    const formData = new FormData();
    const file = await fetch(selectedImage).then(r => r.blob());
    formData.append('image', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        console.log('API response:', result);
        setCalorieData(result);
      } else {
        throw new Error(response.statusText);
      }
    } catch (error) {
      setError('Upload failed: ' + error.message);
      console.error('Error during upload:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="outerContainer">
      <div id="displayingImage">
        <Image onFileChange={handleFileChange} />
        <div className="controls">
          <button className="upload" onClick={handleSubmit} disabled={loading}>
            {loading ? 'Uploading...' : 'Upload Image'}
          </button>
          {error && <div className="error-message">{error}</div>}
        </div>
       
        {/* Uploaded image moved to the end */}
        {selectedImage && (
          <div className='display-image'>
            <img src={selectedImage} alt='Uploaded' className='uploaded-image' />
          </div>
        )}
        {calorieData && <CalorieDisplay data={calorieData} />}
      </div>
    </div>
  );
}

export default ImageUpload;
