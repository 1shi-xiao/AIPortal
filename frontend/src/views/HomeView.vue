<template>
  <div class="home-container">
    <!-- 搜索栏区域 -->
    <div class="search-container">
      <div class="search-bar">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="#999" class="search-icon">
          <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
        </svg>
        <input type="text" placeholder="搜索..." class="search-input">
        <button class="search-button">搜索</button>
      </div>
    </div>

    <!-- 数据卡片区域 -->
    <div class="data-cards-container">
      <div class="section-header">
        <h3>管理智能工具</h3>
        <span class="more-link" style="cursor: pointer;" @click="openLink(APP_LINKS.EXTERNAL.MORE_TOOLS, '_blank', { 
  name: '更多工具', 
  icon: '🔧', 
  category: '外部链接', 
  url: APP_LINKS.EXTERNAL.MORE_TOOLS 
})">更多 &gt;&gt;&gt;</span>
      </div>
      <div class="cards-grid">
        <!-- 工具卡片将通过组件动态渲染 -->
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.CONTRACT_REVIEW, '_blank', { 
  name: '合同审查助手', 
  icon: '📋', 
  category: '管理智能', 
  url: APP_LINKS.TOOLS.CONTRACT_REVIEW 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3,3H21V21H3V3M7,7V9H9V7H7M11,7V9H13V7H11M15,7V9H17V7H15M7,11V13H9V11H7M11,11V13H13V11H11M15,11V13H17V11H15M7,15V17H9V15H7M11,15V17H13V15H11M15,15V17H17V15H15Z"/></svg></div>
  <div class="card-title">合同审查助手</div>
</div>
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.DATA_ANALYSIS, '_blank', { 
  name: '数据分析工具', 
  icon: '📊', 
  category: '数据智能', 
  url: APP_LINKS.TOOLS.DATA_ANALYSIS 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3,3H7V7H3V3M3,11H7V15H3V11M3,19H7V21H3V19M11,3H15V7H11V3M11,11H15V15H11V11M11,19H15V21H11V19M19,3H21V7H19V3M19,11H21V15H19V11M19,19H21V21H19V19M7,11H11V15H7V11Z"/></svg></div>
  <div class="card-title">数据分析工具</div>
</div>
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.INTELLIGENT_RECOMMENDATION, '_blank', { 
  name: '智能推荐系统', 
  icon: '💡', 
  category: '推荐系统', 
  url: APP_LINKS.TOOLS.INTELLIGENT_RECOMMENDATION 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,15L19.55,7.45L21,9L12,18L3,9L4.45,7.45L12,15Z"/></svg></div>
  <div class="card-title">智能推荐系统</div>
</div>
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.DOCUMENT_PROCESSING, '_blank', { 
  name: '文档处理工具', 
  icon: '📄', 
  category: '文档管理', 
  url: APP_LINKS.TOOLS.DOCUMENT_PROCESSING 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M14,2H6C4.9,2,4,2.9,4,4v16c0,1.1,0.9,2,2,2h12c1.1,0,2-0.9,2-2V8L14,2z M16,18H8V16h8V18z M16,14H8V12h10V13z M13,9V3.5L18.5,9H13z"/></svg></div>
  <div class="card-title">文档处理工具</div>
</div>
      </div>
    </div>

    <!-- 工业智能工具区域 -->
    <div class="data-cards-container">
      <div class="section-header">
        <h3>工业智能工具</h3>
        <span class="more-link" style="cursor: pointer;" @click="openLink(APP_LINKS.EXTERNAL.MORE_INDUSTRIAL_TOOLS, '_blank', { 
  name: '更多工业工具', 
  icon: '🏭', 
  category: '外部链接', 
  url: APP_LINKS.EXTERNAL.MORE_INDUSTRIAL_TOOLS 
})">更多 &gt;&gt;&gt;</span>
      </div>
      <div class="cards-grid">
        <!-- 工业智能工具卡片 -->
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.EQUIPMENT_MONITORING, '_blank', { 
  name: '设备监控系统', 
  icon: '📡', 
  category: '工业智能', 
  url: APP_LINKS.TOOLS.EQUIPMENT_MONITORING 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19,3H5C3.89,3,3,3.89,3,5v14c0,1.11,0.89,2,2,2h14c1.11,0,2-0.89,2-2V5C21,3.89,20.11,3,19,3z M19,19H5V5h14V19z M13,17H7v-2h6V17z M17,13H7v-2h10V13z M17,9H7V7h10V9z"/></svg></div>
  <div class="card-title">设备监控系统</div>
</div>
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.PREDICTIVE_MAINTENANCE, '_blank', { 
  name: '预测性维护', 
  icon: '🔮', 
  category: '工业智能', 
  url: APP_LINKS.TOOLS.PREDICTIVE_MAINTENANCE 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,2L4.5,20.29L5.21,21L6.11,19H20V17H6.11L6.83,15H18V13H5.08L5.67,11H18V9H4.26L4.96,7H18V5H3.24L3.94,3H12V2Z"/></svg></div>
  <div class="card-title">预测性维护</div>
</div>
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.QUALITY_INSPECTION, '_blank', { 
  name: '质量检测分析', 
  icon: '✅', 
  category: '工业智能', 
  url: APP_LINKS.TOOLS.QUALITY_INSPECTION 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3,3H21V21H3V3M17,17H19V19H17V17M17,13H19V15H17V13M17,9H19V11H17V9M17,5H19V7H17V5M13,17H15V19H13V17M13,13H15V15H13V13M13,9H15V11H13V9M13,5H15V7H13V5M9,17H11V19H9V17M9,13H11V15H9V13M9,9H11V11H9V9M9,5H11V7H9V5M5,17H7V19H5V17M5,13H7V15H5V13M5,9H7V11H5V9M5,5H7V7H5V5Z"/></svg></div>
  <div class="card-title">质量检测分析</div>
</div>
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.ENERGY_OPTIMIZATION, '_blank', { 
  name: '能耗优化工具', 
  icon: '⚡', 
  category: '工业智能', 
  url: APP_LINKS.TOOLS.ENERGY_OPTIMIZATION 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3.5,18.49L9,13H12L13.5,14.5L15.5,12.5L18,15V10H19V16L12,23L5,16V10H6V15L8.5,12.5L10.5,14.5L12,13L13.5,14.5L15,13H18L13.5,18.49V23H10.5V18.49L6,14H3.5L8,19L12,15L16,19L20.5,14H18L12.5,19.49V23H9.5V19.49L3.5,13H1L6,18L12,12L18,18L23,13H20.5L15,18.49V23H12.5V18.49L3.5,18.49Z"/></svg></div>
  <div class="card-title">能耗优化工具</div>
</div>
      </div>
    </div>

    <!-- 大模型区域 -->
    <div class="data-cards-container">
      <div class="section-header">
        <h3>大模型工具</h3>
        <span class="more-link" style="cursor: pointer;" @click="openLink(APP_LINKS.EXTERNAL.MORE_LLM_TOOLS, '_blank', { 
  name: '更多LLM工具', 
  icon: '🤖', 
  category: '外部链接', 
  url: APP_LINKS.EXTERNAL.MORE_LLM_TOOLS 
})">更多 &gt;&gt;&gt;</span>
      </div>
      <div class="cards-grid cards-grid-three">
        <!-- 大模型工具卡片 -->
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.GENERAL_LLM, '_blank', { 
  name: '通用大模型', 
  icon: '🧠', 
  category: '大模型工具', 
  url: APP_LINKS.TOOLS.GENERAL_LLM 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/></svg></div>
  <div class="card-title">通用大模型</div>
</div>
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.CODE_LLM, '_blank', { 
  name: '代码大模型', 
  icon: '💻', 
  category: '大模型工具', 
  url: APP_LINKS.TOOLS.CODE_LLM 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z"/></svg></div>
  <div class="card-title">代码大模型</div>
</div>
        <div class="feature-card" style="cursor: pointer;" @click="openLink(APP_LINKS.TOOLS.MULTIMODAL_LLM, '_blank', { 
  name: '多模态大模型', 
  icon: '🖼️', 
  category: '大模型工具', 
  url: APP_LINKS.TOOLS.MULTIMODAL_LLM 
})">
  <div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M14,17H7V15H14V17M17,13H7V11H17V13M17,9H7V7H17V9M19,3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.9 20.1,3 19,3Z"/></svg></div>
  <div class="card-title">多模态大模型</div>
</div>
      </div>
    </div>

    <!-- 列表项区域 -->
    <div class="list-section">
      <div class="section-header">
        <h3>最近使用记录</h3>
        <span class="more-link">更多 &gt;&gt;&gt;</span>
      </div>
      <div class="records-list">
        <!-- 记录项将通过组件动态渲染 -->
        <div class="record-item"><div class="record-title">合同分析报告</div><div class="record-meta"><span class="record-time">2023-10-15 14:30</span><span class="record-status status-completed">已完成</span></div></div>
        <div class="record-item"><div class="record-title">销售数据预测</div><div class="record-meta"><span class="record-time">2023-10-14 09:15</span><span class="record-status status-processing">处理中</span></div></div>
        <div class="record-item"><div class="record-title">客户画像生成</div><div class="record-meta"><span class="record-time">2023-10-12 16:45</span><span class="record-status status-completed">已完成</span></div></div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 导入链接配置和工具函数
import { APP_LINKS, openLink } from '../config/links.js';
</script>

<style scoped>
.home-container {
  padding: 1rem 2rem 2rem;
  height: 100%;
  overflow-y: auto;
}

/* 搜索栏样式 */
.search-container {
  margin-bottom: 2rem;
}

.search-bar {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 0.75rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.search-icon {
  margin-right: 0.75rem;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 1rem;
  color: #4a5568;
}

.search-button {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.search-button:hover {
  background: #5a67d8;
  transform: translateY(-1px);
}

/* 数据卡片样式 */
.data-cards-container {
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
}

.more-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.3s ease;
}

.more-link:hover {
  color: #5a67d8;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.cards-grid-three {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 0.75rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 140px;
}

.feature-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.95);
}

.card-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.75rem;
  color: white;
}

.card-icon svg {
  width: 20px;
  height: 20px;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

/* 列表样式 */
.list-section {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.record-item:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateX(5px);
}

.record-title {
  font-weight: 600;
  color: #2c3e50;
}

.record-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.record-time {
  color: #718096;
  font-size: 0.9rem;
}

.record-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-completed {
  background: #48bb78;
  color: white;
}

.status-processing {
  background: #ed8936;
  color: white;
}

@media (max-width: 768px) {
  .home-container {
    padding: 1rem;
  }
  
  .cards-grid {
    grid-template-columns: 1fr;
  }
  
  .record-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .record-meta {
    width: 100%;
    justify-content: space-between;
  }
}
</style>