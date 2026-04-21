const BASE_URL = 'http://localhost:8000';

interface RequestOptions extends RequestInit {
  params?: Record<string, string>;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { params, ...init } = options;

  const url = new URL(`${BASE_URL}${path}`);

  // Auto-append user_id from localStorage if not provided in params
  const userId = localStorage.getItem('user_id');
  if (userId && !path.startsWith('/auth')) {
    url.searchParams.append('user_id', userId);
  }

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url.searchParams.append(key, value);
    });
  }

  const response = await fetch(url.toString(), {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...init.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || response.statusText);
  }

  return response.json();
}

export const api = {
  get: <T>(path: string, params?: Record<string, string>) =>
    request<T>(path, { method: 'GET', params }),

  post: <T>(path: string, body?: any, params?: Record<string, string>) =>
    request<T>(path, { method: 'POST', body: JSON.stringify(body), params }),

  put: <T>(path: string, body?: any, params?: Record<string, string>) =>
    request<T>(path, { method: 'PUT', body: JSON.stringify(body), params }),

  delete: <T>(path: string, params?: Record<string, string>) =>
    request<T>(path, { method: 'DELETE', params }),
};
