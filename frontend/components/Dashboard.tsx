'use client'

import { useState, useEffect } from 'react'
import { analyticsService, DashboardStats } from '@/lib/api'
import toast from 'react-hot-toast'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Link2, MousePointerClick, Users, TrendingUp } from 'lucide-react'

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const data = await analyticsService.getDashboardStats()
      setStats(data)
    } catch (error) {
      toast.error('Failed to fetch analytics')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 text-center text-gray-500">
        No analytics data available
      </div>
    )
  }

  const statCards = [
    {
      title: 'Total URLs',
      value: stats.total_urls,
      icon: Link2,
      color: 'blue',
    },
    {
      title: 'Total Clicks',
      value: stats.total_clicks,
      icon: MousePointerClick,
      color: 'green',
    },
    {
      title: 'Unique Visitors',
      value: stats.total_unique_visitors,
      icon: Users,
      color: 'purple',
    },
    {
      title: 'Clicks This Week',
      value: stats.clicks_this_week,
      icon: TrendingUp,
      color: 'orange',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <div
            key={index}
            className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">{stat.title}</p>
                <p className="text-3xl font-bold text-gray-900">
                  {stat.value.toLocaleString()}
                </p>
              </div>
              <div className={`p-3 rounded-full bg-${stat.color}-100`}>
                <stat.icon className={`text-${stat.color}-600`} size={24} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Top URLs */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Top URLs</h2>
        {stats.top_urls.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No URLs yet</p>
        ) : (
          <div className="space-y-4">
            {stats.top_urls.map((url, index) => (
              <div
                key={url.short_code}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center gap-4">
                  <span className="text-2xl font-bold text-gray-400">
                    #{index + 1}
                  </span>
                  <div>
                    <p className="font-semibold text-gray-900">
                      {url.title || url.short_code}
                    </p>
                    <p className="text-sm text-gray-600 truncate max-w-md">
                      {url.original_url}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-blue-600">
                    {url.clicks.toLocaleString()}
                  </p>
                  <p className="text-sm text-gray-500">clicks</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Chart */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Activity Overview</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={[
              { name: 'Today', clicks: stats.clicks_today },
              { name: 'This Week', clicks: stats.clicks_this_week },
            ]}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="clicks" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
