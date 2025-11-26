<template>
  <div class="hot-tools-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="section-title">{{ currentTool.title }}</h2>
      <p class="section-subtitle">{{ currentTool.subtitle }}</p>
    </div>

    <!-- 工具详情 -->
    <div class="tool-detail-card">
      <!-- 工具描述 -->
      <div class="tool-description">
        <h3>工具介绍</h3>
        <p>{{ currentTool.description }}</p>
      </div>

      <!-- 工具功能 -->
      <div class="tool-features">
        <h3>核心功能</h3>
        <ul>
          <li v-for="(feature, index) in currentTool.features" :key="index">
            <span class="feature-icon">✨</span>
            {{ feature }}
          </li>
        </ul>
      </div>

      <!-- 工具使用示例 -->
      <div class="tool-example">
        <h3>使用示例</h3>
        <div class="example-content">{{ currentTool.example }}</div>
      </div>

      <!-- 工具使用按钮 -->
      <div class="tool-actions">
        <button class="primary-button" @click="useTool">{{ currentTool.actionButton }}</button>
        <button class="secondary-button" @click="goBack">返回上一页</button>
      </div>
    </div>

    <!-- 相关工具推荐 -->
    <div class="related-tools">
      <h3>相关工具推荐</h3>
      <div class="tools-grid">
        <div 
          v-for="(tool, index) in relatedTools" 
          :key="index"
          class="related-tool-card"
          @click="navigateToTool(tool.id)"
        >
          <div class="related-tool-icon">{{ tool.icon }}</div>
          <h4 class="related-tool-name">{{ tool.name }}</h4>
          <p class="related-tool-desc">{{ tool.shortDesc }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';

// 定义工具数据
const toolsData = {
  'contract-review': {
    id: 'contract-review',
    title: '合同审查助手',
    subtitle: '智能合同审查与风险评估',
    icon: '📝',
    description: '合同审查助手是一款基于人工智能技术的合同分析工具，能够快速识别合同中的风险点、不明确条款和潜在法律问题，帮助企业降低合同风险，提高审查效率。',
    features: [
      '自动识别合同中的关键条款和风险点',
      '提供合同合规性评估和建议',
      '支持多种合同类型的智能审查',
      '生成详细的审查报告和风险等级',
      '支持自定义审查规则和模板'
    ],
    example: '上传合同文档 → AI自动分析 → 查看风险报告 → 接收改进建议',
    actionButton: '立即使用合同审查助手'
  },
  'image-style-transfer': {
    id: 'image-style-transfer',
    title: '图片风格转换器',
    subtitle: 'AI驱动的图像风格迁移技术',
    icon: '🖼️',
    description: '图片风格转换器利用深度学习技术，能够将任意图片转换为不同艺术大师的绘画风格，支持多种艺术风格选择，让普通照片瞬间变成艺术作品。',
    features: [
      '支持多种经典艺术风格转换',
      '高分辨率图像处理能力',
      '实时预览转换效果',
      '批量处理多张图片',
      '自定义风格混合比例'
    ],
    example: '上传原始图片 → 选择艺术风格 → 实时预览效果 → 下载转换后图片',
    actionButton: '开始转换图片风格'
  },
  'speech-to-text': {
    id: 'speech-to-text',
    title: '语音转文字助手',
    subtitle: '精准高效的语音识别技术',
    icon: '🎤',
    description: '语音转文字助手采用先进的语音识别算法，能够准确识别多种语言和口音的语音内容，并实时转换为文本，大幅提高会议记录、采访转录和语音笔记的效率。',
    features: [
      '高准确率的语音识别',
      '支持多种语言和口音',
      '实时转换和实时编辑',
      '支持长音频文件处理',
      '自动标点和段落划分'
    ],
    example: '上传音频文件或开始录音 → AI自动识别 → 实时查看文字转换 → 编辑保存文本',
    actionButton: '启动语音识别功能'
  },
  'code-completion': {
    id: 'code-completion',
    title: '代码智能补全器',
    subtitle: '提升编码效率的AI助手',
    icon: '💻',
    description: '代码智能补全器是一款为开发者设计的AI辅助编码工具，能够根据上下文智能预测和补全代码片段，支持多种编程语言，显著提高编码效率和代码质量。',
    features: [
      '智能代码预测和补全',
      '支持多种编程语言',
      '上下文感知的代码建议',
      '代码错误检测和修复',
      '常用代码片段快速插入'
    ],
    example: '开始编写代码 → AI智能补全提示 → 选择合适的补全项 → 继续编码',
    actionButton: '使用代码补全功能'
  },
  'sentiment-analysis': {
    id: 'sentiment-analysis',
    title: '情感分析检测器',
    subtitle: '文本情感智能分析工具',
    icon: '😊',
    description: '情感分析检测器能够自动分析文本内容的情感倾向，包括正面、负面和中性情感，适用于社交媒体分析、客户反馈评估、市场调研等场景。',
    features: [
      '准确识别文本情感倾向',
      '支持批量文本分析',
      '情感强度评分',
      '多语言情感分析支持',
      '可视化情感分析结果'
    ],
    example: '输入或上传文本 → AI情感分析 → 查看情感评分 → 获取分析报告',
    actionButton: '进行情感分析'
  }
};

// 当前工具ID和数据
const currentToolId = ref('contract-review');
const currentTool = computed(() => {
  return toolsData[currentToolId.value] || toolsData['contract-review'];
});

// 相关工具
const relatedTools = computed(() => {
  // 排除当前工具，返回其他所有工具的简要信息
  return Object.values(toolsData)
    .filter(tool => tool.id !== currentToolId.value)
    .map(tool => ({
      id: tool.id,
      name: tool.title,
      icon: tool.icon,
      shortDesc: tool.description.substring(0, 50) + '...'
    }));
});

// 使用工具方法
const useTool = () => {
  // 根据工具ID执行不同的操作
  if (currentTool.value.id === 'contract-review') {
    // 合同审查助手使用指定的百度搜索链接
    window.open('https://cn.bing.com/search?q=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B%E4%BD%A0%E5%B0%B1%E7%9F%A5%E9%81%93&form=ANNTH1&refig=692578ee1a744a348d6c6c506bb877ab&pc=CNNDDB&adppc=EDGEESS&pq=%E7%99%BE%E5%BA%A6&pqlth=2&assgl=8&sgcn=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B%E4%BD%A0%E5%B0%B1%E7%9F%A5%E9%81%93&qs=CT&sgtpv=CT&smvpcn=0&swbcn=10&sctcn=0&sc=10-2&sp=2&ghc=0&cvid=692578ee1a744a348d6c6c506bb877ab&clckatsg=1&hsmssg=0', '_blank');
  } else {
    // 其他工具使用默认提示
    alert(`正在启动${currentTool.value.title}...`);
  }
};

// 返回上一页
const goBack = () => {
  // 触发返回事件
  window.dispatchEvent(new CustomEvent('navigate-to-smart-tools'));
};

// 导航到其他工具
const navigateToTool = (toolId) => {
  currentToolId.value = toolId;
};

// 监听自定义事件，更新当前工具
onMounted(() => {
  const handleNavigateToTool = (event) => {
    if (event.detail && event.detail.toolId && toolsData[event.detail.toolId]) {
      currentToolId.value = event.detail.toolId;
    }
  };

  window.addEventListener('navigate-to-hot-tool', handleNavigateToTool);

  // 清理事件监听器
  return () => {
    window.removeEventListener('navigate-to-hot-tool', handleNavigateToTool);
  };
});
</script>

<style scoped>
.hot-tools-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: 700;
}

.section-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

/* 工具详情卡片 */
.tool-detail-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* 工具描述、功能、示例等通用样式 */
.tool-description, .tool-features, .tool-example {
  margin-bottom: 30px;
}

.tool-description h3, .tool-features h3, .tool-example h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 15px;
  border-bottom: 2px solid #667eea;
  padding-bottom: 8px;
}

.tool-description p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #555;
}

/* 功能列表 */
.tool-features ul {
  list-style: none;
  padding: 0;
}

.tool-features li {
  padding: 10px 0;
  padding-left: 25px;
  position: relative;
  margin-bottom: 8px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.tool-features li:hover {
  transform: translateX(5px);
  background: rgba(102, 126, 234, 0.15);
}

.feature-icon {
  position: absolute;
  left: 10px;
  top: 12px;
}

/* 使用示例 */
.example-content {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  font-style: italic;
  color: #666;
}

/* 工具操作按钮 */
.tool-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
  justify-content: center;
}

.primary-button, .secondary-button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.secondary-button {
  background: #f8f9fa;
  color: #333;
  border: 1px solid #ddd;
}

.secondary-button:hover {
  background: #e9ecef;
  transform: translateY(-1px);
}

/* 相关工具推荐 */
.related-tools {
  margin-top: 40px;
}

.related-tools h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.related-tool-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.related-tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.related-tool-icon {
  font-size: 2rem;
  margin-bottom: 15px;
  text-align: center;
}

.related-tool-name {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 10px;
  text-align: center;
}

.related-tool-desc {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hot-tools-container {
    padding: 10px;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .tool-detail-card {
    padding: 20px;
  }
  
  .tools-grid {
    grid-template-columns: 1fr;
  }
  
  .tool-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .primary-button, .secondary-button {
    width: 100%;
    max-width: 200px;
  }
}
</style>