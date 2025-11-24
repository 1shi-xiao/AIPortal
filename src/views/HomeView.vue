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
        <span class="more-link">更多 &gt;&gt;&gt;</span>
      </div>
      <div class="cards-grid">
        <!-- 工具卡片将通过组件动态渲染 -->
        <div class="feature-card"><div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3,3H21V21H3V3M7,7V9H9V7H7M11,7V9H13V7H11M15,7V9H17V7H15M7,11V13H9V11H7M11,11V13H13V11H11M15,11V13H17V11H15M7,15V17H9V15H7M11,15V17H13V15H11M15,15V17H17V15H15Z"/></svg></div><div class="card-title">合同审查助手</div></div>
        <div class="feature-card"><div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3,3H7V7H3V3M3,11H7V15H3V11M3,19H7V21H3V19M11,3H15V7H11V3M11,11H15V15H11V11M11,19H15V21H11V19M19,3H21V7H19V3M19,11H21V15H19V11M19,19H21V21H19V19M7,11H11V15H7V11Z"/></svg></div><div class="card-title">数据分析工具</div></div>
        <div class="feature-card"><div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12,15L19.55,7.45L21,9L12,18L3,9L4.45,7.45L12,15Z"/></svg></div><div class="card-title">智能推荐系统</div></div>
        <div class="feature-card"><div class="card-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M14,2H6C4.9,2,4,2.9,4,4v16c0,1.1,0.9,2,2,2h12c1.1,0,2-0.9,2-2V8L14,2z M16,18H8V16h8V18z M16,14H8V12h8V14z M13,9V3.5L18.5,9H13z"/></svg></div><div class="card-title">文档处理工具</div></div>
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
// 首页组件逻辑
</script>

<style scoped>
.home-container {
  padding: 2rem;
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
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.95);
}

.card-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  color: white;
}

.card-title {
  font-size: 1.1rem;
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