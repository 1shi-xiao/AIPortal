<template>
  <div class="model-library-container">
    <!-- 最近浏览工具 -->
    <div class="recent-tools">
      <div class="section-header">
        <h2>最近浏览记录</h2>
        <div class="header-actions">
          <button class="toggle-btn" @click="toggleExpand" v-if="recentTools.length > 4">
            {{ isExpanded ? '收起' : '展开' }}
          </button>
          <button class="clear-btn" @click="clearRecentTools" v-if="recentTools.length > 0">
            清空
          </button>
        </div>
      </div>
      <div class="tools-grid">
        <div v-if="recentTools.length === 0" class="empty-state">
          <p>暂无最近浏览记录</p>
        </div>
        <div 
          v-for="(tool, index) in (isExpanded ? recentTools : recentTools.slice(0, 4))" 
          :key="'recent-' + index"
          class="tool-card"
          @click="navigateToTool(tool)"
        >
          <div class="tool-icon" v-html="getToolIcon(tool.name)"></div>
          <div class="tool-info">
            <div class="tool-name">{{ tool.name }}</div>
            <div class="tool-time">{{ formatTime(tool.timestamp) }}</div>
          </div>
          <div class="tool-actions">
            <button class="favorite-btn" @click.stop="toggleFavorite(tool)">
              {{ isFavorite(tool) ? '❤️' : '🤍' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 我的收藏 -->
    <div class="favorite-tools">
      <div class="section-header">
        <h2>我的收藏</h2>
        <div class="header-actions">
          <button class="toggle-btn" @click="toggleFavoriteExpand" v-if="favoriteTools.length > 4">
            {{ isFavoriteExpanded ? '收起' : '展开' }}
          </button>
        </div>
      </div>
      <div class="tools-grid">
        <div v-if="favoriteTools.length === 0" class="empty-state">
          <p>暂无收藏工具</p>
        </div>
        <div 
          v-for="(tool, index) in (isFavoriteExpanded ? favoriteTools : favoriteTools.slice(0, 4))" 
          :key="'favorite-' + index"
          class="tool-card"
          @click="navigateToTool(tool)"
        >
          <div class="tool-icon" v-html="getToolIcon(tool.name)"></div>
          <div class="tool-info">
            <div class="tool-name">{{ tool.name }}</div>
            <div class="tool-category">{{ tool.category }}</div>
          </div>
          <div class="tool-actions">
            <button class="favorite-btn" @click.stop="toggleFavorite(tool)">
              ❤️
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 推荐工具（供用户添加到收藏） -->
    <div class="recommended-tools">
      <div class="section-header">
        <h2>推荐工具</h2>
      </div>
      <div class="tools-grid">
        <div 
          v-for="tool in recommendedTools" 
          :key="'recommended-' + tool.id"
          class="tool-card"
          @click="navigateToTool(tool)"
        >
          <div class="tool-icon" v-html="getToolIcon(tool.name)"></div>
          <div class="tool-info">
            <div class="tool-name">{{ tool.name }}</div>
            <div class="tool-category">{{ tool.category }}</div>
          </div>
          <div class="tool-actions">
            <button class="favorite-btn" @click.stop="toggleFavorite(tool)">
              {{ isFavorite(tool) ? '❤️' : '🤍' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { openLink } from '../config/links.js'
import toolService from '../services/toolService.js'

// 最近浏览工具列表
const recentTools = ref([])

// 收藏工具列表
const favoriteTools = ref([])

// 最近浏览工具展开/收起状态
const isExpanded = ref(false)

// 我的收藏工具展开/收起状态
const isFavoriteExpanded = ref(false)

// 切换最近浏览工具展开/收起状态
function toggleExpand() {
  isExpanded.value = !isExpanded.value
}

// 切换我的收藏工具展开/收起状态
function toggleFavoriteExpand() {
  isFavoriteExpanded.value = !isFavoriteExpanded.value
}

// 根据工具名称获取对应的SVG图标
function getToolIcon(toolName) {
  const iconMap = {
    '合同审查助手': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3,3H21V21H3V3M7,7V9H9V7H7M11,7V9H13V7H11M15,7V9H17V7H15M7,11V13H9V11H7M11,11V13H13V11H11M15,11V13H17V11H15M7,15V17H9V15H7M11,15V17H13V15H11M15,15V17H17V15H15Z"/></svg>',
    '数据分析工具': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3,3H7V7H3V3M3,11H7V15H3V11M3,19H7V21H3V19M11,3H15V7H11V3M11,11H15V15H11V11M11,19H15V21H11V19M19,3H21V7H19V3M19,11H21V15H19V11M19,19H21V21H19V19M7,11H11V15H7V11Z"/></svg>',
    '智能推荐系统': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,15L19.55,7.45L21,9L12,18L3,9L4.45,7.45L12,15Z"/></svg>',
    '文档处理工具': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M14,2H6C4.9,2,4,2.9,4,4v16c0,1.1,0.9,2,2,2h12c1.1,0,2-0.9,2-2V8L14,2z M16,18H8V16h8V18z M16,14H8V12h10V13z M13,9V3.5L18.5,9H13z"/></svg>',
    '设备监控系统': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19,3H5C3.89,3,3,3.89,3,5v14c0,1.11,0.89,2,2,2h14c1.11,0,2-0.89,2-2V5C21,3.89,20.11,3,19,3z M19,19H5V5h14V19z M13,17H7v-2h6V17z M17,13H7v-2h10V13z M17,9H7V7h10V9z"/></svg>',
    '预测性维护': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,2L4.5,20.29L5.21,21L6.11,19H20V17H6.11L6.83,15H18V13H5.08L5.67,11H18V9H4.26L4.96,7H18V5H3.24L3.94,3H12V2Z"/></svg>',
    '质量检测分析': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9,16.17L4.83,12L3.41,13.41L9,19L21,7L19.59,5.59L9,16.17Z"/></svg>',
    '能源优化系统': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M13,8H11V13L16.2,16.2L17,14.9L13,12.2V8M19,3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.9 20.1,3 19,3Z"/></svg>',
    '通用大模型': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/></svg>',
    '代码大模型': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z"/></svg>',
    '多模态大模型': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M14,17H7V15H14V17M17,13H7V11H17V13M17,9H7V7H17V9M19,3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.9 20.1,3 19,3Z"/></svg>',
    '图片风格转换器': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,10C10.34,10 9,11.34 9,13C9,14.66 10.34,16 12,16C13.66,16 15,14.66 15,13C15,11.34 13.66,10 12,10M12,14C11.45,14 11,13.55 11,13C11,12.45 11.45,12 12,12C12.55,12 13,12.45 13,13C13,13.55 12.55,14 12,14M19,3H5C3.9,3 3,3.9 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.9 20.1,3 19,3M19,19H5V5H19V19Z"/></svg>',
    '语音转文字助手': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,14C13.1,14 14,13.1 14,12C14,10.9 13.1,10 12,10C10.9,10 10,10.9 10,12C10,13.1 10.9,14 12,14M12,3C7.03,3 3,7.03 3,12C3,16.97 7.03,21 12,21C16.97,21 21,16.97 21,12C21,7.03 16.97,3 12,3M12,19C8.13,19 5,15.87 5,12C5,8.13 8.13,5 12,5C15.87,5 19,8.13 19,12C19,15.87 15.87,19 12,19M12,8C13.1,8 14,8.9 14,10V12C14,13.1 13.1,14 12,14C10.9,14 10,13.1 10,12V10C10,8.9 10.9,8 12,8Z"/></svg>',
    '代码智能补全器': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M14,2L6,8V21H13V22H15V21H22V8L14,2Z"/></svg>',
    '情感分析检测器': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z"/></svg>',
    '更多工具': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M12,10A2,2 0 0,0 10,12A2,2 0 0,0 12,14A2,2 0 0,0 14,12A2,2 0 0,0 12,10M12,19.2C9.5,19.2 7.29,17.92 6,15.98C6.03,13.99 10,12.9 12,12.9C13.99,12.9 17.97,13.99 18,15.98C16.71,17.92 14.5,19.2 12,19.2Z"/></svg>',
    '更多工业工具': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M12,10A2,2 0 0,0 10,12A2,2 0 0,0 12,14A2,2 0 0,0 14,12A2,2 0 0,0 12,10M12,19.2C9.5,19.2 7.29,17.92 6,15.98C6.03,13.99 10,12.9 12,12.9C13.99,12.9 17.97,13.99 18,15.98C16.71,17.92 14.5,19.2 12,19.2Z"/></svg>',
    '更多大模型工具': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M12,10A2,2 0 0,0 10,12A2,2 0 0,0 12,14A2,2 0 0,0 14,12A2,2 0 0,0 12,10M12,19.2C9.5,19.2 7.29,17.92 6,15.98C6.03,13.99 10,12.9 12,12.9C13.99,12.9 17.97,13.99 18,15.98C16.71,17.92 14.5,19.2 12,19.2Z"/></svg>',
    '新增演示工具': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M13,17H11V15H13V17M13,13H11V7H13V13Z"/></svg>',
    '演示工具2': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,3C16.97,3 21,6.58 21,11C21,15.42 16.97,19 12,19C7.03,19 3,15.42 3,11C3,6.58 7.03,3 12,3M12,5C8.69,5 6,8.24 6,12C6,15.76 8.69,19 12,19C15.31,19 18,15.76 18,12C18,8.24 15.31,5 12,5Z"/></svg>'
  };
  
  return iconMap[toolName] || '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4Z"/></svg>';
}

// 推荐工具列表
const recommendedTools = ref([
  { id: 1, name: '合同审查助手', icon: '📋', category: '管理智能', url: 'https://cn.bing.com/search?q=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B%E4%BD%A0%E5%B0%B1%E7%9F%A5%E9%81%93&form=ANNTH1' },
  { id: 2, name: '图片风格转换器', icon: '🎨', category: '多媒体', url: 'https://cn.bing.com/search?q=%E5%9B%BE%E7%89%87%E9%A3%8E%E6%A0%BC%E8%BD%AC%E6%8D%A2%E5%B7%A5%E5%85%B7&form=ANNTH1' },
  { id: 3, name: '语音转文字助手', icon: '🎤', category: '语音识别', url: 'https://cn.bing.com/search?q=%E8%AF%AD%E9%9F%B3%E8%BD%AC%E6%96%87%E5%AD%97%E5%B7%A5%E5%85%B7&form=ANNTH1' },
  { id: 4, name: '代码智能补全器', icon: '💻', category: '开发工具', url: 'https://cn.bing.com/search?q=%E4%BB%A3%E7%A0%81%E6%99%BA%E8%83%BD%E8%A1%A5%E5%85%A8%E5%B7%A5%E5%85%B7&form=ANNTH1' },
  { id: 5, name: '情感分析检测器', icon: '😊', category: '文本分析', url: 'https://cn.bing.com/search?q=%E6%83%85%E6%84%9F%E5%88%86%E6%9E%90%E5%B7%A5%E5%85%B7&form=ANNTH1' },
  { id: 6, name: '数据分析工具', icon: '📊', category: '数据分析', url: 'https://cn.bing.com/search?q=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B7%A5%E5%85%B7&form=ANNTH1' }
])

// 从工具服务加载数据
onMounted(() => {
  loadData()
  
  // 监听全局工具访问事件
  window.addEventListener('tool-accessed', handleGlobalToolAccess)
})

onUnmounted(() => {
  // 移除事件监听
  window.removeEventListener('tool-accessed', handleGlobalToolAccess)
})

// 加载数据
function loadData() {
  recentTools.value = toolService.getRecentTools()
  favoriteTools.value = toolService.getFavoriteTools()
  
  // 模拟一些最近浏览记录（实际项目中应该在工具访问时记录）
  if (recentTools.value.length === 0) {
    const mockRecent = [
      { name: '合同审查助手', icon: '📋', category: '管理智能', url: 'https://cn.bing.com/search?q=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B%E4%BD%A0%E5%B0%B1%E7%9F%A5%E9%81%93&form=ANNTH1', timestamp: Date.now() - 3600000 },
      { name: '图片风格转换器', icon: '🎨', category: '多媒体', url: 'https://cn.bing.com/search?q=%E5%9B%BE%E7%89%87%E9%A3%8E%E6%A0%BC%E8%BD%AC%E6%8D%A2%E5%B7%A5%E5%85%B7&form=ANNTH1', timestamp: Date.now() - 7200000 },
      { name: '数据分析工具', icon: '📊', category: '数据分析', url: 'https://cn.bing.com/search?q=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B7%A5%E5%85%B7&form=ANNTH1', timestamp: Date.now() - 10800000 }
    ]
    
    // 保存模拟数据到localStorage
    mockRecent.forEach(tool => {
      toolService.recordToolAccess(tool)
    })
    
    // 重新加载数据
    recentTools.value = toolService.getRecentTools()
  }
}

// 处理全局工具访问事件
function handleGlobalToolAccess(event) {
  const tool = event.detail
  recentTools.value = toolService.getRecentTools()
}

// 导航到工具
function navigateToTool(tool) {
  // 更新最近浏览（通过工具服务）
  toolService.recordToolAccess(tool)
  
  // 更新本地状态
  recentTools.value = toolService.getRecentTools()
  
  // 打开工具链接
  openLink(tool.url, '_blank', tool)
}

// 切换收藏状态
function toggleFavorite(tool) {
  // 使用工具服务切换收藏状态
  toolService.toggleFavorite(tool)
  
  // 更新本地状态
  favoriteTools.value = toolService.getFavoriteTools()
}

// 检查是否已收藏
function isFavorite(tool) {
  return toolService.isFavorite(tool)
}

// 清空最近浏览
function clearRecentTools() {
  // 使用工具服务清空最近浏览
  toolService.clearRecentTools()
  
  // 更新本地状态
  recentTools.value = toolService.getRecentTools()
}

// 格式化时间
function formatTime(timestamp) {
  return toolService.formatTime(timestamp)
}
</script>

<style scoped>
.model-library-container {
  padding: 2rem;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

/* 通用区块样式 */
.recent-tools,
.favorite-tools,
.recommended-tools {
  max-width: 1200px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.toggle-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  background: #5a67d8;
  transform: translateY(-1px);
}

.section-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.75rem;
  font-weight: 600;
}

.clear-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  color: #718096;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  color: #e53e3e;
}

/* 工具网格布局 */
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  min-height: 200px;
}

/* 空状态 */
.empty-state {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 150px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  color: #a0aec0;
  font-size: 1.1rem;
  font-weight: 500;
}

/* 工具卡片 */
.tool-card {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  padding: 1.25rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.tool-card:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.tool-icon {
  font-size: 2rem;
  margin-right: 1.25rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  color: white;
  flex-shrink: 0;
}

.tool-info {
  flex: 1;
  min-width: 0;
}

.tool-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
  font-size: 1.05rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tool-time,
.tool-category {
  color: #718096;
  font-size: 0.85rem;
  font-weight: 500;
}

.tool-actions {
  display: flex;
  align-items: center;
  margin-left: 0.75rem;
}

.favorite-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
}

.favorite-btn:hover {
  background: rgba(0, 0, 0, 0.05);
  transform: scale(1.1);
}

/* 工具类型颜色标识 */
.tool-card:nth-child(1) .tool-icon { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); }
.tool-card:nth-child(2) .tool-icon { background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); }
.tool-card:nth-child(3) .tool-icon { background: linear-gradient(135deg, #45b7d1 0%, #2980b9 100%); }
.tool-card:nth-child(4) .tool-icon { background: linear-gradient(135deg, #96ceb4 0%, #8fbc8f 100%); }
.tool-card:nth-child(5) .tool-icon { background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); }
.tool-card:nth-child(6) .tool-icon { background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); }
.tool-card:nth-child(7) .tool-icon { background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%); }
.tool-card:nth-child(8) .tool-icon { background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%); }

/* 响应式设计 */
@media (max-width: 768px) {
  .model-library-container {
    padding: 1rem;
    gap: 2rem;
  }
  
  .section-header h2 {
    font-size: 1.5rem;
  }
  
  .tools-grid {
    grid-template-columns: 1fr;
    padding: 1.25rem;
    gap: 1rem;
  }
  
  .tool-card {
    padding: 1rem;
  }
  
  .tool-icon {
    font-size: 1.75rem;
    width: 45px;
    height: 45px;
    margin-right: 1rem;
  }
}

@media (max-width: 480px) {
  .model-library-container {
    padding: 0.75rem;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .tools-grid {
    padding: 1rem;
  }
  
  .tool-card {
    flex-direction: column;
    text-align: center;
    padding: 1.25rem;
  }
  
  .tool-icon {
    margin-right: 0;
    margin-bottom: 1rem;
  }
  
  .tool-actions {
    margin-left: 0;
    margin-top: 0.75rem;
  }
}
</style>