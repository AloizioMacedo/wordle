from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint
from typing import Dict, List

WORDS: List[str] = []
with open("wordle-answers-alphabetical.txt") as file:
    WORDS = file.read().split("\n")


class GameType(ABC):

    @abstractmethod
    def get_max_guesses(self) -> int:
        pass

    @abstractmethod
    def generate_correct_words(self) -> List[str]:
        pass


class Wordle(GameType):

    def get_max_guesses(self) -> int:
        return 6

    def generate_correct_words(self) -> List[str]:
        correct_words = [
            WORDS[randint(0, len(WORDS))]
            ]
        return correct_words


class Dordle(GameType):

    def get_max_guesses(self) -> int:
        return 7

    def generate_correct_words(self) -> List[str]:
        correct_words = [
            WORDS[randint(0, len(WORDS))]
            for i in range(0, 2)
            ]
        return correct_words


class Quordle(GameType):

    def get_max_guesses(self) -> int:
        return 9

    def generate_correct_words(self) -> List[str]:
        correct_words = [
            WORDS[randint(0, len(WORDS))]
            for i in range(0, 4)
            ]
        return correct_words
