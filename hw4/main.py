"""
@Date: 31/03/2021 ~ Version: 1.0
@Groupno: RIDDLER
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara
@Author: Ege Şahin

@Description: Implementation of the A* algorithm.
            - Solves 15-puzzle optimally with minimum number of moves.

### Running the program
    python3 main.py

"""
import state
from state import State, PuzzleGenerator, a_star


def print_solution(path):
    """Prints the solution path, state by state.
    """
    rowCurrent = 0
    columnCurrent = 0
    rowNext = 0
    columnNext = 0
    for i in range(len(path)):
        currentPuzzle = path[i]
        print(currentPuzzle)
        if i < (len(path) - 1):
            nextPuzzle = path[i + 1]
            for row in range(nextPuzzle.size):
                for column in range(nextPuzzle.size):
                    if currentPuzzle.array[row][column] == 0:
                        rowCurrent = row
                        columnCurrent = column
                    elif nextPuzzle.array[row][column] == 0:
                        rowNext = row
                        columnNext = column

            if rowCurrent > rowNext:
                action = (" "
                          + str(currentPuzzle.array[rowNext][columnNext])
                          + " ---> down \n")
                print(action)
            elif rowCurrent < rowNext:
                action = (" "
                          + str(currentPuzzle.array[rowNext][columnNext])
                          + " ---> up \n")
                print(action)
            elif columnCurrent > columnNext:
                action = (" "
                          + str(currentPuzzle.array[rowNext][columnNext])
                          + " ---> right \n")
                print(action)
            elif columnCurrent < columnNext:
                action = (" "
                          + str(currentPuzzle.array[rowNext][columnNext])
                          + " ---> left \n")
                print(action)
    print("Number of movements made to reach goal state: " + str(len(path)-1) + "\n")
    print("######################################################\n")


def main():
    """Main body to run the program"""

    initial_state = State()
    state = initial_state
    nof_puzzles = 10
    puzzle_generator = PuzzleGenerator(
        nof_distinct_states=nof_puzzles,
        threshold=3)
    print(nof_puzzles, "randomly generated distict puzzles")
    print(puzzle_generator)

    # Solve the generated puzzles
    generated_puzzles = puzzle_generator.get_states()
    puzzle_no = 1
    for puzzle in generated_puzzles:
        print("Solve puzzle S:", str(puzzle_no))
        path = a_star(puzzle)
        print_solution(path)
        puzzle_no += 1

    return 0


if __name__ == "__main__":
    main()
