from __future__ import annotations

from tkinter import Button, Entry, Label, Tk
from turtle import onclick

from game_type import Dordle, GameType, Quordle, Wordle
from guessing_process import (GuessingObserver, GuessingProcess,
                              GuessingProcessGui)

GAME_TYPE_OPTIONS = {
    "wordle": Wordle,
    "dordle": Dordle,
    "quordle": Quordle
}

GAME_TYPE: GameType = None  # type: ignore


class GameStatus(GuessingObserver):

    def __init__(self, guessing_process: GuessingProcess) -> None:
        self.game_is_running = True
        self.guessing_process = guessing_process
        guessing_process.attach(self)

    def update(self, guessing_process: GuessingProcess) -> None:
        if (guessing_process.get_number_of_guesses()
                >= guessing_process.get_max_guesses()
                and not all(guessing_process.get_were_words_guessed())):
            self.game_is_running = False
            self.game_won = False
        elif all(guessing_process.get_were_words_guessed()):
            self.game_is_running = False
            self.game_won = True

    def trigger_end_game(self) -> None:
        if self.game_won:
            print("Congratulations! You guessed it right!\n")
        else:
            print("I'm sorry! You lost. : (")
            print("The correct answer was"
                  f" {str(self.guessing_process.get_correct_words())}.\n")


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
    root.title("Wordle")
    guessing_process = GuessingProcessGui(GAME_TYPE, root)
    game_status = GameStatus(guessing_process)
    set_up_game_gui(root, GAME_TYPE, guessing_process)
    root.mainloop()
    game_status.trigger_end_game()


def set_up_game_gui(root: Tk, game_type: GameType,
                    guessing_process: GuessingProcessGui) -> None:
    entry = Entry(root)
    for i in range(game_type.get_max_guesses()):
        for j in range(game_type.get_number_of_words()):
            label = Label(root, text="⬜⬜⬜⬜⬜")
            label.grid(row=i, column=j)
    entry.grid(row=game_type.get_max_guesses(), column=0)
    entry.bind('<Return>', guessing_process.guess_step)


def main():
    selection_window()
    main_game()


if __name__ == "__main__":
    main()
