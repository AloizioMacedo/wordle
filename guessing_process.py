from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from game_type import GameType, is_input_valid
from word_painter import get_painted_words


class GuessingObserver(ABC):

    @abstractmethod
    def update(self, guessing_process: GuessingProcess) -> None:
        pass


class GuessingProcess:

    def __init__(self, game_type: GameType) -> None:
        self.game_type = game_type

        self.correct_words = game_type.generate_correct_words()
        self.were_words_guessed: List[bool] = [
            False for word in self.correct_words
            ]
        self.max_guesses = game_type.get_max_guesses()
        self.number_of_guesses: int = 0
        self._observers: List[GuessingObserver] = []

    def attach(self, observer: GuessingObserver) -> None:
        self._observers.append(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def guess_step(self) -> None:
        word_is_valid = False
        while not word_is_valid:
            word_input = input("Write your next attempt!\n")
            word_input = word_input.lower()

            if is_input_valid(word_input):
                word_is_valid = True
            else:
                print("Invalid word. Please select another one.\n")

        painted_words = get_painted_words(
            word_input,  # type: ignore
            self.correct_words,
            self.were_words_guessed
            )
        print(painted_words)

        for index, word in enumerate(self.correct_words):
            if word_input == word:  # type: ignore
                self.were_words_guessed[index] = True

        self.number_of_guesses += 1
        self._notify()
