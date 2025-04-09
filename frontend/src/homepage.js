import React from "react";
import "./homepage.css";
import logo from "./yolohome.png"
import image from "./homepageimg.jpg"

export default function SmartHomeLanding() {
  return (
    <div className="container">
      <div className="navbar">
        <div className="logo">
          <img src={logo} alt="Smart Home Logo" />
          <span>SMART HOME</span>
        </div>
        <div className="nav-links">
          <button className="disabled-button">Button 6</button>
          <a href="#about">ABOUT US</a>
          <button className="login-button">LOGIN</button>
        </div>
      </div>

      <div className="main-section">
        <div className="text-content">
          <h1><span className="light">smart</span>home</h1>
          <h2>Your home can do anything !</h2>
          <p>Welcome to my smart home</p>
          <button className="learn-more">LEARN MORE</button>
        </div>

        <div className="image-section">
          {[{image}, {image}, {image}].map((src, index) => (
            <img
              key={index}
              src={src}
              alt={image}
              className="cut-image"
            />
          ))}
        </div>
      </div>
    </div>
  );
}
