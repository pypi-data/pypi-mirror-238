"""
Task Manager Module (task_manager.py)

This module provides a simple task management system.
It allows you to create, manage, and track tasks within your application.

Usage:
    
Import this module to use the task manager functionality.
You can create, update, and delete tasks.
Tasks can have a title, description, due date, and status.
Use the functions and classes provided in this module to interact with the task manager.
"""
from importlib import metadata
import toml
from .task_manager import Task, PrioriTeaList

__all__ = ["Task", "PrioriTeaList"]

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
print(__version__)
