// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

// import React from 'react';
// import SmartHomeLanding from './homepage';

// function App() {
//   return (
//     <div>
//       <SmartHomeLanding />
//     </div>
//   );
// }

// export default App;

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './homepage'; // Assuming lowercase as per previous fix
import LoginPage from './login';
import DashboardPage from './dashboard'; // Import the new DashboardPage
import VoiceControlPage from './voice_control';
import StatisticsPage from './statistics';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/voice_control" element={<VoiceControlPage />} />
        <Route path="/statistics" element={<StatisticsPage />} />
        <Route path="/about" element={<div>About Page (Placeholder)</div>} />
      </Routes>
    </Router>
  );
}

export default App;
