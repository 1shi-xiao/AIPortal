<template>
  <div class="workflow-container">
    <div class="settings-panel">
      <h2>系统设置</h2>
      <div class="settings-form">
        <div class="form-group">
          <label>主题模式</label>
          <select>
            <option>浅色模式</option>
            <option>深色模式</option>
            <option>跟随系统</option>
          </select>
        </div>
        <div class="form-group">
          <label>语言设置</label>
          <select>
            <option>中文</option>
            <option>English</option>
          </select>
        </div>
        <div class="form-group">
          <label>通知设置</label>
          <input type="checkbox" /> 启用桌面通知
        </div>
        <button class="save-btn">保存设置</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 工作流组件逻辑
</script>

<style scoped>
.workflow-container {
  padding: 2rem;
  height: 100%;
  overflow-y: auto;
}

/* 设置面板样式 */
.settings-panel {
  max-width: 800px;
}

.settings-panel h2 {
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 600;
}

.settings-form {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4a5568;
  font-weight: 600;
  font-size: 1rem;
}

.form-group select,
.form-group input[type="text"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.8);
  outline: none;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.form-group select:focus,
.form-group input[type="text"]:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input[type="checkbox"] {
  margin-right: 0.5rem;
  transform: scale(1.2);
}

.save-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

@media (max-width: 768px) {
  .workflow-container {
    padding: 1rem;
  }
  
  .settings-form {
    padding: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
}
</style>