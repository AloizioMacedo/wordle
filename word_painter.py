from abc import ABC, abstractmethod
from collections import defaultdict
from tkinter import Label
from typing import Dict, List


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


def get_painted_words(word_input: str,
                      correct_words: List[str],
                      were_words_guessed: List[bool]) -> str:
    painted_words: List[str] = []
    for index, correct_word in enumerate(correct_words):
        word_painter = _WordPainterNoGui(list(correct_word),
                                         list(word_input))
        if were_words_guessed[index]:
            painted_word = word_painter.get_solved()
            painted_words.append(painted_word)
            continue
        painted_word = word_painter.get_painted_word()
        painted_words.append(painted_word)
    return " ".join(painted_words)


def put_painted_words_in_gui(word_input: str,
                             correct_words: List[str],
                             were_words_guessed: List[bool],
                             guess_number: int,
                             labels: List[List[Label]]) -> None:
    painted_words: List[str] = []
    for index, correct_word in enumerate(correct_words):
        word_painter = _WordPainterGui(list(correct_word),
                                       list(word_input),
                                       labels[index])
        if were_words_guessed[index]:
            word_painter.paint_solved()
            continue
        word_painter.paint_word()


class WordPainter(ABC):

    @abstractmethod
    def get_solved():
        pass

    @abstractmethod
    def _get_yellow_paint_available():
        pass

    @abstractmethod
    def _paint_green():
        pass

    @abstractmethod
    def _paint_yellow():
        pass

    @abstractmethod
    def _paint_gray():
        pass

    @abstractmethod
    def get_painted_word():
        pass


class _WordPainterNoGui(WordPainter):

    def __init__(self, correct_word: List[str], word_input: List[str]) -> None:
        self.correct_word = correct_word
        self.word_input = word_input
        self._yellow_paint_available = self._get_yellow_paint_available()
        self._canvas = [""] * len(word_input)

    def get_solved(self) -> str:
        return f"{bcolors.OKGREEN}*****{bcolors.ENDC}"

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


class _WordPainterGui(WordPainter):

    def __init__(self, correct_word: List[str], word_input: List[str],
                 labels: List[Label]) -> None:
        self.correct_word = correct_word
        self.word_input = word_input
        self._yellow_paint_available = self._get_yellow_paint_available()
        self._canvas = labels

    def get_solved(self) -> str:
        return f"{bcolors.OKGREEN}*****{bcolors.ENDC}"

    def paint_solved(self):
        for index in range(len(self.word_input)):
            self._canvas[index].config(text="*", fg="green",
                                       font='Helvetica 18 bold')

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
                self._canvas[index].config(text=letter.upper(), fg="green",
                                           font='Helvetica 18 bold')
                self._yellow_paint_available[letter] -= 1

    def _paint_yellow(self) -> None:
        for index, letter in enumerate(self.word_input):
            if (letter in self.correct_word
                    and self._yellow_paint_available[letter] > 0
                    and self._canvas[index].cget("text") == "⬜"):
                self._canvas[index].config(text=letter.upper(), fg="orange",
                                           font='Helvetica 18 bold')
                self._yellow_paint_available[letter] -= 1

    def _paint_gray(self) -> None:
        for index, letter in enumerate(self.word_input):
            if self._canvas[index].cget("text") == "⬜":
                self._canvas[index].config(text=letter.upper(), fg="gray",
                                           font='Helvetica 18 bold')

    def get_painted_word(self) -> str:
        self._paint_green()
        self._paint_yellow()
        self._paint_gray()
        return "".join(self._canvas)  # type: ignore

    def paint_word(self) -> None:
        self._paint_green()
        self._paint_yellow()
        self._paint_gray()
