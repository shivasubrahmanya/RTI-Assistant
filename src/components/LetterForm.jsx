import { useState } from 'react';
import { AlertCircle, ArrowLeft, FileText, Loader2 } from 'lucide-react';
import { generateLetter } from '../api';

const LetterForm = ({ predictionResult, userIssue, onBack, onLetterGenerated }) => {
  const [formData, setFormData] = useState({
    userName: '',
    userAddress: '',
    selectedPio: predictionResult.pios[0] || {},
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePioSelect = (e) => {
    const selectedIndex = parseInt(e.target.value);
    setFormData(prev => ({
      ...prev,
      selectedPio: predictionResult.pios[selectedIndex]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.userName.trim() || !formData.userAddress.trim()) {
      setError('Please fill in all required fields');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const letterData = {
        user_issue: userIssue,
        user_name: formData.userName,
        user_address: formData.userAddress,
        department: formData.selectedPio.Department,
        pio_authority: formData.selectedPio.PIO_Authority,
        authority_name: formData.selectedPio.Authority_Name,
        state: formData.selectedPio.State,
      };

      const result = await generateLetter(letterData);
      onLetterGenerated(result.letter);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate letter. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <button
          onClick={onBack}
          className="mb-6 flex items-center gap-2 text-gray-700 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Search
        </button>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Generate RTI Letter</h2>

          <div className="mb-8 p-6 bg-blue-50 rounded-lg">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Prediction Results</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Predicted Department:</span>
                <span className="font-semibold text-gray-900">{predictionResult.predicted_department}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Confidence:</span>
                <span className="font-semibold text-gray-900">
                  {(predictionResult.confidence * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Your Full Name *
              </label>
              <input
                type="text"
                name="userName"
                value={formData.userName}
                onChange={handleChange}
                placeholder="Enter your full name"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                disabled={loading}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Your Address *
              </label>
              <textarea
                name="userAddress"
                value={formData.userAddress}
                onChange={handleChange}
                placeholder="Enter your complete address"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all min-h-[100px] resize-y"
                disabled={loading}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Select Public Information Officer (PIO)
              </label>
              <select
                onChange={handlePioSelect}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                disabled={loading}
              >
                {predictionResult.pios.map((pio, index) => (
                  <option key={index} value={index}>
                    {pio.PIO_Authority} - {pio.Authority_Name} ({pio.State})
                  </option>
                ))}
              </select>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-semibold text-gray-700 mb-3">Selected PIO Details:</h4>
              <div className="space-y-2 text-sm">
                <div>
                  <span className="text-gray-600">Authority:</span>{' '}
                  <span className="font-medium text-gray-900">{formData.selectedPio.PIO_Authority}</span>
                </div>
                <div>
                  <span className="text-gray-600">Name:</span>{' '}
                  <span className="font-medium text-gray-900">{formData.selectedPio.Authority_Name}</span>
                </div>
                <div>
                  <span className="text-gray-600">State:</span>{' '}
                  <span className="font-medium text-gray-900">{formData.selectedPio.State}</span>
                </div>
              </div>
            </div>

            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <p className="text-red-800 text-sm">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Generating Letter...
                </>
              ) : (
                <>
                  <FileText className="w-5 h-5" />
                  Generate RTI Letter
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LetterForm;
