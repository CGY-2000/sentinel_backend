# Sentinel 后端服务

这是一个基于FastAPI开发的后端服务，提供用户管理和任务处理功能。

## 功能特点

- 用户认证与授权
- 任务管理
- 数据库集成
- RESTful API接口

## 环境要求

- Python 3.8+
- MySQL数据库

## 安装指南

### 1. 克隆代码仓库

```bash
git clone https://github.com/CGY-2000/sentinel_backend.git
cd sentinel_backend
```

### 2. 创建虚拟环境（推荐）

```bash
conda create -n sentinel_backend python=3.8
conda activate sentinel_backend
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

修改数据库连接配置（具体方法参考项目文档）。

## 使用方法

### 启动服务

```bash
python run.py
```

服务将在 `http://192.168.1.53:8001` 上运行。

### API文档

启动服务后，访问以下URL查看API文档：

- Swagger UI: `http://192.168.1.53:8001/docs`
- ReDoc: `http://192.168.1.53:8001/redoc`

## 项目结构

```
sentinel_backend/
├── app/                # 主应用目录
│   ├── api/            # API路由
│   ├── core/           # 核心功能
│   ├── databse/        # 数据库模型和操作
│   └── schemas/        # 数据模式定义
├── utils/              # 工具函数
├── requirements.txt    # 项目依赖
└── run.py              # 应用入口
```

## 开发指南

### 添加新的API端点

1. 在 `app/api/v1/` 目录下创建新的路由模块
2. 在 `app/schemas/` 创建对应的数据模型
3. 在路由注册文件中添加新路由

### 数据库操作

项目使用SQLAlchemy进行数据库操作，相关模型定义在 `app/databse/` 目录下。

## 部署

### 生产环境部署

对于生产环境，建议使用Gunicorn作为WSGI服务器：

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:create_app
```
