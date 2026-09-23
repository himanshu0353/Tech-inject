const getApiBaseUrl = () => {
  if (typeof window !== 'undefined' && window.location && window.location.hostname) {
    return `${window.location.protocol}//${window.location.hostname}:8000/api`;
  }
  return 'http://127.0.0.1:8000/api';
};

const API_BASE_URL = getApiBaseUrl();

export interface User {
  id: number;
  email: string;
  role: 'admin' | 'customer';
  is_premium: boolean;
  created_at: string;
  token?: string;
}

export interface PropDef {
  name: string;
  type: string;
  default?: string;
  description: string;
}

export interface Dependency {
  name: string;
  version: string;
  is_dev?: boolean;
}

export interface ComponentSummary {
  id: number;
  slug: string;
  name: string;
  description: string;
  category: string;
  access_level: 'free' | 'premium';
  status: 'draft' | 'published';
  version: string;
  created_at: string;
  updated_at: string;
  published_at?: string;
}

export interface ComponentDetail extends ComponentSummary {
  props: PropDef[];
  dependencies: Dependency[];
  preview_data: Record<string, any>;
  source_files?: Record<string, string> | null;
  is_locked: boolean;
}

// Fetch helper with credentials for JWT cookie support & Authorization header fallback
async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('tech_inject_token') : null;
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    credentials: 'include',
    headers,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'API Error' }));
    throw new Error(errorData.detail || `Request failed with status ${res.status}`);
  }

  return res.json();
}

export const api = {
  // Auth
  login: async (email: string, password: string) => {
    const u = await fetchApi<User>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    if (u.token) {
      localStorage.setItem('tech_inject_token', u.token);
    }
    return u;
  },

  signup: async (email: string, password: string) => {
    const u = await fetchApi<User>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    if (u.token) {
      localStorage.setItem('tech_inject_token', u.token);
    }
    return u;
  },

  logout: async () => {
    localStorage.removeItem('tech_inject_token');
    return fetchApi<{ message: string }>('/auth/logout', { method: 'POST' });
  },

  getMe: () => fetchApi<User>('/auth/me'),

  // Public / Customer Components
  getComponents: (category?: string, search?: string) => {
    const params = new URLSearchParams();
    if (category && category !== 'All') params.append('category', category);
    if (search) params.append('search', search);
    const query = params.toString() ? `?${params.toString()}` : '';
    return fetchApi<ComponentSummary[]>(`/components${query}`);
  },

  getComponent: (slug: string) => fetchApi<ComponentDetail>(`/components/${slug}`),

  getInstallPayload: (slug: string) => fetchApi<any>(`/components/${slug}/install`),

  getAgentPrompt: (slug: string) => fetchApi<{ slug: string; name: string; prompt: string }>(`/components/${slug}/agent-prompt`),

  // Admin APIs
  createComponent: (data: any) =>
    fetchApi<ComponentDetail>('/admin/components', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateComponent: (id: number, data: any) =>
    fetchApi<ComponentDetail>(`/admin/components/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  publishComponent: (id: number) =>
    fetchApi<ComponentDetail>(`/admin/components/${id}/publish`, {
      method: 'POST',
    }),

  unpublishComponent: (id: number) =>
    fetchApi<ComponentDetail>(`/admin/components/${id}/unpublish`, {
      method: 'POST',
    }),

  deleteComponent: (id: number) =>
    fetchApi<{ message: string }>(`/admin/components/${id}`, {
      method: 'DELETE',
    }),

  // Admin Customer APIs
  getCustomers: () => fetchApi<User[]>('/admin/customers'),

  grantPremium: (userId: number) =>
    fetchApi<User>(`/admin/customers/${userId}/grant-premium`, { method: 'POST' }),

  revokePremium: (userId: number) =>
    fetchApi<User>(`/admin/customers/${userId}/revoke-premium`, { method: 'POST' }),
};
