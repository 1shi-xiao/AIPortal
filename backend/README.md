# AI门户系统 - 后端服务

一个基于FastAPI构建的现代化AI门户后端系统，提供用户认证、AI工具管理、文件处理、聊天功能等完整功能。

## 功能特性

- 🔐 **用户认证** - JWT令牌认证，支持注册、登录、密码重置
- 🤖 **AI工具管理** - 集成多种AI工具，如合同审查、数据分析、图像处理等
- 📁 **文件管理** - 支持文件上传、下载、分享和分类管理
- 💬 **AI聊天** - 支持多会话聊天，集成OpenAI GPT模型
- 📊 **数据统计** - 用户行为分析和系统使用情况统计
- ⚙️ **系统设置** - 用户个性化设置和系统全局配置
- 🔍 **智能搜索** - 全局搜索功能，支持工具、文件、聊天记录搜索

## 技术栈

- **Web框架**: FastAPI (高性能异步Web框架)
- **数据库**: SQLAlchemy + SQLite (支持PostgreSQL/MySQL)
- **认证**: JWT + bcrypt (安全的用户认证)
- **文件处理**: aiofiles + Pillow (异步文件操作)
- **AI集成**: OpenAI API (GPT模型集成)
- **数据验证**: Pydantic (数据模型验证)
- **迁移工具**: Alembic (数据库迁移)
- **部署**: Uvicorn (ASGI服务器)

## 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd AIPortal/backend
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，设置必要的配置项
   ```

5. **初始化数据库**
   ```bash
   # 创建数据库表
   python -c "from app.db.database import init_db; init_db()"
   
   # 或使用Alembic进行迁移
   alembic upgrade head
   ```

6. **启动服务**
   ```bash
   # 开发模式
   python main.py
   
   # 或使用uvicorn
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **访问API文档**
   
   启动后访问: http://localhost:8000/docs

## 项目结构

```
backend/
├── app/                    # 应用主目录
│   ├── api/               # API路由
│   │   ├── auth.py       # 用户认证
│   │   ├── files.py      # 文件管理
│   │   ├── ai_tools.py   # AI工具
│   │   ├── chat.py       # AI聊天
│   │   ├── dashboard.py  # 数据统计
│   │   ├── settings.py   # 系统设置
│   │   └── search.py     # 搜索功能
│   ├── core/              # 核心配置
│   │   ├── config.py     # 配置管理
│   │   ├── security.py   # 安全工具
│   │   └── database.py   # 数据库连接
│   ├── models/            # 数据模型
│   │   ├── user.py       # 用户模型
│   │   ├── file.py       # 文件模型
│   │   ├── chat.py       # 聊天模型
│   │   ├── tool.py       # 工具模型
│   │   ├── dashboard.py  # 统计模型
│   │   └── settings.py   # 设置模型
│   ├── schemas/           # 数据模式
│   │   └── __init__.py   # Pydantic模型
│   └── db/                # 数据库相关
│       └── database.py   # 数据库配置
├── alembic/              # 数据库迁移
├── uploads/              # 文件上传目录
├── logs/                 # 日志文件
├── main.py              # 应用入口
├── requirements.txt     # 项目依赖
└── .env.example        # 环境变量示例
```

## API接口文档

### 认证模块

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/refresh` - 刷新令牌
- `GET /api/v1/auth/me` - 获取用户信息
- `PUT /api/v1/auth/profile` - 更新用户信息
- `POST /api/v1/auth/logout` - 用户登出
- `POST /api/v1/auth/change-password` - 修改密码

### 文件管理模块

- `POST /api/v1/files/upload` - 文件上传
- `GET /api/v1/files/` - 获取文件列表
- `GET /api/v1/files/{file_id}` - 获取文件信息
- `DELETE /api/v1/files/{file_id}` - 删除文件
- `GET /api/v1/files/{file_id}/download` - 下载文件
- `POST /api/v1/files/{file_id}/share` - 分享文件
- `GET /api/v1/files/public/{share_token}` - 获取公开文件

### AI工具模块

- `GET /api/v1/ai-tools/` - 获取工具列表
- `GET /api/v1/ai-tools/{tool_id}` - 获取工具详情
- `POST /api/v1/ai-tools/{tool_id}/use` - 使用工具
- `GET /api/v1/ai-tools/{tool_id}/related` - 获取相关工具
- `GET /api/v1/ai-tools/usage` - 用户工具使用记录
- `GET /api/v1/ai-tools/categories` - 工具分类
- `GET /api/v1/ai-tools/popular` - 热门工具

### AI聊天模块

- `POST /api/v1/chat/sessions` - 创建聊天会话
- `GET /api/v1/chat/sessions` - 获取会话列表
- `GET /api/v1/chat/sessions/{session_id}` - 获取会话详情
- `DELETE /api/v1/chat/sessions/{session_id}` - 删除会话
- `GET /api/v1/chat/sessions/{session_id}/messages` - 获取聊天记录
- `POST /api/v1/chat/sessions/{session_id}/messages` - 发送消息
- `DELETE /api/v1/chat/sessions/{session_id}/messages` - 清空聊天记录
- `GET /api/v1/chat/models` - 获取可用AI模型

### 数据统计模块

- `GET /api/v1/dashboard/stats` - 获取仪表板统计数据
- `GET /api/v1/dashboard/user-stats` - 获取用户个人统计
- `POST /api/v1/dashboard/activity` - 记录用户活动
- `GET /api/v1/dashboard/trends` - 获取趋势数据

### 系统设置模块

- `GET /api/v1/settings/user` - 获取用户设置
- `PUT /api/v1/settings/user` - 更新用户设置
- `GET /api/v1/settings/system` - 获取系统设置
- `PUT /api/v1/settings/system` - 更新系统设置
- `DELETE /api/v1/settings/system/{key}` - 删除系统设置
- `GET /api/v1/settings/themes` - 获取可用主题
- `GET /api/v1/settings/languages` - 获取可用语言

### 搜索模块

- `POST /api/v1/search` - 全局搜索
- `GET /api/v1/search/suggestions` - 搜索建议

## 开发指南

### 环境配置

1. **开发环境变量** (`.env`):
   ```env
   DEBUG=true
   LOG_LEVEL=DEBUG
   CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
   ```

2. **生产环境变量**:
   ```env
   DEBUG=false
   LOG_LEVEL=INFO
   SECRET_KEY=your-production-secret-key
   ```

### 数据库操作

1. **创建迁移**:
   ```bash
   alembic revision --autogenerate -m "描述信息"
   ```

2. **应用迁移**:
   ```bash
   alembic upgrade head
   ```

3. **回滚迁移**:
   ```bash
   alembic downgrade -1
   ```

### 测试

1. **运行测试**:
   ```bash
   pytest
   ```

2. **测试覆盖率**:
   ```bash
   pytest --cov=app --cov-report=html
   ```

### 代码规范

- 使用 `black` 进行代码格式化
- 使用 `isort` 进行导入排序
- 使用 `flake8` 进行代码检查

```bash
# 格式化代码
black app/
isort app/

# 检查代码
flake8 app/
```

## 部署说明

### Docker部署

1. **构建镜像**:
   ```bash
   docker build -t aiportal-backend .
   ```

2. **运行容器**:
   ```bash
   docker run -d -p 8000:8000 --env-file .env aiportal-backend
   ```

### 生产环境部署

1. **使用Gunicorn**:
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

2. **使用Nginx反向代理**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

### 环境变量配置

生产环境必须配置的变量：
- `SECRET_KEY`: JWT密钥，必须设置为强随机字符串
- `DATABASE_URL`: 数据库连接字符串
- `OPENAI_API_KEY`: OpenAI API密钥
- `DEBUG`: 设置为 `false`

### 安全建议

1. **HTTPS**: 生产环境必须使用HTTPS
2. **密钥管理**: 使用密钥管理服务存储敏感信息
3. **数据库**: 使用PostgreSQL或MySQL替代SQLite
4. **文件存储**: 使用云存储服务（如AWS S3）
5. **监控**: 集成应用性能监控工具

## 许可证

MIT License

## 支持与联系

如有问题或建议，请通过以下方式联系：
- 邮箱: shixm.114@mail.avic
<!-- - 文档: [https://docs.aiportal.com](https://docs.aiportal.com)
- 问题反馈: [GitHub Issues](https://github.com/your-repo/issues) -->