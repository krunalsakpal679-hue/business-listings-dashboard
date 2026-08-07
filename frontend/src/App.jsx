import React, { useState, useEffect } from 'react';
import CityChart from './components/CityChart';
import CategoryChart from './components/CategoryChart';
import SourceChart from './components/SourceChart';
import { getCityWise, getCategoryWise, getSourceWise } from './api/api';
import './App.css';

function App() {
  const [stats, setStats] = useState({
    totalListings: 0,
    citiesCount: 0,
    categoriesCount: 0,
    topSource: 'Loading...'
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadOverviewStats = async () => {
      try {
        const [cities, categories, sources] = await Promise.all([
          getCityWise(),
          getCategoryWise(),
          getSourceWise()
        ]);
        
        const total = cities.reduce((acc, curr) => acc + curr.count, 0);
        const top = sources.length > 0 ? sources[0].label : 'N/A';
        
        setStats({
          totalListings: total,
          citiesCount: cities.length,
          categoriesCount: categories.length,
          topSource: top
        });
      } catch (err) {
        console.error("Error loading overview stats:", err);
      } finally {
        setLoading(false);
      }
    };
    
    loadOverviewStats();
  }, []);

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <h1 className="dashboard-title">Business Listings Dashboard</h1>
        <p className="dashboard-subtitle">Real-time marketplace insights, city statistics, and aggregation analytics</p>
      </header>

      {/* Overview Stats Cards */}
      <section className="stats-overview">
        <div className="stat-card">
          <span className="stat-label">Total Listings</span>
          <span className="stat-val">{loading ? "..." : stats.totalListings.toLocaleString()}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Cities Covered</span>
          <span className="stat-val">{loading ? "..." : stats.citiesCount}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Business Categories</span>
          <span className="stat-val">{loading ? "..." : stats.categoriesCount}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Primary Source</span>
          <span className="stat-val" style={{ color: stats.topSource.includes('Google') ? '#60a5fa' : '#fb923c' }}>
            {loading ? "..." : stats.topSource}
          </span>
        </div>
      </section>

      {/* Main Charts Layout */}
      <main className="charts-grid">
        <CityChart />
        <CategoryChart />
        <SourceChart />
      </main>
    </div>
  );
}

export default App;
