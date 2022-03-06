from __future__ import annotations

from abc import ABC, abstractmethod
from tkinter import END, Entry, Event, Tk
from typing import List

from game_type import GameType, is_input_valid
from word_painter import get_painted_words


class GuessingObserver(ABC):

    @abstractmethod
    def update(self, guessing_process: GuessingProcess) -> None:
        pass


class GuessingProcess(ABC):

    @abstractmethod
    def attach(self, observer: GuessingObserver) -> None:
        pass

    @abstractmethod
    def _notify(self) -> None:
        pass

    @abstractmethod
    def guess_step(self) -> None:
        pass

    @abstractmethod
    def get_max_guesses(self) -> int:
        pass

    @abstractmethod
    def get_were_words_guessed(self) -> List[bool]:
        pass

    @abstractmethod
    def get_number_of_guesses(self) -> int:
        pass

    @abstractmethod
    def get_correct_words(self) -> List[str]:
        pass


class GuessingProcessNoGui(GuessingProcess):

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

    def get_max_guesses(self) -> int:
        return self.max_guesses

    def get_were_words_guessed(self) -> List[bool]:
        return self.were_words_guessed

    def get_number_of_guesses(self) -> int:
        return self.number_of_guesses

    def get_correct_words(self) -> List[str]:
        return self.correct_words


class GuessingProcessGui(GuessingProcess):

    def __init__(self, game_type: GameType, root: Tk) -> None:
        self.game_type = game_type

        self.correct_words = game_type.generate_correct_words()
        self.were_words_guessed: List[bool] = [
            False for word in self.correct_words
            ]
        self.max_guesses = game_type.get_max_guesses()
        self.number_of_guesses: int = 0
        self._observers: List[GuessingObserver] = []

        self.root = root

    def attach(self, observer: GuessingObserver) -> None:
        self._observers.append(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def guess_step(self, event: Event) -> None:
        entry: Entry = event.widget
        word_input = entry.get().lower()

        if is_input_valid(word_input):
            print("Válido!")
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
        else:
            print("Inválido!")

        entry.delete(0, END)

    def get_max_guesses(self) -> int:
        return self.max_guesses

    def get_were_words_guessed(self) -> List[bool]:
        return self.were_words_guessed

    def get_number_of_guesses(self) -> int:
        return self.number_of_guesses

    def get_correct_words(self) -> List[str]:
        return self.correct_words
