import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      // TODO: Implement token refresh logic
      // For now, just redirect to login
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/auth/login'
      }
    }
    
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register: (data: any) => api.post('/auth/register', data),
  login: (data: any) => api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
}

// Job Seeker API
export const seekerAPI = {
  getProfile: () => api.get('/seekers/me'),
  updateProfile: (data: any) => api.put('/seekers/me', data),
  uploadResume: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/seekers/me/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

// Jobs API
export const jobsAPI = {
  search: (params: any) => api.get('/jobs', { params }),
  getJob: (id: string) => api.get(`/jobs/${id}`),
  create: (data: any) => api.post('/jobs', data),
  update: (id: string, data: any) => api.put(`/jobs/${id}`, data),
  getMyJobs: () => api.get('/jobs/my-jobs'),
}

// Applications API
export const applicationsAPI = {
  apply: (data: any) => api.post('/applications', data),
  getMyApplications: () => api.get('/applications'),
  getApplication: (id: string) => api.get(`/applications/${id}`),
}

// Employer API
export const employerAPI = {
  getProfile: () => api.get('/employers/me'),
  updateProfile: (data: any) => api.put('/employers/me', data),
}
