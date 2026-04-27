<template>
  <div class="flex items-center space-x-2 text-gray-500">
    <div class="flex space-x-1">
      <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0ms"></div>
      <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 150ms"></div>
      <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 300ms"></div>
    </div>
    <span class="text-sm">{{ message }}</span>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: 'Generating...'
  }
})
</script>

<style scoped>
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-bounce {
  animation: bounce 0.6s infinite;
}
</style>