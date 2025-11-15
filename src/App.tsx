import { useState } from 'react';
import Home from './components/Home.jsx';
import LetterForm from './components/LetterForm.jsx';
import LetterDisplay from './components/LetterDisplay.jsx';


type Step = 'home' | 'form' | 'display';

interface PredictionResult {
  predicted_department: string;
  confidence: number;
  pios: Array<{
    Department: string;
    PIO_Authority: string;
    Authority_Name: string;
    State: string;
    Problem_Description: string;
    Domain_Description: string;
  }>;
}

function App() {
  const [currentStep, setCurrentStep] = useState<Step>('home');
  const [predictionResult, setPredictionResult] = useState<PredictionResult | null>(null);
  const [userIssue, setUserIssue] = useState('');
  const [generatedLetter, setGeneratedLetter] = useState('');

  const handlePredictionComplete = (result: PredictionResult, issue: string) => {
    setPredictionResult(result);
    setUserIssue(issue);
    setCurrentStep('form');
  };

  const handleLetterGenerated = (letter: string) => {
    setGeneratedLetter(letter);
    setCurrentStep('display');
  };

  const handleBackToHome = () => {
    setCurrentStep('home');
    setPredictionResult(null);
    setUserIssue('');
    setGeneratedLetter('');
  };

  

  return (
    <>
      {currentStep === 'home' && (
        <Home onPredictionComplete={handlePredictionComplete} />
      )}
      {currentStep === 'form' && predictionResult && (
        <LetterForm
          predictionResult={predictionResult}
          userIssue={userIssue}
          onBack={handleBackToHome}
          onLetterGenerated={handleLetterGenerated}
        />
      )}
      {currentStep === 'display' && generatedLetter && (
        <LetterDisplay
          letter={generatedLetter}
          onBack={handleBackToHome}
        />
      )}
    </>
  );
}

export default App;
