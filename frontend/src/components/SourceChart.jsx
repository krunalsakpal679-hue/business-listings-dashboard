import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, Cell 
} from 'recharts';
import { getSourceWise } from '../api/api';

const SourceChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getSourceWise();
      setData(res);
    } catch (err) {
      console.error("Error loading source data:", err);
      setError("Failed to load data sources. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Loading skeleton state
  if (loading) {
    return (
      <div className="chart-card loading">
        <h3 className="chart-title">Source Distribution</h3>
        <div className="skeleton-chart horizontal">
          <div className="skeleton-bar-h" style={{ width: '80%' }}></div>
          <div className="skeleton-bar-h" style={{ width: '60%' }}></div>
          <div className="skeleton-bar-h" style={{ width: '70%' }}></div>
        </div>
      </div>
    );
  }

  // Error boundary fallback
  if (error) {
    return (
      <div className="chart-card error">
        <h3 className="chart-title">Source Distribution</h3>
        <div className="error-message">
          <p>{error}</p>
          <button className="retry-btn" onClick={fetchData}>Retry</button>
        </div>
      </div>
    );
  }

  // Source-specific colors for branding
  const getSourceColor = (sourceName) => {
    const lowerName = sourceName.toLowerCase();
    if (lowerName.includes("google")) return "#4285f4"; // Google Blue
    if (lowerName.includes("justdial")) return "#ff6f00"; // Justdial Orange
    if (lowerName.includes("sulekha")) return "#00838f"; // Sulekha Teal/Cyan
    return "#6366f1"; // Default Indigo
  };

  return (
    <div className="chart-card">
      <h3 className="chart-title">Source Distribution</h3>
      <p className="chart-subtitle">Listing volume compared across directories</p>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 20, right: 20, left: 10, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#374151" />
            <XAxis 
              type="number" 
              stroke="#9ca3af" 
              fontSize={11}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              dataKey="label" 
              type="category" 
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
              radius={[0, 4, 4, 0]}
              barSize={20}
              animationDuration={900}
            >
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={getSourceColor(entry.label)} 
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default SourceChart;
