<template>
  <div class="ai-products-container">
    <div class="chat-interface">
      <h2>AI 聊天助手</h2>
      <div class="chat-container">
        <div class="chat-messages">
          <div class="message bot">
            <strong>AI助手:</strong> 你好！我是你的AI助手，有什么可以帮助你的吗？
          </div>
          <div class="message user">
            <strong>你:</strong> 请介绍一下这个系统
          </div>
          <div class="message bot">
            <strong>AI助手:</strong> 这是一个基于Vue 3构建的AI门户系统，包含多个功能模块...
          </div>
        </div>
        <div class="chat-input">
          <input type="text" placeholder="输入你的消息..." />
          <button>发送</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 智能产品组件逻辑
</script>

<style scoped>
.ai-products-container {
  padding: 2rem;
  height: 100%;
  overflow-y: auto;
}

/* AI聊天助手样式 */
.chat-interface {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.chat-interface h2 {
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 600;
}

.chat-container {
  max-width: 800px;
  margin: 0 auto;
}

.chat-messages {
  height: 400px;
  overflow-y: auto;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  background: rgba(255, 255, 255, 0.6);
}

.message {
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 12px;
  max-width: 80%;
  line-height: 1.5;
}

.message.user {
  background: #667eea;
  color: white;
  margin-left: auto;
}

.message.bot {
  background: rgba(255, 255, 255, 0.9);
  color: #4a5568;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.chat-input {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.chat-input input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-right: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  outline: none;
  transition: all 0.3s ease;
}

.chat-input input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.chat-input button {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.chat-input button:hover {
  background: #5a67d8;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .ai-products-container {
    padding: 1rem;
  }
  
  .chat-messages {
    height: 300px;
  }
  
  .chat-input {
    flex-direction: column;
  }
  
  .chat-input input {
    margin-right: 0;
    margin-bottom: 0.5rem;
  }
}
</style>