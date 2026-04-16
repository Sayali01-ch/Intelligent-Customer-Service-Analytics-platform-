import React, { useState, useEffect } from 'react';
import axios from 'axios';

const History = () => {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);

  useEffect(() => {
    fetchAnalyses();
  }, []);

  const fetchAnalyses = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/analyses', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAnalyses(response.data);
    } catch (error) {
      console.error('Error fetching analyses:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAnalysisDetails = async (analysisId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`/analysis/${analysisId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSelectedAnalysis(response.data);
    } catch (error) {
      console.error('Error fetching analysis details:', error);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Analysis History</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Analysis List */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Your Analyses</h2>
          {analyses.length === 0 ? (
            <p className="text-gray-500">No analyses found. Create your first analysis!</p>
          ) : (
            <div className="space-y-3">
              {analyses.map(analysis => (
                <div
                  key={analysis.id}
                  className="border rounded-lg p-4 cursor-pointer hover:bg-gray-50"
                  onClick={() => fetchAnalysisDetails(analysis.id)}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-medium">{analysis.filename}</h3>
                      <p className="text-sm text-gray-600">{analysis.industry}</p>
                      <p className="text-xs text-gray-500">
                        {new Date(analysis.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className={`text-sm font-medium ${
                        analysis.sentiment_category === 'Positive' ? 'text-green-600' :
                        analysis.sentiment_category === 'Negative' ? 'text-red-600' :
                        'text-yellow-600'
                      }`}>
                        {analysis.sentiment_category}
                      </div>
                      <div className="text-xs text-gray-500">
                        {analysis.polarity?.toFixed(2)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Analysis Details */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          {selectedAnalysis ? (
            <>
              <h2 className="text-xl font-semibold mb-4">Analysis Details</h2>

              <div className="space-y-4">
                <div>
                  <h3 className="font-medium">File: {selectedAnalysis.filename}</h3>
                  <p className="text-sm text-gray-600">Industry: {selectedAnalysis.industry}</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-3 bg-blue-50 rounded">
                    <div className="text-lg font-bold text-blue-600">
                      {selectedAnalysis.polarity?.toFixed(2)}
                    </div>
                    <div className="text-xs text-gray-600">Polarity</div>
                  </div>
                  <div className="text-center p-3 bg-green-50 rounded">
                    <div className="text-lg font-bold text-green-600">
                      {selectedAnalysis.nps_score?.toFixed(0)}
                    </div>
                    <div className="text-xs text-gray-600">NPS Score</div>
                  </div>
                </div>

                {selectedAnalysis.keywords && (
                  <div>
                    <h4 className="font-medium mb-2">Top Keywords</h4>
                    <div className="flex flex-wrap gap-1">
                      {selectedAnalysis.keywords.slice(0, 8).map(([keyword, freq], index) => (
                        <span key={index} className="bg-gray-100 px-2 py-1 rounded text-xs">
                          {keyword} ({freq})
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {selectedAnalysis.insights && (
                  <div>
                    <h4 className="font-medium mb-2">Insights</h4>
                    <ul className="space-y-1">
                      {selectedAnalysis.insights.map((insight, index) => (
                        <li key={index} className="text-sm flex items-start">
                          <span className="text-green-500 mr-2">•</span>
                          <span>{insight.content}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="text-center text-gray-500 py-8">
              Select an analysis to view details
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default History;