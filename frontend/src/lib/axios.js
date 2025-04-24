import axios from 'axios';
import { getCookie } from './getCookie';

axios.interceptors.request.use((config) => {
  const token = getCookie('csrftoken');
  if (token && ['post', 'put', 'patch', 'delete'].includes(config.method)) {
    config.headers['X-CSRFToken'] = token;
  }
  return config;
});

export default axios;