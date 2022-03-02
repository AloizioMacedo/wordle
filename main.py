from __future__ import annotations

from guessing_process import GuessingObserver, GuessingProcess


class GameStatus(GuessingObserver):

    def __init__(self, guessing_process: GuessingProcess) -> None:
        self.game_is_running = True
        guessing_process.attach(self)

    def update(self, guessing_process: GuessingProcess) -> None:
        if guessing_process.number_of_guesses >= 5:
            self.game_is_running = False
            self.game_won = False
        elif len(guessing_process.correct_indexes_guessed) == 5:
            self.game_is_running = False
            self.game_won = True

    def trigger_end_game(self) -> None:
        if self.game_won:
            print("Congratulations! You guessed the word!\n")
        else:
            print("I'm sorry! You lost. : (\n")


def main():
    guessing_process = GuessingProcess()
    game_status = GameStatus(guessing_process)
    while game_status.game_is_running:
        guessing_process.guess_step()
    game_status.trigger_end_game()


if __name__ == "__main__":
    main()
