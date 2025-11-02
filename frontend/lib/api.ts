import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface URLData {
  id: number
  original_url: string
  short_code: string
  short_url: string
  custom_code: boolean
  title?: string
  description?: string
  clicks: number
  unique_clicks: number
  last_accessed?: string
  is_active: boolean
  expires_at?: string
  is_expired: boolean
  created_at: string
  updated_at: string
  qr_code_url?: string
}

export interface CreateURLPayload {
  original_url: string
  custom_code?: string
  title?: string
  description?: string
  expires_at?: string
}

export interface DashboardStats {
  total_urls: number
  total_clicks: number
  total_unique_visitors: number
  clicks_today: number
  clicks_this_week: number
  top_urls: Array<{
    short_code: string
    original_url: string
    clicks: number
    title?: string
  }>
}

export interface URLStats {
  total_clicks: number
  unique_clicks: number
  last_accessed?: string
  clicks_by_date: Array<{ clicked_at__date: string; count: number }>
  clicks_by_country: Record<string, number>
  clicks_by_device: Record<string, number>
  clicks_by_browser: Record<string, number>
  top_referrers: Array<{ referer: string; count: number }>
}

// API methods
export const urlService = {
  createURL: async (data: CreateURLPayload): Promise<URLData> => {
    const response = await api.post('/urls/', data)
    return response.data
  },

  getURLs: async (params?: {
    page?: number
    search?: string
    order_by?: string
  }): Promise<{ results: URLData[]; count: number }> => {
    const response = await api.get('/urls/', { params })
    return response.data
  },

  getURL: async (id: number): Promise<URLData> => {
    const response = await api.get(`/urls/${id}/`)
    return response.data
  },

  updateURL: async (id: number, data: Partial<CreateURLPayload>): Promise<URLData> => {
    const response = await api.patch(`/urls/${id}/`, data)
    return response.data
  },

  deleteURL: async (id: number): Promise<void> => {
    await api.delete(`/urls/${id}/`)
  },

  getURLStats: async (id: number): Promise<URLStats> => {
    const response = await api.get(`/urls/${id}/stats/`)
    return response.data
  },

  getPopularURLs: async (limit: number = 10): Promise<URLData[]> => {
    const response = await api.get('/urls/popular/', { params: { limit } })
    return response.data
  },

  getRecentURLs: async (limit: number = 10): Promise<URLData[]> => {
    const response = await api.get('/urls/recent/', { params: { limit } })
    return response.data
  },
}

export const analyticsService = {
  getDashboardStats: async (): Promise<DashboardStats> => {
    const response = await api.get('/analytics/dashboard/')
    return response.data
  },

  getTrends: async (days: number = 30) => {
    const response = await api.get('/analytics/trends/', { params: { days } })
    return response.data
  },
}
