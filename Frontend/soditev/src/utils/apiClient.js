// utils/apiClient.js

import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // URL de votre backend
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
