import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 300000  // 5 minutes timeout
})

// Add response interceptor for better error handling
api.interceptors.response.use(
  response => {
    console.log('✅ API response successful')
    return response
  },
  error => {
    console.error('❌ API error:', error.response?.data || error.message)
    throw error
  }
)

export const sendMessage = async (message, history = []) => {
  try {
    console.log('📤 Sending message:', message)
    console.log('📋 History count:', history.length)
    
    // Validate message
    if (!message || !message.trim()) {
      throw new Error('Message cannot be empty')
    }
    
    // Validate and clean history
    const cleanHistory = history.map(item => ({
      role: item.role || 'user',
      content: String(item.content || '').substring(0, 5000)  // Limit content length
    })).filter(item => item.content.trim())  // Remove empty items
    
    console.log('📋 Cleaned history:', cleanHistory.length)
    
    const response = await api.post('/chat', {
      message: message.trim(),
      history: cleanHistory
    })
    
    console.log('📥 Raw response data:', response.data)
    
    const data = response.data
    
    // Validate response
    if (!data.type) {
      throw new Error('Invalid response format: missing type')
    }
    
    // Validate and normalize response based on type
    if (data.type === 'text') {
      if (typeof data.data !== 'string') {
        throw new Error('Text response must be a string')
      }
    } 
    else if (data.type === 'images') {
      if (!Array.isArray(data.data)) {
        data.data = [data.data].filter(url => url)
      }
    } 
    else if (data.type === 'hybrid') {
      if (typeof data.data !== 'object' || !data.data.text || !data.data.images) {
        throw new Error('Hybrid response must have text and images')
      }
      // Ensure images is an array
      if (!Array.isArray(data.data.images)) {
        data.data.images = [data.data.images].filter(img => img)
      }
    }
    
    console.log('✅ Response validated:', data.type)
    return data
  } catch (error) {
    console.error('❌ API Error:', error)
    
    if (error.response?.status === 500) {
      const detail = error.response.data?.detail
      throw new Error(detail || 'Server error. Please try again.')
    } else if (error.response?.status === 400) {
      throw new Error(error.response.data?.detail || 'Bad request.')
    } else if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout. Please try again.')
    } else if (error.message) {
      throw new Error(error.message)
    } else {
      throw new Error('Failed to connect to server. Please try again.')
    }
  }
}

export const healthCheck = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    throw error
  }
}

export default api