import React from 'react';

const CalorieDisplay = ({ data }) => {
  if (!data) {
    return <div>No data to display</div>; // Display a fallback message if no data is available
  }

  return (
    <div className="calorie">
      <h3>Food Item: {data.predicted_label}</h3> {/* Display the food label */}
      {/* <p>Probability: {(data.predicted_probability * 100).toFixed(2)}%</p> Display probability as a percentage */}
      <p>Calories: {data.estimated_calories} kcal</p> {/* Display estimated calories */}
      {/* <p>Total Detected Area: {data.total_area} pixels</p>  */}
    </div>
  );
};

export default CalorieDisplay;
