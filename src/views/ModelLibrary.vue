<template>
  <div class="model-library-container">
    <div class="file-manager">
      <h2>文件管理</h2>
      <div class="file-grid">
        <div class="file-item">
          <div class="file-icon">📄</div>
          <div class="file-info">
            <div class="file-name">项目文档.pdf</div>
            <div class="file-size">2.3 MB</div>
          </div>
        </div>
        <div class="file-item">
          <div class="file-icon">📊</div>
          <div class="file-info">
            <div class="file-name">数据分析.xlsx</div>
            <div class="file-size">1.5 MB</div>
          </div>
        </div>
        <div class="file-item">
          <div class="file-icon">🖼️</div>
          <div class="file-info">
            <div class="file-name">设计图.png</div>
            <div class="file-size">4.7 MB</div>
          </div>
        </div>
        <div class="file-item">
          <div class="file-icon">📁</div>
          <div class="file-info">
            <div class="file-name">模型文件.onnx</div>
            <div class="file-size">15.2 MB</div>
          </div>
        </div>
        <div class="file-item">
          <div class="file-icon">🔧</div>
          <div class="file-info">
            <div class="file-name">配置文件.json</div>
            <div class="file-size">0.8 MB</div>
          </div>
        </div>
        <div class="file-item">
          <div class="file-icon">📈</div>
          <div class="file-info">
            <div class="file-name">训练数据.csv</div>
            <div class="file-size">8.9 MB</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 模型库组件逻辑
</script>

<style scoped>
.model-library-container {
  padding: 2rem;
  height: 100%;
  overflow-y: auto;
}

/* 文件管理器样式 */
.file-manager {
  max-width: 1200px;
}

.file-manager h2 {
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 600;
}

.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.file-item {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-item:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.file-icon {
  font-size: 2.5rem;
  margin-right: 1.5rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  color: white;
}

.file-info {
  flex: 1;
}

.file-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.file-size {
  color: #718096;
  font-size: 0.9rem;
  font-weight: 500;
}

/* 添加文件类型颜色标识 */
.file-item:nth-child(1) .file-icon { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); }
.file-item:nth-child(2) .file-icon { background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); }
.file-item:nth-child(3) .file-icon { background: linear-gradient(135deg, #45b7d1 0%, #2980b9 100%); }
.file-item:nth-child(4) .file-icon { background: linear-gradient(135deg, #96ceb4 0%, #8fbc8f 100%); }
.file-item:nth-child(5) .file-icon { background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); }
.file-item:nth-child(6) .file-icon { background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); }

@media (max-width: 768px) {
  .model-library-container {
    padding: 1rem;
  }
  
  .file-grid {
    grid-template-columns: 1fr;
    padding: 1.5rem;
  }
  
  .file-item {
    padding: 1rem;
  }
  
  .file-icon {
    font-size: 2rem;
    width: 50px;
    height: 50px;
    margin-right: 1rem;
  }
}

@media (max-width: 480px) {
  .file-grid {
    padding: 1rem;
  }
  
  .file-item {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem 1rem;
  }
  
  .file-icon {
    margin-right: 0;
    margin-bottom: 1rem;
  }
}
</style>