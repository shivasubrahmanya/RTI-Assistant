import axios from 'axios';

interface LetterData {
  user_issue: string;
  user_name: string;
  user_address: string;
  department: string;
  pio_authority: string;
  authority_name: string;
  state: string;
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001';

export async function predictDepartment(complaint: string) {
  const response = await axios.post(`${API_BASE}/predict`, { complaint });
  return response.data;
}

export async function generateLetter(letterData: LetterData) {
  const response = await axios.post(`${API_BASE}/generate-letter`, letterData);
  return response.data;
}
