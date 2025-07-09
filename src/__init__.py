"""
海岸线生态对抗建模系统
"""

from .game_controller import ShorlineEcologyGame
from .llm_client import LLMClient
from .random_events import RandomEventSystem
from .game_state import GameState

__version__ = "1.0.0"
__all__ = ["ShorlineEcologyGame", "LLMClient", "RandomEventSystem", "GameState"]
