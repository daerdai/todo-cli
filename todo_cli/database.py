import sqlite3
import os
from datetime import datetime, date
from typing import List, Optional, Dict, Any


class TodoDatabase:
    """SQLite 数据库操作类"""
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            home = os.path.expanduser("~")
            db_dir = os.path.join(home, ".todo-cli")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "todos.db")
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """初始化数据库表"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    priority TEXT DEFAULT 'medium',
                    due_date TEXT,
                    tag TEXT,
                    completed BOOLEAN DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    completed_at TEXT
                )
            """)
    
    def add(self, content: str, priority: str = "medium", 
            due_date: Optional[str] = None, tag: Optional[str] = None) -> int:
        """添加任务"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO todos (content, priority, due_date, tag)
                   VALUES (?, ?, ?, ?)""",
                (content, priority, due_date, tag)
            )
            return cursor.lastrowid
    
    def list(self, tag: Optional[str] = None, 
             completed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """列出任务"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM todos WHERE 1=1"
            params = []
            
            if tag:
                query += " AND tag = ?"
                params.append(tag)
            if completed is not None:
                query += " AND completed = ?"
                params.append(1 if completed else 0)
            
            query += " ORDER BY completed ASC, 
                    CASE priority 
                        WHEN 'high' THEN 1 
                        WHEN 'medium' THEN 2 
                        WHEN 'low' THEN 3 
                    END, 
                    due_date ASC"
            
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]
    
    def complete(self, todo_id: int) -> bool:
        """标记完成"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """UPDATE todos 
                   SET completed = 1, completed_at = ? 
                   WHERE id = ?""",
                (datetime.now().isoformat(), todo_id)
            )
            return cursor.rowcount > 0
    
    def undo(self, todo_id: int) -> bool:
        """取消完成"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """UPDATE todos 
                   SET completed = 0, completed_at = NULL 
                   WHERE id = ?""",
                (todo_id,)
            )
            return cursor.rowcount > 0
    
    def delete(self, todo_id: int) -> bool:
        """删除任务"""
        with self.get_connection() as conn:
            cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            return cursor.rowcount > 0
    
    def clean_completed(self) -> int:
        """清除已完成的任务"""
        with self.get_connection() as conn:
            cursor = conn.execute("DELETE FROM todos WHERE completed = 1")
            return cursor.rowcount
    
    def get_stats(self) -> Dict[str, int]:
        """获取统计信息"""
        with self.get_connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
            completed = conn.execute(
                "SELECT COUNT(*) FROM todos WHERE completed = 1"
            ).fetchone()[0]
            pending = total - completed
            return {
                "total": total,
                "completed": completed,
                "pending": pending
            }
    
    def get_tags(self) -> List[str]:
        """获取所有标签"""
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT DISTINCT tag FROM todos WHERE tag IS NOT NULL"
            ).fetchall()
            return [row[0] for row in rows]
