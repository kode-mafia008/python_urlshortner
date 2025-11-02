import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import URLShortener from '@/components/URLShortener'
import { urlService } from '@/services/api'

// Mock the API service
jest.mock('@/services/api')
const mockUrlService = urlService as jest.Mocked<typeof urlService>

// Mock toast
jest.mock('react-hot-toast', () => ({
  success: jest.fn(),
  error: jest.fn(),
}))

describe('URLShortener Component', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders the form correctly', () => {
    render(<URLShortener />)
    
    expect(screen.getByPlaceholderText(/https:\/\/example.com/i)).toBeInTheDocument()
    expect(screen.getByText(/Enter your long URL/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Shorten URL/i })).toBeInTheDocument()
  })

  it('submits the form with valid URL', async () => {
    const mockResponse = {
      id: 1,
      original_url: 'https://www.example.com',
      short_code: 'abc123',
      short_url: 'http://localhost:8000/abc123/',
      title: 'Test',
      clicks: 0,
      created_at: new Date().toISOString(),
    }

    mockUrlService.createURL.mockResolvedValue(mockResponse)

    render(<URLShortener />)

    const urlInput = screen.getByPlaceholderText(/https:\/\/example.com/i)
    const submitButton = screen.getByRole('button', { name: /Shorten URL/i })

    fireEvent.change(urlInput, { target: { value: 'https://www.example.com' } })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(mockUrlService.createURL).toHaveBeenCalledWith({
        original_url: 'https://www.example.com',
        custom_code: '',
        title: '',
      })
    })
  })

  it('shows error for invalid URL', async () => {
    render(<URLShortener />)

    const urlInput = screen.getByPlaceholderText(/https:\/\/example.com/i)
    const submitButton = screen.getByRole('button', { name: /Shorten URL/i })

    fireEvent.change(urlInput, { target: { value: 'not-a-valid-url' } })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/Please enter a valid URL/i)).toBeInTheDocument()
    })
  })

  it('handles custom code input', async () => {
    const mockResponse = {
      id: 1,
      original_url: 'https://www.example.com',
      short_code: 'mycustom',
      short_url: 'http://localhost:8000/mycustom/',
      title: '',
      clicks: 0,
      created_at: new Date().toISOString(),
    }

    mockUrlService.createURL.mockResolvedValue(mockResponse)

    render(<URLShortener />)

    const urlInput = screen.getByPlaceholderText(/https:\/\/example.com/i)
    const customCodeInput = screen.getByPlaceholderText(/my-custom-code/i)
    const submitButton = screen.getByRole('button', { name: /Shorten URL/i })

    fireEvent.change(urlInput, { target: { value: 'https://www.example.com' } })
    fireEvent.change(customCodeInput, { target: { value: 'mycustom' } })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(mockUrlService.createURL).toHaveBeenCalledWith({
        original_url: 'https://www.example.com',
        custom_code: 'mycustom',
        title: '',
      })
    })
  })

  it('displays shortened URL after successful creation', async () => {
    const mockResponse = {
      id: 1,
      original_url: 'https://www.example.com',
      short_code: 'abc123',
      short_url: 'http://localhost:8000/abc123/',
      title: '',
      clicks: 0,
      created_at: new Date().toISOString(),
    }

    mockUrlService.createURL.mockResolvedValue(mockResponse)

    render(<URLShortener />)

    const urlInput = screen.getByPlaceholderText(/https:\/\/example.com/i)
    const submitButton = screen.getByRole('button', { name: /Shorten URL/i })

    fireEvent.change(urlInput, { target: { value: 'https://www.example.com' } })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByDisplayValue('http://localhost:8000/abc123/')).toBeInTheDocument()
    })
  })

  it('shows loading state while submitting', async () => {
    mockUrlService.createURL.mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    )

    render(<URLShortener />)

    const urlInput = screen.getByPlaceholderText(/https:\/\/example.com/i)
    const submitButton = screen.getByRole('button', { name: /Shorten URL/i })

    fireEvent.change(urlInput, { target: { value: 'https://www.example.com' } })
    fireEvent.click(submitButton)

    expect(submitButton).toBeDisabled()
  })
})
