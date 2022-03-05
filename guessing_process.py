from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from random import randint
from typing import Dict, List, Set

words: List[str] = []
with open("wordle-answers-alphabetical.txt") as file:
    words = file.read().split("\n")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BRIGHT_BLACK = '\u001b[30;1m'


class WordPainter:

    def __init__(self, correct_word: List[str], word_input: List[str]) -> None:
        self.correct_word = correct_word
        self.word_input = word_input
        self._yellow_paint_available = self._get_yellow_paint_available()
        self._canvas = [""] * len(word_input)

    def _get_yellow_paint_available(self) -> Dict[str, int]:
        correct_word_letter_count = defaultdict(
            lambda: 0,
            {
                letter: self.correct_word.count(letter)
                for letter in self.correct_word
            }.items()
        )
        word_input_letter_count = {
            letter: self.word_input.count(letter)
            for letter in self.word_input
        }
        return {
            letter: min(correct_word_letter_count[letter],
                        word_input_letter_count[letter])
            for letter in self.word_input
        }

    def _paint_green(self) -> None:
        for index, letter in enumerate(self.word_input):
            if self.word_input[index] == self.correct_word[index]:
                self._canvas[index] = (
                    f"{bcolors.OKGREEN}{letter.upper()}{bcolors.ENDC}"
                    )
                self._yellow_paint_available[letter] -= 1

    def _paint_yellow(self) -> None:
        for index, letter in enumerate(self.word_input):
            if (letter in self.correct_word
                    and self._yellow_paint_available[letter] > 0
                    and self._canvas[index] == ""):
                self._canvas[index] = (
                    f"{bcolors.WARNING}{letter.upper()}{bcolors.ENDC}"
                    )
                self._yellow_paint_available[letter] -= 1

    def _paint_gray(self) -> None:
        for index, letter in enumerate(self.word_input):
            if self._canvas[index] == "":
                self._canvas[index] = (
                    f"{bcolors.BRIGHT_BLACK}{letter.upper()}{bcolors.ENDC}"
                    )

    def get_painted_word(self) -> str:
        self._paint_green()
        self._paint_yellow()
        self._paint_gray()
        return "".join(self._canvas)


class GuessingObserver(ABC):

    @abstractmethod
    def update(self, guessing_process: GuessingProcess) -> None:
        pass


class GuessingProcess:

    def __init__(self) -> None:
        self.correct_word = words[randint(0, len(words))]
        self.number_of_guesses: int = 0
        self.word_was_guessed = False
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

            if word_input in words:
                word_is_valid = True
            else:
                print("Invalid word. Please select another one.\n")

        if self.correct_word == word_input:  # type: ignore
            self.word_was_guessed = True

        word_painter = WordPainter(list(self.correct_word),
                                   list(word_input))  # type: ignore
        print(word_painter.get_painted_word())

        self.number_of_guesses += 1
        self._notify()
