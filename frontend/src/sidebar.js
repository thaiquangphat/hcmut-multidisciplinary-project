import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import logoImg from './yolohome.png';
import { FaHome, FaMicrochip, FaChartLine, FaUsers, FaMicrophone, FaCog, FaUser } from 'react-icons/fa';
import './sidebar.css';

const Sidebar = () => {
  const location = useLocation();

  const pathToLabel = {
    '/dashboard': 'DASHBOARD',
    '/devices': 'DEVICES',
    '/statistics': 'STATISTICS',
    '/family_members': 'FAMILY MEMBERS',
    '/voice_control': 'VOICE CONTROL',
    '/setting': 'SETTING',
  };

  const activePage = pathToLabel[location.pathname] || 'DASHBOARD';

  const navItems = [
    { to: '/dashboard', label: 'DASHBOARD', icon: <FaHome /> },
    { to: '/devices', label: 'DEVICES', icon: <FaMicrochip /> },
    { to: '/statistics', label: 'STATISTICS', icon: <FaChartLine /> },
    { to: '/family_members', label: 'FAMILY MEMBERS', icon: <FaUsers /> },
    { to: '/voice_control', label: 'VOICE CONTROL', icon: <FaMicrophone /> },
    { to: '/setting', label: 'SETTING', icon: <FaCog /> },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        <Link to="/" className="logo-link">
          <div className="logo-container">
            <img src={logoImg} alt="Smart Home Logo" className="logo" />
            <span className="logo-title">SMART HOME</span>
          </div>
        </Link>

        <nav className="nav-container">
          <ul className="nav-list">
            {navItems.map((item) => (
              <li key={item.to} className="nav-item">
                <Link
                  to={item.to}
                  className={`nav-link ${item.label === activePage ? 'active' : ''}`}
                >
                  <span className="nav-icon">{item.icon}</span>
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>

      <div className="user-profile">
        <FaUser className="user-icon" />
        <span>Thao Le</span>
      </div>
    </aside>
  );
};

export default Sidebar;