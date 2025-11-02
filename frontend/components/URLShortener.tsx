'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { urlService, CreateURLPayload, URLData } from '@/lib/api'
import toast from 'react-hot-toast'
import { Copy, Check, Link, QrCode } from 'lucide-react'
import { QRCodeSVG } from 'qrcode.react'

export default function URLShortener() {
  const [shortenedURL, setShortenedURL] = useState<URLData | null>(null)
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)
  const [showQR, setShowQR] = useState(false)

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CreateURLPayload>()

  const onSubmit = async (data: CreateURLPayload) => {
    setLoading(true)
    try {
      const result = await urlService.createURL(data)
      setShortenedURL(result)
      toast.success('Short URL created successfully!')
      reset()
    } catch (error: any) {
      const errorMsg = error.response?.data?.original_url?.[0] || 
                      error.response?.data?.custom_code?.[0] ||
                      'Failed to create short URL'
      toast.error(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = () => {
    if (shortenedURL) {
      navigator.clipboard.writeText(shortenedURL.short_url)
      setCopied(true)
      toast.success('Copied to clipboard!')
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Original URL */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Enter your long URL
          </label>
          <div className="relative">
            <Link className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="url"
              {...register('original_url', {
                required: 'URL is required',
                pattern: {
                  value: /^https?:\/\/.+/,
                  message: 'Please enter a valid URL',
                },
              })}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
              placeholder="https://example.com/very-long-url"
            />
          </div>
          {errors.original_url && (
            <p className="mt-1 text-sm text-red-600">{errors.original_url.message}</p>
          )}
        </div>

        {/* Custom Code (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Custom short code (optional)
          </label>
          <input
            type="text"
            {...register('custom_code', {
              minLength: { value: 3, message: 'Minimum 3 characters' },
              maxLength: { value: 20, message: 'Maximum 20 characters' },
              pattern: {
                value: /^[a-zA-Z0-9]+$/,
                message: 'Only letters and numbers allowed',
              },
            })}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
            placeholder="my-custom-code"
          />
          {errors.custom_code && (
            <p className="mt-1 text-sm text-red-600">{errors.custom_code.message}</p>
          )}
        </div>

        {/* Title (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Title (optional)
          </label>
          <input
            type="text"
            {...register('title')}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
            placeholder="My Website"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Creating...' : 'Shorten URL'}
        </button>
      </form>

      {/* Result */}
      {shortenedURL && (
        <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Your shortened URL is ready!
          </h3>
          
          <div className="flex items-center gap-2 mb-4">
            <input
              type="text"
              value={shortenedURL.short_url}
              readOnly
              className="flex-1 px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900"
            />
            <button
              onClick={copyToClipboard}
              className="px-4 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
            >
              {copied ? <Check size={20} /> : <Copy size={20} />}
            </button>
            <button
              onClick={() => setShowQR(!showQR)}
              className="px-4 py-3 bg-gray-700 hover:bg-gray-800 text-white rounded-lg transition-colors"
            >
              <QrCode size={20} />
            </button>
          </div>

          {showQR && (
            <div className="flex justify-center p-4 bg-white rounded-lg">
              <QRCodeSVG value={shortenedURL.short_url} size={200} />
            </div>
          )}

          <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
            <div>
              <span className="font-medium">Short Code:</span> {shortenedURL.short_code}
            </div>
            <div>
              <span className="font-medium">Clicks:</span> {shortenedURL.clicks}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
