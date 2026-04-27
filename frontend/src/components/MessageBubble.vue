<template>
  <div :class="bubbleClasses">
    <!-- User Message -->
    <div v-if="message.role === 'user'" class="bg-primary text-white rounded-2xl px-4 py-3 max-w-[80%] ml-auto">
      <p class="text-sm md:text-base">{{ message.content }}</p>
    </div>

    <!-- Assistant Message -->
    <div v-else class="max-w-[100%]">
      <!-- Text Response -->
      <div v-if="message.type === 'text'" class="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-100 max-w-2xl">
        <p class="text-sm md:text-base text-gray-800 whitespace-pre-wrap">{{ message.content }}</p>
      </div>

      <!-- Images Response -->
      <div v-else-if="message.type === 'images'" class="space-y-3">
        <div class="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-100">
          <p class="text-sm text-gray-600">Generated {{ message.images.length }} image(s):</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl">
          <div 
            v-for="(url, index) in message.images" 
            :key="index"
            class="relative group overflow-hidden rounded-xl shadow-lg hover:shadow-xl transition-shadow bg-gray-100"
          >
            <!-- Loading State -->
            <div v-if="loadingImages[index]" class="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-gray-200 to-gray-300 z-10">
              <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-primary mx-auto mb-2"></div>
                <p class="text-xs text-gray-700 font-medium">Loading image...</p>
                <p class="text-xs text-gray-500 mt-1">This may take a moment</p>
              </div>
            </div>

            <!-- Error State -->
            <div v-else-if="errorImages[index]" class="absolute inset-0 flex items-center justify-center bg-red-50 z-10">
              <div class="text-center p-4">
                <p class="text-sm text-red-600 font-medium mb-2">⚠️ Load Failed</p>
                <p class="text-xs text-red-500 mb-3">{{ errorImages[index] }}</p>
                <button 
                  @click="retryImage(index, url)"
                  class="text-xs bg-red-600 text-white px-2 py-1 rounded hover:bg-red-700"
                >
                  Retry
                </button>
              </div>
            </div>

            <!-- Image Container -->
            <div class="aspect-square overflow-hidden bg-gray-200">
              <img 
                :src="getProxyUrl(url)" 
                :alt="`Generated image ${index + 1}`"
                class="w-full h-full object-cover"
                @load="onImageLoad(index)"
                @error="handleImageError(index)"
                @click="openImage(url)"
                loading="lazy"
              />
            </div>
            
            <!-- Hover Overlay -->
            <div v-if="!loadingImages[index] && !errorImages[index]" class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity cursor-pointer"></div>
            
            <!-- Click to Enlarge Badge -->
            <div v-if="!loadingImages[index] && !errorImages[index]" class="absolute bottom-2 right-2 bg-black bg-opacity-70 text-white px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity">
              🔍 Enlarge
            </div>
          </div>
        </div>
      </div>

      <!-- Hybrid Response -->
      <div v-else-if="message.type === 'hybrid'" class="space-y-4">
        <div class="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-100 max-w-2xl">
          <p class="text-sm md:text-base text-gray-800 whitespace-pre-wrap">{{ message.content.text }}</p>
        </div>
        
        <div v-if="message.content.images && message.content.images.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl">
          <div 
            v-for="(url, index) in message.content.images" 
            :key="index"
            class="relative group overflow-hidden rounded-xl shadow-lg hover:shadow-xl transition-shadow bg-gray-100"
          >
            <!-- Loading State -->
            <div v-if="loadingImages[`hybrid-${index}`]" class="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-gray-200 to-gray-300 z-10">
              <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-primary mx-auto mb-2"></div>
                <p class="text-xs text-gray-700 font-medium">Loading...</p>
              </div>
            </div>

            <!-- Error State -->
            <div v-else-if="errorImages[`hybrid-${index}`]" class="absolute inset-0 flex items-center justify-center bg-red-50 z-10">
              <div class="text-center p-4">
                <p class="text-sm text-red-600 font-medium mb-2">⚠️ Load Failed</p>
                <button 
                  @click="retryImage(`hybrid-${index}`, url)"
                  class="text-xs bg-red-600 text-white px-2 py-1 rounded hover:bg-red-700"
                >
                  Retry
                </button>
              </div>
            </div>

            <!-- Image Container -->
            <div class="aspect-square overflow-hidden bg-gray-200">
              <img 
                :src="getProxyUrl(url)" 
                :alt="`Generated image ${index + 1}`"
                class="w-full h-full object-cover"
                @load="() => onImageLoad(`hybrid-${index}`)"
                @error="() => handleImageError(`hybrid-${index}`)"
                @click="openImage(url)"
                loading="lazy"
              />
            </div>
            
            <!-- Hover Overlay -->
            <div v-if="!loadingImages[`hybrid-${index}`] && !errorImages[`hybrid-${index}`]" class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity cursor-pointer"></div>
            
            <!-- Click to Enlarge Badge -->
            <div v-if="!loadingImages[`hybrid-${index}`] && !errorImages[`hybrid-${index}`]" class="absolute bottom-2 right-2 bg-black bg-opacity-70 text-white px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity">
              🔍 Enlarge
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

const loadingImages = ref({})
const errorImages = ref({})

const bubbleClasses = computed(() => {
  return [
    'mb-6',
    'animate-fadeIn'
  ]
})

// Initialize loading state for images
const initializeLoading = () => {
  if (props.message.type === 'images') {
    props.message.images.forEach((_, index) => {
      loadingImages.value[index] = true
    })
  } else if (props.message.type === 'hybrid' && props.message.content.images) {
    props.message.content.images.forEach((_, index) => {
      loadingImages.value[`hybrid-${index}`] = true
    })
  }
}

// Use backend proxy for all images
const getProxyUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('data:')) return url
  
  return `/api/image-proxy?url=${encodeURIComponent(url)}`
}

const onImageLoad = (index) => {
  loadingImages.value[index] = false
  delete errorImages.value[index]
  console.log(`✅ Image ${index} loaded`)
}

const handleImageError = (index) => {
  loadingImages.value[index] = false
  errorImages.value[index] = "Failed to load. Server may be slow. Try retry."
  console.error(`❌ Image ${index} failed to load`)
}

const retryImage = (index, url) => {
  console.log(`🔄 Retrying image ${index}`)
  loadingImages.value[index] = true
  delete errorImages.value[index]
  
  // Force reload by changing src
  const img = document.querySelector(`img[alt="Generated image ${String(index).split('-')[0]}"]`)
  if (img) {
    img.src = getProxyUrl(url)
  }
}

const openImage = (url) => {
  if (url && !url.startsWith('data:')) {
    window.open(url, '_blank')
  }
}

// Initialize on mount
initializeLoading()
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>