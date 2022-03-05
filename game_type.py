from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List


class GameType(ABC):

    @abstractmethod
    def get_max_guesses(self) -> int:
        pass

    @abstractmethod
    def generate_correct_words(self) -> List[str]:
        pass
