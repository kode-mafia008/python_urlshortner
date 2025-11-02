'use client'

import { useState } from 'react'
import URLShortener from '@/components/URLShortener'
import URLList from '@/components/URLList'
import Dashboard from '@/components/Dashboard'
import { Link2, BarChart3, List } from 'lucide-react'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'shorten' | 'list' | 'analytics'>('shorten')

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            URL Shortener
          </h1>
          <p className="text-xl text-gray-600">
            Create short, memorable links with powerful analytics
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex rounded-lg border border-gray-200 bg-white p-1 shadow-sm">
            <button
              onClick={() => setActiveTab('shorten')}
              className={`flex items-center px-6 py-3 rounded-md font-medium transition-colors ${
                activeTab === 'shorten'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <Link2 className="w-5 h-5 mr-2" />
              Shorten URL
            </button>
            <button
              onClick={() => setActiveTab('list')}
              className={`flex items-center px-6 py-3 rounded-md font-medium transition-colors ${
                activeTab === 'list'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <List className="w-5 h-5 mr-2" />
              My URLs
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`flex items-center px-6 py-3 rounded-md font-medium transition-colors ${
                activeTab === 'analytics'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <BarChart3 className="w-5 h-5 mr-2" />
              Analytics
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="max-w-6xl mx-auto">
          {activeTab === 'shorten' && <URLShortener />}
          {activeTab === 'list' && <URLList />}
          {activeTab === 'analytics' && <Dashboard />}
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-600">
          <p>Built with Django, PostgreSQL, Next.js, and TypeScript</p>
        </footer>
      </div>
    </main>
  )
}
