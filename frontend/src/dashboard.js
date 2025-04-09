import React, { useRef, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  TimeScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import Sidebar from './sidebar'; // Import the Sidebar component

// Import the CSS file
import './dashboard.css';

// Register Chart.js components
ChartJS.register(LineElement, PointElement, LinearScale, TimeScale, Title, Tooltip, Legend);

const DashboardPage = () => {
  const chartRef = useRef(null);

  // Chart data
  const chartData = {
    labels: [
      new Date('2025-04-09T00:00:00'),
      new Date('2025-04-09T03:00:00'),
      new Date('2025-04-09T06:00:00'),
      new Date('2025-04-09T09:00:00'),
      new Date('2025-04-09T12:00:00'),
      new Date('2025-04-09T15:00:00'),
      new Date('2025-04-09T18:00:00'),
      new Date('2025-04-09T21:00:00'),
      new Date('2025-04-10T00:00:00'),
    ],
    datasets: [
      {
        label: 'Temperature (°C)',
        data: [26.5, 26.0, 25.5, 25.8, 25.7, 25.9, 26.1, 25.8, 25.6],
        borderColor: '#f5e5b3',
        backgroundColor: 'rgba(245, 229, 179, 0.2)',
        fill: true,
        tension: 0.3,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'hour',
          displayFormats: { hour: 'HH:mm' },
        },
        ticks: {
          maxTicksLimit: 8,
          source: 'data',
        },
      },
      y: {
        beginAtZero: false,
        min: 20,
        max: 30,
        title: {
          display: true,
          text: 'Temperature (°C)',
        },
      },
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
  };

  // Cleanup chart instance on unmount
  useEffect(() => {
    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, []);

  return (
    <div className="dashboard-page">
      {/* Sidebar */}
      <Sidebar activePage="DASHBOARD" />

      {/* Main Content */}
      <main className="dashboard-main-content">
        <header className="dashboard-header">
          <div>
            <h1 className="dashboard-header-title">Welcome, My Smart Home</h1>
            <p className="dashboard-header-subtitle">
              District 10, HCM city • Partly Cloudy
            </p>
          </div>
          <div className="dashboard-header-right">
            <span className="dashboard-temperature">25.8°C</span>
            <button className="dashboard-add-device-button">+ NEW DEVICE</button>
          </div>
        </header>

        <div className="dashboard-grid">
          {/* Temperature Frame Section */}
          <div className="dashboard-frame dashboard-temperature-frame">
            <h3 className="dashboard-frame-title">Temperature Frame</h3>
            <div className="dashboard-progress-bar">
              <div className="dashboard-progress-filled" />
            </div>
            <p className="dashboard-frame-value">25.8°C</p>
          </div>

          {/* Temperature Chart */}
          <div className="dashboard-frame dashboard-temperature-chart">
            <h3 className="dashboard-frame-title">Temperature</h3>
            <div className="dashboard-chart-container">
              <Line ref={chartRef} data={chartData} options={chartOptions} />
            </div>
          </div>

          {/* Humidity */}
          <div className="dashboard-frame dashboard-humidity-frame">
            <h3 className="dashboard-frame-title">Humidity</h3>
            <div className="dashboard-circle-container">
              <span className="dashboard-circle-value">53.9%</span>
              <div className="dashboard-circle-overlay" />
            </div>
          </div>

          {/* Motion */}
          <div className="dashboard-frame dashboard-motion-frame">
            <h3 className="dashboard-frame-title">Motion</h3>
            <div className="dashboard-circle-container dashboard-motion-circle">
              <span className="dashboard-circle-value">-</span>
            </div>
          </div>

          {/* Light Frame */}
          <div className="dashboard-frame dashboard-light-frame">
            <h3 className="dashboard-frame-title">Light Frame</h3>
            <div className="dashboard-circle-container dashboard-light-circle">
              <div className="dashboard-light-value-container">
                <span className="dashboard-circle-value">20%</span>
                <span className="dashboard-circle-label">Value</span>
              </div>
              <div className="dashboard-circle-overlay dashboard-light-overlay" />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;