// 工具服务：管理工具的最近浏览和收藏功能

// 工具类型定义
class Tool {
  constructor(name, icon, category, url) {
    this.name = name;
    this.icon = icon;
    this.category = category;
    this.url = url;
    this.timestamp = Date.now();
  }
}

// 工具服务对象
const toolService = {
  // 获取最近浏览工具
  getRecentTools() {
    const saved = localStorage.getItem('recentTools');
    return saved ? JSON.parse(saved) : [];
  },

  // 保存最近浏览工具
  saveRecentTools(tools) {
    localStorage.setItem('recentTools', JSON.stringify(tools));
  },

  // 获取收藏工具
  getFavoriteTools() {
    const saved = localStorage.getItem('favoriteTools');
    return saved ? JSON.parse(saved) : [];
  },

  // 保存收藏工具
  saveFavoriteTools(tools) {
    localStorage.setItem('favoriteTools', JSON.stringify(tools));
  },

  // 记录工具访问
  recordToolAccess(toolData) {
    // 确保toolData是Tool对象
    const tool = new Tool(
      toolData.name,
      toolData.icon,
      toolData.category,
      toolData.url
    );

    // 获取现有记录
    const recentTools = this.getRecentTools();

    // 移除已存在的相同工具
    const filteredTools = recentTools.filter(t => t.name !== tool.name);

    // 添加到最前面
    filteredTools.unshift(tool);

    // 只保留最近10个
    const updatedTools = filteredTools.slice(0, 10);

    // 保存更新后的记录
    this.saveRecentTools(updatedTools);

    return updatedTools;
  },

  // 切换收藏状态
  toggleFavorite(toolData) {
    // 获取现有收藏
    const favoriteTools = this.getFavoriteTools();

    // 查找是否已收藏
    const index = favoriteTools.findIndex(t => t.name === toolData.name);

    if (index > -1) {
      // 取消收藏
      favoriteTools.splice(index, 1);
    } else {
      // 添加收藏
      favoriteTools.push(new Tool(
        toolData.name,
        toolData.icon,
        toolData.category,
        toolData.url
      ));
    }

    // 保存更新后的收藏
    this.saveFavoriteTools(favoriteTools);

    return favoriteTools;
  },

  // 检查是否已收藏
  isFavorite(toolData) {
    const favoriteTools = this.getFavoriteTools();
    return favoriteTools.some(t => t.name === toolData.name);
  },

  // 清空最近浏览
  clearRecentTools() {
    localStorage.removeItem('recentTools');
  },

  // 格式化时间
  formatTime(timestamp) {
    const now = Date.now();
    const diff = now - timestamp;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    return `${days}天前`;
  }
};

export default toolService;