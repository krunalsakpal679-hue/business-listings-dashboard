import React, { useState, useEffect } from 'react';
import { 
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { getCategoryWise } from '../api/api';

const CategoryChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getCategoryWise();
      setData(res);
    } catch (err) {
      console.error("Error loading category data:", err);
      setError("Failed to load category metrics. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Loading state skeleton
  if (loading) {
    return (
      <div className="chart-card loading">
        <h3 className="chart-title">Category-wise Share</h3>
        <div className="skeleton-donut-container">
          <div className="skeleton-donut"></div>
        </div>
      </div>
    );
  }

  // Error boundary state
  if (error) {
    return (
      <div className="chart-card error">
        <h3 className="chart-title">Category-wise Share</h3>
        <div className="error-message">
          <p>{error}</p>
          <button className="retry-btn" onClick={fetchData}>Retry</button>
        </div>
      </div>
    );
  }

  // Curated premium HSL-tailored palette (8 values)
  const COLORS = [
    '#3b82f6', // Blue
    '#10b981', // Emerald
    '#f59e0b', // Amber
    '#ec4899', // Pink
    '#8b5cf6', // Purple
    '#06b6d4', // Cyan
    '#f43f5e', // Rose
    '#14b8a6'  // Teal
  ];

  return (
    <div className="chart-card">
      <h3 className="chart-title">Category-wise Share</h3>
      <p className="chart-subtitle">Distribution of listings by business category</p>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="45%"
              innerRadius={65}
              outerRadius={95}
              paddingAngle={4}
              dataKey="count"
              nameKey="label"
              animationDuration={850}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
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
            />
            <Legend 
              verticalAlign="bottom" 
              height={50}
              iconType="circle"
              iconSize={8}
              wrapperStyle={{ fontSize: '11px', color: '#9ca3af', bottom: 5 }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default CategoryChart;
