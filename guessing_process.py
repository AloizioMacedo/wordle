from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint
from typing import List, Set

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


class GuessingProcess:

    def __init__(self) -> None:
        self.correct_word = words[randint(0, len(words))]
        self.number_of_guesses: int = 0
        self.correct_indexes_guessed: Set[int] = set()
        self.correct_letters_guessed: Set[str] = set()
        self.observers: List[GuessingObserver] = []

    def attach(self, observer: GuessingObserver) -> None:
        self.observers.append(observer)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self)

    def guess_step(self) -> None:
        word_is_valid = False
        while not word_is_valid:
            word_input = input("Select the next attempt!\n")
            word_input = word_input.lower()

            if word_input in words:
                word_is_valid = True
            else:
                print("Invalid word. Please select another one.\n")

        for index, letter in enumerate(list(word_input)):  # type: ignore
            self.check_letter(letter, index)

        print(self.get_colored_word(word_input))  # type: ignore
        self.number_of_guesses += 1
        self.notify()

    def check_letter(self, letter: str, index: int) -> None:
        if letter in self.correct_word:
            self.correct_letters_guessed.add(letter)
        if self.correct_word[index] == letter:
            self.correct_indexes_guessed.add(index)

    def get_colored_word(self, word: str) -> str:
        letters = list(word)
        built_up_string = ""
        for index, letter in enumerate(letters):
            upped_letter = letter.upper()
            if self.correct_word[index] == letter:
                built_up_string += (
                    f"{bcolors.OKGREEN}{upped_letter}{bcolors.ENDC}"
                    )
            elif letter in self.correct_letters_guessed:
                built_up_string += (
                    f"{bcolors.WARNING}{upped_letter}{bcolors.ENDC}"
                    )
            else:
                built_up_string += (
                    f"{bcolors.BRIGHT_BLACK}{upped_letter}{bcolors.ENDC}"
                )
        return built_up_string

    def trigger_game_over(self) -> None:
        print("Game Over!")
