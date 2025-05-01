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
import Sidebar from './sidebar';
import GridLayout from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

// Import the CSS file
import './dashboard.css';

// Register Chart.js components
ChartJS.register(LineElement, PointElement, LinearScale, TimeScale, Title, Tooltip, Legend);

const DashboardPage = () => {
  const chartRef = useRef(null);
  const [humidity, setHumidity] = useState(0);
  const [temperature, setTemperature] = useState(0);
  const [temperatureData, setTemperatureData] = useState({
    labels: [],
    values: []
  });
  const [showWarning, setShowWarning] = useState(false);
  const [warningMessage, setWarningMessage] = useState('');

  // Track current values for warning checks
  const currentValues = useRef({ temp: 0, hum: 0 });

  // Get color based on value and type
  const getColor = (value, type) => {
    if (type === 'temperature') {
      if (value < 20) return '#add8e6'; // light blue
      if (value > 40) return '#ff0000'; // red
      return '#f5e5b3'; // default color
    } else if (type === 'humidity') {
      if (value < 20) return '#add8e6'; // light blue
      if (value > 35) return '#ff0000'; // red
      return '#f5e5b3'; // default color
    }
    return '#f5e5b3';
  };

  // Check for warnings
  const checkWarnings = (temp, hum) => {
    const warnings = [];
    if (temp !== 0 && (temp < 20 || temp > 40)) {
      warnings.push(`Temperature is ${temp < 20 ? 'too low' : 'too high'} (${temp.toFixed(1)}°C)`);
    }
    // if (hum < 20 || hum > 35) {
    //   warnings.push(`Humidity is ${hum < 20 ? 'too low' : 'too high'} (${hum.toFixed(1)}%)`);
    // }
    
    if (warnings.length > 0) {
      setWarningMessage(warnings.join('\n'));
      setShowWarning(true);
    } else {
      setShowWarning(false);
    }
  };

  // Poll for latest data every 1 second and check warnings
  useEffect(() => {
    // Initial fetch
    fetchTemperatureData();
    fetchHumidityData();
    
    // Set up interval for updates
    const fetchInterval = setInterval(() => {
      fetchTemperatureData();
      fetchHumidityData();
    }, 1000);

    // Set up separate interval for warning checks with 1.2s delay
    const warningInterval = setInterval(() => {
      checkWarnings(currentValues.current.temp, currentValues.current.hum);
    }, 1200);
    
    return () => {
      clearInterval(fetchInterval);
      clearInterval(warningInterval);
    };
  }, []);

  // Function to fetch temperature data from the server
  const fetchTemperatureData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/receive_temperature');
      if (!response.data.ok) {
        throw new Error('Failed to fetch temperature data');
      }
      const newTemp = Math.min(100, Math.max(-100, response.data.value));
      setTemperature(newTemp);
      currentValues.current.temp = newTemp; // Update the current temperature value
      
      // Update chart data
      const currentTime = new Date();
      setTemperatureData(prevData => {
        const newLabels = [...prevData.labels, currentTime];
        const newValues = [...prevData.values, newTemp];
        
        if (newLabels.length > 10) {
          newLabels.shift();
          newValues.shift();
        }
        
        return {
          labels: newLabels,
          values: newValues
        };
      });
    } catch (error) {
      console.error('Error fetching temperature data:', error);
    }
  };

  // Function to fetch humidity data from the server
  const fetchHumidityData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/receive_humidity');
      if (!response.data.ok) {
        throw new Error('Failed to fetch humidity data');
      }
      const newHum = Math.min(100, Math.max(0, response.data.value));
      setHumidity(newHum);
      currentValues.current.hum = newHum; // Update the current humidity value
    } catch (error) {
      console.error('Error fetching humidity data:', error);
    }
  };

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

        <div className="dashboard-content">
          <GridLayout
            className="dashboard-grid"
            layout={layout}
            cols={3}
            rowHeight={270}
            width={1100}
            onLayoutChange={(newLayout) => {
              setLayout(newLayout);
              localStorage.setItem('dashboardLayout', JSON.stringify(newLayout));
            }}
            margin={[10, 20]}
            isDraggable={true}
            isResizable={false}
          >
            {/* Temperature Frame Section */}
            <div key="temperature" className="dashboard-frame dashboard-temperature-frame">
              <h3 className="dashboard-frame-title">Temperature Frame</h3>
              <div className="dashboard-progress-bar">
                <div className="dashboard-progress-filled" />
              </div>
              <p className="dashboard-frame-value">25.8°C</p>
            </div>

            {/* Temperature Chart */}
            <div key="tempChart" className="dashboard-frame dashboard-temperature-chart">
              <h3 className="dashboard-frame-title">Temperature</h3>
              <div className="dashboard-chart-container">
                <Line ref={chartRef} data={chartData} options={chartOptions} />
              </div>
            </div>

            {/* Humidity */}
            <div key="humidity" className="dashboard-frame dashboard-humidity-frame">
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
            <div key="light" className="dashboard-frame dashboard-light-frame">
              <h3 className="dashboard-frame-title">Light Frame</h3>
              <div className="dashboard-circle-container dashboard-light-circle">
                <div className="dashboard-light-value-container">
                  <span className="dashboard-circle-value">20%</span>
                  <span className="dashboard-circle-label">Value</span>
                </div>
                <div className="dashboard-circle-overlay dashboard-light-overlay" />
              </div>
            </div>
          </GridLayout>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;