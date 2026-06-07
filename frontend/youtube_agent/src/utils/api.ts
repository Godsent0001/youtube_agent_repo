const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiRequest = async (endpoint: string, options: any = {}) => {
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  const normalizedEndpoint = endpoint.replace(/\/+$/, "");

  let url = `${API_BASE_URL}${normalizedEndpoint}`;
  const separator = url.includes('?') ? '&' : '?';

  if (userId && !normalizedEndpoint.includes('auth')) {
    if (!url.includes('user_id=')) {
      url = `${url}${separator}user_id=${userId}`;
    }
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
};
