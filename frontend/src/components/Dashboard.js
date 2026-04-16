import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalAnalyses: 0,
    avgSentiment: 0,
    topIndustry: 'N/A'
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/analyses', {
        headers: { Authorization: `Bearer ${token}` }
      });

      const analyses = response.data;
      const totalAnalyses = analyses.length;
      const avgSentiment = analyses.length > 0
        ? analyses.reduce((sum, analysis) => sum + analysis.polarity, 0) / analyses.length
        : 0;

      // Calculate top industry
      const industryCount = {};
      analyses.forEach(analysis => {
        industryCount[analysis.industry] = (industryCount[analysis.industry] || 0) + 1;
      });
      const topIndustry = Object.keys(industryCount).reduce((a, b) =>
        industryCount[a] > industryCount[b] ? a : b, 'N/A'
      );

      setStats({ totalAnalyses, avgSentiment, topIndustry });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Customer Service Analytics Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700">Total Analyses</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.totalAnalyses}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700">Average Sentiment</h3>
          <p className="text-3xl font-bold text-green-600">{stats.avgSentiment.toFixed(2)}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700">Top Industry</h3>
          <p className="text-3xl font-bold text-purple-600">{stats.topIndustry}</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            to="/analysis"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition duration-200 text-center"
          >
            New Analysis
          </Link>
          <Link
            to="/history"
            className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition duration-200 text-center"
          >
            View History
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;