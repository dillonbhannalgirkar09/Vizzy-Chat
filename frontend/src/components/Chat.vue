<template>
  <div class="flex flex-col h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-4 py-4 shadow-sm">
      <div class="max-w-4xl mx-auto flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
            </svg>
          </div>
          <div>
            <h1 class="text-xl font-bold text-gray-900">Vizzy Chat</h1>
            <p class="text-xs text-gray-500">Creative AI Assistant</p>
          </div>
        </div>
        <button 
          @click="clearChat"
          class="text-sm text-gray-600 hover:text-gray-900 px-3 py-1 rounded-lg hover:bg-gray-100 transition-colors"
        >
          Clear Chat
        </button>
      </div>
    </header>

    <!-- Messages Container -->
    <div 
      ref="messagesContainer"
      class="flex-1 overflow-y-auto px-4 py-6"
    >
      <div class="max-w-4xl mx-auto">
        <!-- Welcome Message -->
        <div v-if="messages.length === 0" class="text-center py-12">
          <div class="w-20 h-20 bg-gradient-to-br from-primary to-secondary rounded-2xl flex items-center justify-center mx-auto mb-6">
            <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 mb-3">Welcome to Vizzy Chat</h2>
          <p class="text-gray-600 mb-8 max-w-md mx-auto">
            Your creative AI companion. Generate stunning visuals, craft engaging stories, or create both together.
          </p>
          
          <!-- Example Prompts -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
            <button
              v-for="example in examplePrompts"
              :key="example"
              @click="useExample(example)"
              class="text-left p-4 bg-white rounded-xl border border-gray-200 hover:border-primary hover:shadow-md transition-all"
            >
              <p class="text-sm text-gray-700">{{ example }}</p>
            </button>
          </div>
        </div>

        <!-- Messages -->
        <div v-else>
          <MessageBubble 
            v-for="(message, index) in messages"
            :key="index"
            :message="message"
          />
        </div>

        <!-- Loading Indicator -->
        <div v-if="isLoading" class="mb-4">
          <LoadingIndicator message="Creating magic..." />
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="bg-white border-t border-gray-200 px-4 py-4">
      <div class="max-w-4xl mx-auto">
        <form @submit.prevent="sendMessage" class="flex items-end space-x-3">
          <div class="flex-1">
            <textarea
              v-model="inputMessage"
              @keydown.enter.exact.prevent="sendMessage"
              placeholder="Describe what you want to create..."
              rows="1"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
              style="max-height: 150px;"
              :disabled="isLoading"
            ></textarea>
          </div>
          <button
            type="submit"
            :disabled="!inputMessage.trim() || isLoading"
            class="bg-gradient-to-r from-primary to-secondary text-white px-6 py-3 rounded-xl font-medium hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <span>Send</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </form>
        <p class="text-xs text-gray-500 mt-2 text-center">
          Press Enter to send • Shift + Enter for new line
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import MessageBubble from './MessageBubble.vue'
import LoadingIndicator from './LoadingIndicator.vue'
import { sendMessage as apiSendMessage } from '../services/api'

const messages = ref([])
const inputMessage = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)

const examplePrompts = [
  "Paint something that feels like a peaceful morning",
  "Turn this into a renaissance-style artwork",
  "Create a dreamlike vision board for my goals",
  "Generate a short story about adventure and visualize it"
]

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// Build conversation history for API
// Only include user and assistant text messages
const buildHistory = () => {
  const history = []
  
  for (const msg of messages.value) {
    try {
      if (msg.role === 'user') {
        // Add user messages
        history.push({
          role: 'user',
          content: msg.content || ''
        })
      } else if (msg.role === 'assistant' && msg.type === 'text') {
        // Only add text responses to history
        history.push({
          role: 'assistant',
          content: msg.content || ''
        })
      } else if (msg.role === 'assistant' && msg.type === 'hybrid') {
        // For hybrid, only add the text part
        history.push({
          role: 'assistant',
          content: msg.content?.text || ''
        })
      }
      // Skip image-only responses from history
    } catch (error) {
      console.error('Error building history item:', error)
    }
  }
  
  return history
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value) return

  const userMessage = inputMessage.value.trim()
  
  // Add user message to chat
  messages.value.push({
    role: 'user',
    content: userMessage
  })

  inputMessage.value = ''
  scrollToBottom()

  isLoading.value = true

  try {
    console.log('📤 Sending message:', userMessage)
    
    // Build history from current messages
    const history = buildHistory()
    
    console.log('📋 History:', history)
    console.log('📋 History length:', history.length)
    
    // Call API
    const response = await apiSendMessage(userMessage, history)

    console.log('📥 API Response:', response)
    console.log('📥 Response type:', response.type)
    console.log('📥 Response data:', response.data)

    // Add assistant response
    if (response.type === 'text') {
      console.log('📝 Adding text response')
      messages.value.push({
        role: 'assistant',
        type: 'text',
        content: response.data
      })
    } 
    else if (response.type === 'images') {
      console.log('🎨 Adding image response')
      // Handle both string URLs and array of URLs
      const imageUrls = Array.isArray(response.data) ? response.data : [response.data]
      
      messages.value.push({
        role: 'assistant',
        type: 'images',
        images: imageUrls
      })
    } 
    else if (response.type === 'hybrid') {
      console.log('🔄 Adding hybrid response')
      console.log('   Text:', response.data.text?.substring(0, 50))
      console.log('   Images:', response.data.images?.length)
      
      // Ensure images is an array
      const imageUrls = Array.isArray(response.data.images) 
        ? response.data.images 
        : [response.data.images].filter(img => img)
      
      messages.value.push({
        role: 'assistant',
        type: 'hybrid',
        content: {
          text: response.data.text || '',
          images: imageUrls
        }
      })
    }
    else {
      throw new Error(`Unknown response type: ${response.type}`)
    }

    scrollToBottom()
  } catch (error) {
    console.error('❌ Error sending message:', error)
    
    // Remove the user message if API failed
    if (messages.value.length > 0 && messages.value[messages.value.length - 1].role === 'user') {
      messages.value.pop()
    }
    
    messages.value.push({
      role: 'assistant',
      type: 'text',
      content: `Sorry, I encountered an error: ${error.message}. Please try again.`
    })
  } finally {
    isLoading.value = false
  }
}

const useExample = (example) => {
  inputMessage.value = example
  sendMessage()
}

const clearChat = () => {
  if (confirm('Clear all messages?')) {
    messages.value = []
  }
}
</script>