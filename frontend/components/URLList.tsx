'use client'

import { useState, useEffect } from 'react'
import { urlService, URLData } from '@/lib/api'
import toast from 'react-hot-toast'
import { ExternalLink, Trash2, TrendingUp, Calendar } from 'lucide-react'
import { format } from 'date-fns'

export default function URLList() {
  const [urls, setUrls] = useState<URLData[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  useEffect(() => {
    fetchURLs()
  }, [])

  const fetchURLs = async () => {
    try {
      const response = await urlService.getURLs({ search })
      setUrls(response.results)
    } catch (error) {
      toast.error('Failed to fetch URLs')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this URL?')) return

    try {
      await urlService.deleteURL(id)
      setUrls(urls.filter(url => url.id !== id))
      toast.success('URL deleted successfully')
    } catch (error) {
      toast.error('Failed to delete URL')
    }
  }

  const handleSearch = () => {
    setLoading(true)
    fetchURLs()
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">My URLs</h2>
        <div className="flex gap-2">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Search..."
          />
          <button
            onClick={handleSearch}
            className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
          >
            Search
          </button>
        </div>
      </div>

      {urls.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p className="text-lg">No URLs found</p>
          <p className="text-sm">Create your first short URL to get started</p>
        </div>
      ) : (
        <div className="space-y-4">
          {urls.map((url) => (
            <div
              key={url.id}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <a
                      href={url.short_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-lg font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1"
                    >
                      {url.short_code}
                      <ExternalLink size={16} />
                    </a>
                    {url.custom_code && (
                      <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded">
                        Custom
                      </span>
                    )}
                  </div>
                  
                  <p className="text-sm text-gray-600 mb-2 truncate">
                    {url.original_url}
                  </p>
                  
                  {url.title && (
                    <p className="text-sm font-medium text-gray-800 mb-2">
                      {url.title}
                    </p>
                  )}
                  
                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    <span className="flex items-center gap-1">
                      <TrendingUp size={14} />
                      {url.clicks} clicks ({url.unique_clicks} unique)
                    </span>
                    <span className="flex items-center gap-1">
                      <Calendar size={14} />
                      {format(new Date(url.created_at), 'MMM dd, yyyy')}
                    </span>
                  </div>
                </div>
                
                <button
                  onClick={() => handleDelete(url.id)}
                  className="ml-4 p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
