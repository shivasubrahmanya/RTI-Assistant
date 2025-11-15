import { useState } from 'react';
import { AlertCircle, Search, Loader2 } from 'lucide-react';
import { predictDepartment } from '../api';

const Home = ({ onPredictionComplete }) => {
  const [complaint, setComplaint] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!complaint.trim()) {
      setError('Please enter your complaint or issue');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await predictDepartment(complaint);
      onPredictionComplete(result, complaint);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to predict department. Please ensure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">RTI Assistant</h1>
          <p className="text-xl text-gray-700">
            File RTI requests easily with AI-powered assistance
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-2">
              Describe Your Issue
            </h2>
            <p className="text-gray-600">
              Enter your complaint or query in natural language, and we'll help you identify the right department and PIO
            </p>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <textarea
                value={complaint}
                onChange={(e) => setComplaint(e.target.value)}
                placeholder="Example: My ration card has not been updated for 3 months..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all min-h-[150px] resize-y"
                disabled={loading}
              />
            </div>

            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <p className="text-red-800 text-sm">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !complaint.trim()}
              className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  Find Department & PIO
                </>
              )}
            </button>
          </form>

          <div className="mt-8 pt-8 border-t border-gray-200">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">How it works:</h3>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold flex-shrink-0">
                  1
                </div>
                <p className="text-gray-700 pt-1">Describe your issue in your own words</p>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold flex-shrink-0">
                  2
                </div>
                <p className="text-gray-700 pt-1">AI predicts the relevant department and PIO</p>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold flex-shrink-0">
                  3
                </div>
                <p className="text-gray-700 pt-1">Generate a formal RTI letter instantly</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
