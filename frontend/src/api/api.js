import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000,
});

export const getCityWise = async () => {
  const response = await API.get('/dashboard/city-wise');
  return response.data;
};

export const getCategoryWise = async () => {
  const response = await API.get('/dashboard/category-wise');
  return response.data;
};

export const getSourceWise = async () => {
  const response = await API.get('/dashboard/source-wise');
  return response.data;
};

export default API;
