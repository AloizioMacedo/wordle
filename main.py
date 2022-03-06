from __future__ import annotations

from game_type import Dordle, Quordle, Wordle
from guessing_process import (GuessingObserver, GuessingProcess,
                              GuessingProcessNoGui)

GAME_TYPE_OPTIONS = {
    "wordle": Wordle,
    "dordle": Dordle,
    "quordle": Quordle
}


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


def main():
    game_type = input("Choose the game type.\n"
                      "Options are: 'wordle', 'dordle', 'quordle'.\n")
    guessing_process = GuessingProcessNoGui(GAME_TYPE_OPTIONS[game_type]())
    game_status = GameStatus(guessing_process)
    print("Welcome to wordle!")
    while game_status.game_is_running:
        guessing_process.guess_step()
    game_status.trigger_end_game()


if __name__ == "__main__":
    main()
