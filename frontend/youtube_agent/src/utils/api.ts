const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://youtube-backend-agent-repo.onrender.com';

export const apiRequest = async (endpoint: string, options: any = {}) => {
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  // Standardize API structure: ALWAYS remove trailing slashes
  // to follow canonical REST patterns and avoid redirect loops.
  const normalizedEndpoint = endpoint.replace(/\/+$/, "");

  // Auto-append user_id to query params if not already there
  let url = `${API_BASE_URL}${normalizedEndpoint}`;
  if (userId && !normalizedEndpoint.includes('auth')) {
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
