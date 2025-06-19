import React from "react";
import "./Loading.css";
import ballGif from "./image/ball.GIF";

const Loading = () => {
  return (
    <div className="loading-container">
      <img src={ballGif} alt="Loading..." className="loading-gif" />

      <p>Loading....</p>
    </div>
  );
};

export default Loading;
