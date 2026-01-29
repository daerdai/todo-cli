# Todo CLI

一个简洁优雅的命令行待办事项管理工具。

## 功能特性

- ✅ 添加、完成、删除任务
- 🏷️ 优先级标记（高/中/低）
- 📅 截止日期支持
- 📝 分类标签
- 🎨 漂亮的彩色终端输出
- 💾 SQLite 本地存储

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

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

## 命令列表

- `todo add <内容>` - 添加新任务
- `todo list` - 列出所有任务
- `todo done <ID>` - 标记任务完成
- `todo undo <ID>` - 取消完成状态
- `todo delete <ID>` - 删除任务
- `todo clean` - 清除所有已完成任务
- `todo stats` - 查看统计信息

## License

MIT
