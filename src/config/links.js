// 集中管理系统中的所有跳转链接
export const APP_LINKS = {
  // 工具链接
  TOOLS: {
    //管理智能工具
    CONTRACT_REVIEW: 'https://cn.bing.com/search?q=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B%E4%BD%A0%E5%B0%B1%E7%9F%A5%E9%81%93&form=ANNTH1&refig=692578ee1a744a348d6c6c506bb877ab&pc=CNNDDB&adppc=EDGEESS&pq=%E7%99%BE%E5%BA%A6&pqlth=2&assgl=8&sgcn=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B%E4%BD%A0%E5%B0%B1%E7%9F%A5%E9%81%93&qs=CT&sgtpv=CT&smvpcn=0&swbcn=10&sctcn=0&sc=10-2&sp=2&ghc=0&cvid=692578ee1a744a348d6c6c506bb877ab&clckatsg=1&hsmssg=0',
    DATA_ANALYSIS: 'https://cn.bing.com/search?q=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B7%A5%E5%85%B7&form=ANNTH1',
    INTELLIGENT_RECOMMENDATION: 'https://cn.bing.com/search?q=%E6%99%BA%E8%83%BD%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9F&form=ANNTH1',
    DOCUMENT_PROCESSING: 'https://cn.bing.com/search?q=%E6%96%87%E6%A1%A3%E5%A4%84%E7%90%86%E5%B7%A5%E5%85%B7&form=ANNTH1',
    // 工业智能工具
    EQUIPMENT_MONITORING: 'https://blog.csdn.net/dsh789/article/details/110057004',
    PREDICTIVE_MAINTENANCE: '',
    QUALITY_INSPECTION: '',
    ENERGY_OPTIMIZATION: '',
    //大模型工具
    GENERAL_LLM: 'https://cn.bing.com/search?q=通用大模型&form=ANNTH1',
    CODE_LLM: 'https://cn.bing.com/search?q=代码大模型&form=ANNTH1',
    MULTIMODAL_LLM: 'https://cn.bing.com/search?q=多模态大模型&form=ANNTH1'
  },
  // 页面链接
  PAGES: {
    HOME: '/',
    AI_PRODUCTS: '/ai-products',
    AI_ASSISTANT: '/ai-assistant',
    MODEL_LIBRARY: '/model-library',
    WORKFLOW: '/workflow'
  },
  // 外部链接
  EXTERNAL: {
    // 管理智能工具-更多
    MORE_TOOLS: '',
    // 工业智能工具-更多
    MORE_INDUSTRIAL_TOOLS: '',
    // 大模型工具-更多
    MORE_LLM_TOOLS: ''
  },
  // 智能小工具HOT链接
  HOT_TOOLS: {
    // 合同审查助手
    CONTRACT_REVIEW: '/hot-tools/contract-review',
    // 图片风格转换器
    IMAGE_STYLE_TRANSFER: '/hot-tools/image-style-transfer',
    // 语音转文字助手
    SPEECH_TO_TEXT: '/hot-tools/speech-to-text',
    // 代码智能补全器
    CODE_COMPLETION: '/hot-tools/code-completion',
    // 情感分析检测器
    SENTIMENT_ANALYSIS: '/hot-tools/sentiment-analysis'
  },
  // 智能助手指南链接
  AI_GUIDES: {
    // AI数据清洗入门指南 - PDF链接
    DATA_CLEANING: '',
    // 其他指南PDF链接
    VISUALIZATION_TOOLS: '',
    ANOMALY_DETECTION: '',
    EXPORT_BEST_PRACTICES: '',
    MODEL_TRAINING: ''
  },
};

// 打开链接的工具函数
export const openLink = (url, target = '_blank', toolData = null) => {
  // 检查url是否为空
  if (!url || url.trim() === '') {
    // 如果url为空，显示"暂未开发"提示框
    alert('暂未开发');
    return;
  }
  
  // 如果提供了工具数据，记录工具访问
  if (toolData) {
    // 导入工具服务（使用动态导入避免循环依赖）
    import('../services/toolService.js').then(({ default: toolService }) => {
      // 记录工具访问
      toolService.recordToolAccess(toolData);
      
      // 触发全局工具访问事件
      window.dispatchEvent(new CustomEvent('tool-accessed', { 
        detail: toolData 
      }));
    });
  }
  
  // 判断是否为内部页面链接
  if (url.startsWith('/hot-tools/')) {
    // 通过触发自定义事件来切换到对应的热工具详情组件
    const toolId = url.split('/').pop();
    window.dispatchEvent(new CustomEvent('navigate-to-hot-tool', { 
      detail: { toolId } 
    }));
  } else {
    // 外部链接、PDF文件或其他链接在新标签页打开
    try {
      window.open(url, target);
    } catch (error) {
      console.error('打开链接时出错:', error);
      // 如果直接打开失败，尝试使用完整的URL
      const baseUrl = window.location.origin;
      const fullUrl = url.startsWith('/') ? baseUrl + url : url;
      window.open(fullUrl, target);
    }
  }
};