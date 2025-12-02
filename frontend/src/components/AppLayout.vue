<template>
  <div class="app-layout">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>AIPortal</h2>
      </div>
      
      <nav class="nav-menu">
        <div 
          v-for="section in sections" 
          :key="section.id"
          :class="['nav-item', { active: activeSection === section.id }]"
          @click="switchSection(section.id)"
        >
          <span class="nav-icon">{{ section.icon }}</span>
          <span class="nav-text">{{ section.name }}</span>
        </div>
      </nav>
    </aside>

    <!-- 右侧区域（包含标题栏、主要内容和右侧边栏） -->
    <div class="right-area">
      <!-- 固定标题栏 -->
      <div class="header-content">
        <h1 class="page-title">庆安AI智能门户</h1>
        <p class="page-subtitle">Artificial Intelligence for Qing'an</p>
      </div>
      
      <div class="right-content-wrapper">
        <!-- 右侧内容区 -->
        <main class="main-content">
          <slot></slot>
        </main>
        
        <!-- 右侧边栏 -->
        <aside class="sidebar-right">
          <!-- 热门智能小工具 -->
          <div class="card">
            <div class="card-header">
              <h3>智能小工具HOT <span class="hot-icon">🔥</span></h3>
            </div>
            <div class="card-content">
              <div 
                class="tool-item" 
                style="border-left-color: #ff6b6b;"
                @click="openLink(APP_LINKS.HOT_TOOLS.CONTRACT_REVIEW, '_blank', { 
                  name: '合同审查助手', 
                  icon: '📋', 
                  category: '管理智能', 
                  url: APP_LINKS.HOT_TOOLS.CONTRACT_REVIEW 
                })"
              >
                合同审查助手
              </div>
              <div 
                class="tool-item" 
                style="border-left-color: #4ecdc4;"
                @click="openLink(APP_LINKS.HOT_TOOLS.IMAGE_STYLE_TRANSFER, '_blank', { 
                  name: '图片风格转换器', 
                  icon: '🎨', 
                  category: '多媒体', 
                  url: APP_LINKS.HOT_TOOLS.IMAGE_STYLE_TRANSFER 
                })"
              >
                图片风格转换器
              </div>
              <div 
                class="tool-item" 
                style="border-left-color: #45b7d1;"
                @click="openLink(APP_LINKS.HOT_TOOLS.SPEECH_TO_TEXT, '_blank', { 
                  name: '语音转文字助手', 
                  icon: '🎤', 
                  category: '语音识别', 
                  url: APP_LINKS.HOT_TOOLS.SPEECH_TO_TEXT 
                })"
              >
                语音转文字助手
              </div>
              <div 
                class="tool-item" 
                style="border-left-color: #96ceb4;"
                @click="openLink(APP_LINKS.HOT_TOOLS.CODE_COMPLETION, '_blank', { 
                  name: '代码智能补全器', 
                  icon: '💻', 
                  category: '开发工具', 
                  url: APP_LINKS.HOT_TOOLS.CODE_COMPLETION 
                })"
              >
                代码智能补全器
              </div>
              <div 
                class="tool-item" 
                style="border-left-color: #ffeaa7;"
                @click="openLink(APP_LINKS.HOT_TOOLS.SENTIMENT_ANALYSIS, '_blank', { 
                  name: '情感分析检测器', 
                  icon: '😊', 
                  category: '文本分析', 
                  url: APP_LINKS.HOT_TOOLS.SENTIMENT_ANALYSIS 
                })"
              >
                情感分析检测器
              </div>
            </div>
          </div>

          <!-- 智能助手指南 -->
          <div class="card">
            <div class="card-header">
              <h3>智能助手指南</h3>
            </div>
            <div class="card-content">
              <div class="guide-item" style="border-left-color: #45b7d1; cursor: pointer;" @click="openLink(APP_LINKS.AI_GUIDES.DATA_CLEANING, '_blank', { 
                name: 'AI数据清洗入门指南', 
                icon: '🧹', 
                category: 'AI指南', 
                url: APP_LINKS.AI_GUIDES.DATA_CLEANING 
              })">AI数据清洗入门指南</div>
              <div class="guide-item" style="border-left-color: #96ceb4; cursor: pointer;" @click="openLink(APP_LINKS.AI_GUIDES.VISUALIZATION_TOOLS, '_blank', { 
                name: '智能可视化工具教程', 
                icon: '📊', 
                category: 'AI指南', 
                url: APP_LINKS.AI_GUIDES.VISUALIZATION_TOOLS 
              })">智能可视化工具教程</div>
              <div class="guide-item" style="border-left-color: #ffeaa7; cursor: pointer;" @click="openLink(APP_LINKS.AI_GUIDES.ANOMALY_DETECTION, '_blank', { 
                name: '异常检测算法使用', 
                icon: '🔍', 
                category: 'AI指南', 
                url: APP_LINKS.AI_GUIDES.ANOMALY_DETECTION 
              })">异常检测算法使用</div>
              <div class="guide-item" style="border-left-color: #ff6b6b; cursor: pointer;" @click="openLink(APP_LINKS.AI_GUIDES.EXPORT_BEST_PRACTICES, '_blank', { 
                name: '数据导出最佳实践', 
                icon: '📤', 
                category: 'AI指南', 
                url: APP_LINKS.AI_GUIDES.EXPORT_BEST_PRACTICES 
              })">数据导出最佳实践</div>
              <div class="guide-item" style="border-left-color: #74b9ff; cursor: pointer;" @click="openLink(APP_LINKS.AI_GUIDES.MODEL_TRAINING, '_blank', { 
                name: 'AI模型训练基础', 
                icon: '🏋️', 
                category: 'AI指南', 
                url: APP_LINKS.AI_GUIDES.MODEL_TRAINING 
              })">AI模型训练基础</div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { APP_LINKS, openLink } from '../config/links.js'

// 当前选中的功能区
const activeSection = ref(1)

// 功能区配置
const sections = [
  { id: 1, name: '功能区 1', icon: '🏠' },
  { id: 2, name: '功能区 2', icon: '📊' },
  { id: 3, name: '功能区 3', icon: '💬' },
  { id: 4, name: '功能区 4', icon: '⚙️' },
  { id: 5, name: '功能区 5', icon: '📁' }
]

// 切换功能区
const switchSection = (id) => {
  activeSection.value = id
  // 触发自定义事件通知父组件
  emit('section-change', id)
}

// 定义事件
const emit = defineEmits(['section-change'])
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 右侧区域 */
.right-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 固定标题栏 */
.header-content {
  position: sticky;
  top: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.8rem 2rem;
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

/* 右侧内容包装器 */
.right-content-wrapper {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧导航栏 */
.sidebar {
  width: 260px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
}

.sidebar-header h2 {
  margin: 0;
  color: #4a5568;
  font-size: 1.5rem;
  font-weight: 700;
}

.nav-menu {
  flex: 1;
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  color: #34495e;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  border-left-color: rgba(102, 126, 234, 0.5);
}

.nav-item.active {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-left-color: #667eea;
  border-radius: 0 8px 8px 0;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
}

.nav-item.active .nav-text {
  color: #2c3e50;
  font-weight: 600;
}

.nav-icon {
  font-size: 1.2rem;
  margin-right: 0.75rem;
  width: 24px;
  text-align: center;
}

.nav-text {
  color: #4a5568;
  font-size: 0.95rem;
  font-weight: 500;
}

/* 右侧内容区 */
.main-content {
  flex: 1;
  padding: 0.5rem 2rem 2rem;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.3);
}

/* 右侧边栏 */
.sidebar-right {
  width: 280px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-left: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem;
  overflow-y: auto;
  overflow-x: hidden;
  color: #0f172a;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  padding: 1rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
}

.card-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
}

.card-header h3 {
  margin: 0;
  color: #4a5568;
  font-size: 14px;
  font-weight: 700;
}

.hot-icon {
  margin-left: 5px;
  font-size: 14px;
  vertical-align: middle;
}

.tool-item {
  padding: 10px 15px;
  margin-bottom: 8px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.7);
  border-left: 4px solid;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #4a5568;
  font-weight: 600;
  font-size: 14px;
  user-select: none;
}

.tool-item:hover {
  transform: translateX(5px);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.guide-item {
  padding: 10px 15px;
  margin-bottom: 8px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.6);
  border-left: 3px solid;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #4a5568;
  font-weight: 600;
  font-size: 14px;
}

.guide-item:hover {
  transform: translateX(2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-layout {
    flex-direction: column;
    height: 100vh;
  }

  .sidebar {
    width: 100%;
    height: auto;
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }

  .nav-menu {
    flex-direction: row;
    overflow-x: auto;
    padding: 0.5rem;
  }

  .nav-item {
    flex-shrink: 0;
    padding: 0.8rem 1rem;
    font-size: 0.9rem;
    border-left: none;
    border-bottom: 3px solid transparent;
  }

  .nav-item.active {
    border-left: none;
    border-bottom-color: #667eea;
  }

  .nav-icon {
    margin-right: 0;
    margin-bottom: 0.25rem;
  }

  .right-content-wrapper {
    flex-direction: column;
  }
  
  .header-content {
    padding: 0.8rem 1.5rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .page-subtitle {
    font-size: 0.9rem;
  }

  .main-content {
    padding: 1rem;
  }

  .sidebar-right {
    width: 100%;
    border-left: none;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
  }
}
</style>