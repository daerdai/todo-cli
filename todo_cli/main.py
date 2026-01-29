import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime, date
from typing import Optional

from .database import TodoDatabase
from . import __version__

console = Console()
db = TodoDatabase()


PRIORITY_COLORS = {
    "high": "red",
    "medium": "yellow",
    "low": "green"
}

PRIORITY_EMOJI = {
    "high": "🔴",
    "medium": "🟡",
    "low": "🟢"
}


def print_success(message: str):
    console.print(f"✅ {message}", style="green")


def print_error(message: str):
    console.print(f"❌ {message}", style="red")


def print_info(message: str):
    console.print(f"ℹ️  {message}", style="blue")


@click.group()
@click.version_option(version=__version__, prog_name="todo")
def cli():
    """📝 Todo CLI - 简洁优雅的待办事项管理工具"""
    pass


@cli.command()
@click.argument("content")
@click.option("--priority", "-p", type=click.Choice(["high", "medium", "low"]), 
              default="medium", help="任务优先级")
@click.option("--due", "-d", help="截止日期 (YYYY-MM-DD)")
@click.option("--tag", "-t", help="标签分类")
def add(content: str, priority: str, due: Optional[str], tag: Optional[str]):
    """添加新任务"""
    # 验证日期格式
    if due:
        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            print_error("日期格式错误，请使用 YYYY-MM-DD")
            return
    
    todo_id = db.add(content, priority, due, tag)
    print_success(f"已添加任务 #{todo_id}")
    console.print(f"   内容: {content}")
    console.print(f"   优先级: {PRIORITY_EMOJI[priority]} {priority}")
    if due:
        console.print(f"   截止日期: {due}")
    if tag:
        console.print(f"   标签: 🏷️ {tag}")


@cli.command(name="list")
@click.option("--tag", "-t", help="按标签筛选")
@click.option("--all", "-a", is_flag=True, help="显示所有任务（包括已完成）")
@click.option("--completed", "-c", is_flag=True, help="只显示已完成任务")
def list_todos(tag: Optional[str], all: bool, completed: bool):
    """列出任务"""
    if completed:
        todos = db.list(tag=tag, completed=True)
        title = "已完成任务"
    elif all:
        todos = db.list(tag=tag)
        title = "所有任务"
    else:
        todos = db.list(tag=tag, completed=False)
        title = "待办任务"
    
    if not todos:
        print_info(f"暂无{title}")
        return
    
    table = Table(
        title=f"📋 {title}",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    
    table.add_column("ID", style="dim", width=4)
    table.add_column("状态", width=4, justify="center")
    table.add_column("优先级", width=6)
    table.add_column("内容", min_width=30)
    table.add_column("标签", width=10)
    table.add_column("截止日期", width=12)
    
    for todo in todos:
        status = "✅" if todo["completed"] else "⬜"
        priority = f"{PRIORITY_EMOJI[todo['priority']]} {todo['priority'][:1].upper()}"
        tag_display = f"🏷️ {todo['tag']}" if todo["tag"] else ""
        due = todo["due_date"] or ""
        
        # 检查是否过期
        content = todo["content"]
        if todo["due_date"] and not todo["completed"]:
            try:
                due_date = datetime.strptime(todo["due_date"], "%Y-%m-%d").date()
                if due_date < date.today():
                    content = f"[red]{content} (已过期)[/red]"
            except:
                pass
        
        table.add_row(
            str(todo["id"]),
            status,
            priority,
            content,
            tag_display,
            due
        )
    
    console.print(table)
    
    # 显示统计
    stats = db.get_stats()
    console.print(f"\n总计: {stats['total']} | 待办: {stats['pending']} | 已完成: {stats['completed']}")


@cli.command()
@click.argument("todo_id", type=int)
def done(todo_id: int):
    """标记任务完成"""
    if db.complete(todo_id):
        print_success(f"任务 #{todo_id} 已完成！🎉")
    else:
        print_error(f"任务 #{todo_id} 不存在")


@cli.command()
@click.argument("todo_id", type=int)
def undo(todo_id: int):
    """取消完成状态"""
    if db.undo(todo_id):
        print_success(f"任务 #{todo_id} 已重置为未完成")
    else:
        print_error(f"任务 #{todo_id} 不存在")


@cli.command()
@click.argument("todo_id", type=int)
@click.confirmation_option(prompt="确定要删除这个任务吗？")
def delete(todo_id: int):
    """删除任务"""
    if db.delete(todo_id):
        print_success(f"任务 #{todo_id} 已删除")
    else:
        print_error(f"任务 #{todo_id} 不存在")


@cli.command()
@click.confirmation_option(prompt="确定要清除所有已完成任务吗？")
def clean():
    """清除所有已完成任务"""
    count = db.clean_completed()
    print_success(f"已清除 {count} 个已完成任务")


@cli.command()
def stats():
    """查看统计信息"""
    stats = db.get_stats()
    tags = db.get_tags()
    
    # 创建统计面板
    total_panel = Panel(
        f"[bold cyan]{stats['total']}[/bold cyan]",
        title="总任务",
        border_style="cyan"
    )
    pending_panel = Panel(
        f"[bold yellow]{stats['pending']}[/bold yellow]",
        title="待办",
        border_style="yellow"
    )
    completed_panel = Panel(
        f"[bold green]{stats['completed']}[/bold green]",
        title="已完成",
        border_style="green"
    )
    
    console.print("\n")
    console.print(total_panel, pending_panel, completed_panel)
    
    if tags:
        console.print(f"\n🏷️  标签: {', '.join(tags)}")
    
    # 完成率
    if stats['total'] > 0:
        rate = (stats['completed'] / stats['total']) * 100
        console.print(f"\n📊 完成率: {rate:.1f}%")


if __name__ == "__main__":
    cli()
