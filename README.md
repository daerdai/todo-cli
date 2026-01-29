# Todo CLI + Web

一个简洁优雅的待办事项管理工具，支持命令行和 Web 界面。

## 功能特性

- ✅ 添加、完成、删除任务
- 🏷️ 优先级标记（高/中/低）
- 📅 截止日期支持
- 📝 分类标签
- 🎨 漂亮的彩色终端输出
- 🌐 Web UI 界面（响应式设计）
- 💾 SQLite 本地存储
- 🔄 CLI 和 Web 数据同步

## 安装

```bash
pip install -r requirements.txt
```

## CLI 使用方法

```bash
# 添加任务
todo add "完成项目报告" --priority high --due 2026-01-30 --tag 工作

# 查看所有任务
todo list

# 按标签筛选
todo list --tag 工作

# 完成任务
todo done 1

# 删除任务
todo delete 1

# 清除已完成任务
todo clean
```

## Web UI 使用方法

```bash
# 启动 Web 服务器
todo web

# 指定端口
todo web --port 8080

# 调试模式
todo web --debug
```

启动后打开浏览器访问 `http://localhost:5000`

### Web 界面功能

- 🎯 添加任务（支持优先级、截止日期、标签）
- 📊 实时统计面板
- 🔍 按状态/标签筛选
- ✅ 点击完成任务
- 🗑️ 删除任务
- 📱 响应式设计，支持手机访问

## 命令列表

### CLI 命令
- `todo add <内容>` - 添加新任务
- `todo list` - 列出所有任务
- `todo done <ID>` - 标记任务完成
- `todo undo <ID>` - 取消完成状态
- `todo delete <ID>` - 删除任务
- `todo clean` - 清除所有已完成任务
- `todo stats` - 查看统计信息
- `todo web` - 启动 Web 界面

### Web API
- `GET /api/todos` - 获取任务列表
- `POST /api/todos` - 创建任务
- `POST /api/todos/<id>/complete` - 完成任务
- `POST /api/todos/<id>/undo` - 取消完成
- `DELETE /api/todos/<id>` - 删除任务
- `GET /api/stats` - 获取统计信息

## 项目结构

```
todo-cli/
├── todo_cli/
│   ├── __init__.py
│   ├── database.py      # 数据库操作
│   ├── main.py          # CLI 入口
│   └── web/
│       ├── __init__.py
│       ├── app.py       # Flask 应用
│       ├── templates/
│       │   └── index.html
│       └── static/      # 静态资源
├── README.md
├── requirements.txt
├── setup.py
└── LICENSE
```

## License

MIT
