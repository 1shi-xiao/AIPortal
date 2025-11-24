<template>
  <AppLayout @section-change="handleSectionChange">
    <component :is="currentComponent" />
  </AppLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import AppLayout from './components/AppLayout.vue'
import HomeView from './views/HomeView.vue'
import AIAssistant from './views/AiAssistant.vue'
import AIProducts from './views/AIProducts.vue'
import Workflow from './views/Workflow.vue'
import ModelLibrary from './views/ModelLibrary.vue'

// 当前选中的功能区
const activeSection = ref(1)

// 组件映射
const componentMap = {
  1: HomeView,
  2: AIAssistant,
  3: AIProducts,
  4: Workflow,
  5: ModelLibrary
}

// 计算属性：根据当前选中的功能区返回对应的组件
const currentComponent = computed(() => {
  return componentMap[activeSection.value] || HomeView
})

// 处理功能区切换
const handleSectionChange = (sectionId) => {
  activeSection.value = sectionId
}
</script>

<style scoped>
/* App.vue 样式已迁移到各个组件中 */
</style>
