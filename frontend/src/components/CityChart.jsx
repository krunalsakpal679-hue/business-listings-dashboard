import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer, Cell 
} from 'recharts';
import { getCityWise } from '../api/api';

const CityChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getCityWise();
      setData(res);
    } catch (err) {
      console.error("Error loading city data:", err);
      setError("Failed to load city metrics. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Sleek loading skeleton
  if (loading) {
    return (
      <div className="chart-card loading">
        <h3 className="chart-title">City-wise Distribution</h3>
        <div className="skeleton-chart">
          <div className="skeleton-bar" style={{ height: '40%' }}></div>
          <div className="skeleton-bar" style={{ height: '70%' }}></div>
          <div className="skeleton-bar" style={{ height: '50%' }}></div>
          <div className="skeleton-bar" style={{ height: '90%' }}></div>
          <div className="skeleton-bar" style={{ height: '60%' }}></div>
        </div>
      </div>
    );
  }

  // Error boundary fallback
  if (error) {
    return (
      <div className="chart-card error">
        <h3 className="chart-title">City-wise Distribution</h3>
        <div className="error-message">
          <p>{error}</p>
          <button className="retry-btn" onClick={fetchData}>Retry</button>
        </div>
      </div>
    );
  }

  // Curated color palette
  const COLORS = ['#6366f1', '#8b5cf6', '#a78bfa', '#c084fc', '#d8b4fe', '#f3e8ff'];

  return (
    <div className="chart-card">
      <h3 className="chart-title">City-wise Distribution</h3>
      <p className="chart-subtitle">Total listings categorized by cities</p>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={data}
            margin={{ top: 20, right: 10, left: -20, bottom: 5 }}
          >
            <defs>
              <linearGradient id="cityGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#818cf8" stopOpacity={0.9}/>
                <stop offset="100%" stopColor="#4f46e5" stopOpacity={0.6}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#374151" />
            <XAxis 
              dataKey="label" 
              stroke="#9ca3af" 
              fontSize={11}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="#9ca3af" 
              fontSize={11}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(17, 24, 39, 0.85)',
                border: '1px solid rgba(75, 85, 99, 0.4)',
                borderRadius: '8px',
                color: '#fff',
                fontSize: '12px',
                backdropFilter: 'blur(4px)',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
              }}
              cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }}
            />
            <Bar 
              dataKey="count" 
              fill="url(#cityGradient)" 
              radius={[4, 4, 0, 0]}
              animationDuration={800}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default CityChart;
