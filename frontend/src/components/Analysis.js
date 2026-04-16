import React, { useState } from 'react';
import axios from 'axios';

const Analysis = () => {
  const [file, setFile] = useState(null);
  const [industry, setIndustry] = useState('General');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const industries = [
    'General', 'E-Commerce', 'SaaS', 'Hospitality', 'Healthcare'
  ];

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const token = localStorage.getItem('token');
      const formData = new FormData();
      formData.append('file', file);
      formData.append('industry', industry);

      const response = await axios.post('/analyze', formData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      setResults(response.data.results);
    } catch (error) {
      setError(error.response?.data?.detail || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Document Analysis</h1>

      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Document
            </label>
            <input
              type="file"
              accept=".txt,.pdf"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Industry
            </label>
            <select
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              {industries.map(ind => (
                <option key={ind} value={ind}>{ind}</option>
              ))}
            </select>
          </div>

          {error && (
            <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze Document'}
          </button>
        </form>
      </div>

      {results && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-6">Analysis Results</h2>

          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{results.polarity?.toFixed(2)}</div>
              <div className="text-sm text-gray-600">Polarity</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{results.subjectivity?.toFixed(2)}</div>
              <div className="text-sm text-gray-600">Subjectivity</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{results.nps_score?.toFixed(0)}</div>
              <div className="text-sm text-gray-600">NPS Score</div>
            </div>
            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <div className="text-2xl font-bold text-yellow-600">{results.customer_segment}</div>
              <div className="text-sm text-gray-600">Segment</div>
            </div>
          </div>

          {/* Keywords */}
          {results.top_keywords && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-3">Top Keywords</h3>
              <div className="flex flex-wrap gap-2">
                {results.top_keywords.slice(0, 10).map(([keyword, freq], index) => (
                  <span key={index} className="bg-gray-100 px-3 py-1 rounded-full text-sm">
                    {keyword} ({freq})
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Insights */}
          {results.insights && (
            <div>
              <h3 className="text-lg font-semibold mb-3">Industry Insights</h3>
              <ul className="space-y-2">
                {results.insights.map((insight, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <span>{insight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Analysis;