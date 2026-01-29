from setuptools import setup, find_packages

setup(
    name="todo-cli",
    version="1.0.0",
    description="A beautiful command-line todo list manager",
    author="daerdai",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "todo=todo_cli.main:cli",
        ],
    },
    python_requires=">=3.8",
)
