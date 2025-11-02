import { urlService, analyticsService } from '@/services/api'

// Mock fetch
global.fetch = jest.fn()

describe('URL Service', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('createURL', () => {
    it('creates a new URL', async () => {
      const mockResponse = {
        id: 1,
        original_url: 'https://example.com',
        short_code: 'abc123',
        short_url: 'http://localhost:8000/abc123/',
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await urlService.createURL({
        original_url: 'https://example.com',
      })

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/urls/',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
        })
      )
      expect(result).toEqual(mockResponse)
    })

    it('throws error on failed request', async () => {
      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ error: 'Invalid URL' }),
      })

      await expect(
        urlService.createURL({ original_url: 'invalid' })
      ).rejects.toThrow()
    })
  })

  describe('getURLs', () => {
    it('fetches URLs list', async () => {
      const mockResponse = {
        results: [
          {
            id: 1,
            short_code: 'abc123',
            original_url: 'https://example.com',
          },
        ],
        count: 1,
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await urlService.getURLs()

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/urls/'),
        expect.any(Object)
      )
      expect(result).toEqual(mockResponse)
    })
  })

  describe('deleteURL', () => {
    it('deletes a URL', async () => {
      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
      })

      await urlService.deleteURL(1)

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/urls/1/'),
        expect.objectContaining({
          method: 'DELETE',
        })
      )
    })
  })
})

describe('Analytics Service', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('getDashboardStats', () => {
    it('fetches dashboard statistics', async () => {
      const mockStats = {
        total_urls: 10,
        total_clicks: 100,
        total_unique_visitors: 50,
        clicks_today: 5,
        clicks_this_week: 25,
        top_urls: [],
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockStats,
      })

      const result = await analyticsService.getDashboardStats()

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/analytics/dashboard/'),
        expect.any(Object)
      )
      expect(result).toEqual(mockStats)
    })
  })

  describe('getTrends', () => {
    it('fetches trend data', async () => {
      const mockTrends = {
        period_days: 7,
        trends: [],
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockTrends,
      })

      const result = await analyticsService.getTrends()

      expect(fetch).toHaveBeenCalled()
      expect(result).toEqual(mockTrends)
    })

    it('fetches trends with custom days', async () => {
      const mockTrends = {
        period_days: 30,
        trends: [],
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockTrends,
      })

      await analyticsService.getTrends(30)

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('days=30'),
        expect.any(Object)
      )
    })
  })
})
