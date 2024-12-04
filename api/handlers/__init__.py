# api/handlers/__init__.py

from .DocumentHandlers import *
from .TextSplitters import *
from .HandlerFactory import HandlerFactory

__all__ = ["HandlerFactory"]
