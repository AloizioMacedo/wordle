from __future__ import annotations

from time import sleep
from tkinter import Button, Entry, Frame, Label, Tk
from typing import List

from game_type import Dordle, GameType, Quordle, Wordle
from guessing_process import (GuessingObserver, GuessingProcess,
                              GuessingProcessGui)

GAME_TYPE_OPTIONS = {
    "wordle": Wordle,
    "dordle": Dordle,
    "quordle": Quordle
}

GAME_TYPE: GameType = None  # type: ignore

wanting_to_play = True


class GameStatus(GuessingObserver):

    def __init__(self, guessing_process: GuessingProcess, root: Tk,
                 end_print: Label, entry: Entry) -> None:
        self.game_is_running = True
        self.guessing_process = guessing_process
        guessing_process.attach(self)
        self.root = root
        self.end_print = end_print
        self.entry = entry
        self.retry_frame = Frame(root)
        self.retry_yes = Button(self.retry_frame, text="Retry",
                                command=self.retry)
        self.retry_no = Button(self.retry_frame, text="Close",
                               command=self.destroy)

    def update(self, guessing_process: GuessingProcess) -> None:
        if (guessing_process.get_number_of_guesses()
                >= guessing_process.get_max_guesses()
                and not all(guessing_process.get_were_words_guessed())):
            self.entry.config(state="disabled")
            self.end_print.config(text="I'm sorry! You lost. : (")
            self.retry_yes.grid(row=GAME_TYPE.get_max_guesses()+2, column=0)
            self.retry_no.grid(row=GAME_TYPE.get_max_guesses()+2, column=1)
            self.retry_frame.pack()

        elif all(guessing_process.get_were_words_guessed()):
            self.entry.config(state="disabled")
            self.end_print.config(
                text="Congratulations! You guessed it right!\n"
                )
            self.retry_yes.grid(row=GAME_TYPE.get_max_guesses()+2, column=0)
            self.retry_no.grid(row=GAME_TYPE.get_max_guesses()+2, column=1)
            self.retry_frame.pack()

    def destroy(self) -> None:
        global wanting_to_play
        wanting_to_play = False
        self.root.destroy()

    def retry(self) -> None:
        self.root.destroy()


def selection_window():
    root = Tk()
    root.title("Wordle")

    def select_wordle():
        global GAME_TYPE
        GAME_TYPE = Wordle()
        root.destroy()

    def select_dordle():
        global GAME_TYPE
        GAME_TYPE = Dordle()
        root.destroy()

    def select_quordle():
        global GAME_TYPE
        GAME_TYPE = Quordle()
        root.destroy()

    game_mode_selection = Label(root, text="Select the game mode!")
    wordle = Button(root, text="Wordle", command=select_wordle)
    dordle = Button(root, text="Dordle", command=select_dordle)
    quordle = Button(root, text="Quordle", command=select_quordle)

    game_mode_selection.pack()
    wordle.pack()
    dordle.pack()
    quordle.pack()

    root.mainloop()


def main_game():
    root = Tk()

    def quit_playing():
        global wanting_to_play
        wanting_to_play = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", quit_playing)
    root.title("Wordle")

    words_frame = Frame(root)
    bottom_frame = Frame(root)

    labels = generate_labels(words_frame, GAME_TYPE)

    entry = Entry(bottom_frame)
    end_print = Label(bottom_frame, text="")
    end_print.grid(row=GAME_TYPE.get_max_guesses() + 1, column=0)
    guessing_process = GuessingProcessGui(GAME_TYPE, root, labels, end_print)

    GameStatus(guessing_process, root, end_print, entry)
    set_up_game_gui(words_frame, bottom_frame, labels,
                    entry, GAME_TYPE, guessing_process)
    root.mainloop()


def generate_labels(words_frame: Frame,
                    game_type: GameType) -> List[List[List[Label]]]:
    labels: List[List[List[Label]]] = []
    for i in range(game_type.get_max_guesses()):
        row_of_words: List[List[Label]] = []
        labels.append(row_of_words)
        for j in range(game_type.get_number_of_words()):
            word: List[Label] = []
            row_of_words.append(word)
            for k in range(5):
                label = Label(words_frame, text="⬜")
                word.append(label)
    return labels


def set_up_game_gui(words_frame: Frame,
                    bottom_frame: Frame,
                    labels: List[List[List[Label]]],
                    entry: Entry,
                    game_type: GameType,
                    guessing_process: GuessingProcessGui) -> None:
    for i in range(game_type.get_max_guesses()):
        row_of_words = labels[i]
        for j in range(game_type.get_number_of_words()):
            word = row_of_words[j]
            for k in range(5):
                label = word[k]
                label.grid(row=i, column=6*j+k)
            label = Label(words_frame, text="  ")
            label.grid(row=i, column=6*(j+1)-1)
    entry.grid(row=game_type.get_max_guesses(), column=0)
    entry.bind('<Return>', guessing_process.guess_step)
    words_frame.pack()
    bottom_frame.pack()


def main():
    selection_window()
    while wanting_to_play:
        main_game()


if __name__ == "__main__":
    main()
