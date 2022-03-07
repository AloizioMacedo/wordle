from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint
from typing import List

WORDS: List[str] = []
with open("wordle-answers-alphabetical.txt") as file:
    WORDS = file.read().split("\n")


def is_input_valid(word_input: str) -> bool:
    return word_input in WORDS


class GameType(ABC):

    @abstractmethod
    def get_max_guesses(self) -> int:
        pass

    @abstractmethod
    def generate_correct_words(self) -> List[str]:
        pass

    @abstractmethod
    def get_number_of_words(self) -> int:
        pass

    @abstractmethod
    def get_geometry(self) -> str:
        pass


class Wordle(GameType):

    def get_max_guesses(self) -> int:
        return 6

    def generate_correct_words(self) -> List[str]:
        correct_words = [
            WORDS[randint(0, len(WORDS))]
            ]
        return correct_words

    def get_number_of_words(self) -> int:
        return 1

    def get_geometry(self) -> str:
        return '250x400'


class Dordle(GameType):

    def get_max_guesses(self) -> int:
        return 7

    def generate_correct_words(self) -> List[str]:
        correct_words = [
            WORDS[randint(0, len(WORDS))]
            for i in range(0, 2)
            ]
        return correct_words

    def get_number_of_words(self) -> int:
        return 2

    def get_geometry(self) -> str:
        return '300x400'


class Quordle(GameType):

    def get_max_guesses(self) -> int:
        return 9

    def generate_correct_words(self) -> List[str]:
        correct_words = [
            WORDS[randint(0, len(WORDS))]
            for i in range(0, 4)
            ]
        return correct_words

    def get_number_of_words(self) -> int:
        return 4

    def get_geometry(self) -> str:
        return '600x400'
