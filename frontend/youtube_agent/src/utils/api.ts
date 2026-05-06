const API_BASE_URL = 'http://localhost:8000';

export const apiRequest = async (endpoint: string, options: any = {}) => {
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  // Auto-append user_id to query params if not already there
  let url = `${API_BASE_URL}${endpoint}`;
  if (userId && !endpoint.includes('auth')) {
      const separator = url.includes('?') ? '&' : '?';
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
