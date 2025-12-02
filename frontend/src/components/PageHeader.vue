<template>
  <div class="header-content">
    <h1 class="page-title">{{ title }}</h1>
    <p class="page-subtitle">{{ subtitle }}</p>
  </div>
</template>

<script setup>
// 定义标题和副标题属性
const props = defineProps({
  title: {
    type: String,
    required: true,
    default: 'AI智能门户'
  },
  subtitle: {
    type: String,
    required: false,
    default: '探索人工智能的无限可能'
  }
})
</script>

<style scoped>
.header-content {
  position: sticky;
  top: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
  backdrop-filter: blur(10px);
}

.page-title {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1.2;
}

.page-subtitle {
  margin: 0.5rem 0 0;
  font-size: 1rem;
  opacity: 0.9;
  font-weight: 400;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 1rem 1.5rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .page-subtitle {
    font-size: 0.9rem;
  }
}
</style>