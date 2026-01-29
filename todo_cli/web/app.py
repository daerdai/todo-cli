from flask import Flask, render_template, request, jsonify
from flask import send_from_directory
from ..database import TodoDatabase
from datetime import datetime

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
db = TodoDatabase()


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/todos', methods=['GET'])
def get_todos():
    """获取所有任务"""
    tag = request.args.get('tag')
    completed = request.args.get('completed')
    
    if completed is not None:
        completed = completed.lower() == 'true'
    
    todos = db.list(tag=tag, completed=completed)
    return jsonify(todos)


@app.route('/api/todos', methods=['POST'])
def create_todo():
    """创建任务"""
    data = request.json
    todo_id = db.add(
        content=data['content'],
        priority=data.get('priority', 'medium'),
        due_date=data.get('due_date'),
        tag=data.get('tag')
    )
    return jsonify({'id': todo_id, 'message': '创建成功'}), 201


@app.route('/api/todos/<int:todo_id>/complete', methods=['POST'])
def complete_todo(todo_id):
    """完成任务"""
    if db.complete(todo_id):
        return jsonify({'message': '任务已完成'})
    return jsonify({'error': '任务不存在'}), 404


@app.route('/api/todos/<int:todo_id>/undo', methods=['POST'])
def undo_todo(todo_id):
    """取消完成"""
    if db.undo(todo_id):
        return jsonify({'message': '已重置为未完成'})
    return jsonify({'error': '任务不存在'}), 404


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """删除任务"""
    if db.delete(todo_id):
        return jsonify({'message': '删除成功'})
    return jsonify({'error': '任务不存在'}), 404


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    stats = db.get_stats()
    tags = db.get_tags()
    return jsonify({**stats, 'tags': tags})


@app.route('/api/tags', methods=['GET'])
def get_tags():
    """获取所有标签"""
    tags = db.get_tags()
    return jsonify(tags)


def run_web_server(host='0.0.0.0', port=5000, debug=False):
    """启动 Web 服务器"""
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_web_server(debug=True)
