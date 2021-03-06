"""
@Date: 13/02/2021 ~ Version: 1.0
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara
@Author: Ege Şahin

@Description: A version of the missionaries and cannibals problem.
    - 6 missionaires and 6 cannibals with a boat size of 5.
    - with Non-deterministic search routine
    - Run the program via: python3 missionaries_and_cannibals.py
    - you can enable tracing via passing --trace flag (True / False)

"""

# queue for the nondeterministic search
from collections import deque

# random number generator for the nondeterministic search
from random import randint

# run trace mode
import argparse


class State(object):
    def __init__(self, missionaries_left, cannibals_left, action=None):
        """State constructor
        Every object of this class keeps a state information
        which can be achieved by a boat action.
        State represents the number of the cannibals and missionaires
        with their locations as "right" or "left".
        Args:
            missionaries_left: type(int), number of missionaries on the left side of the river
            cannibals_left: type(int), number of cannibals on the left side of the river
            action: type(str), direction of the boat heading to ('left' or 'right').
        Attributes:
            current_action: type(string), Information of the location of the boat; "right" or "left"
            boat_size: type(int), Size of the boat
            nof_missionaries: type(int), Total number of missionaries
            nof_cannibals: type(int), Total number of cannibals
            missionaries_left: type(int), Number of missionaries in the left
            cannibals_left: type(int), Number of cannibals in the left
            missionaries_right: type(int), Number of missionaries in the right
            cannibals_right: type(int), Number of cannibals in the right
        """
        self.current_action = action
        self.boat_size = 5
        self.nof_missionaries = 6
        self.nof_cannibals = 6
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.missionaries_right = self.nof_missionaries - missionaries_left
        self.cannibals_right = self.nof_cannibals - cannibals_left

    def is_goal(self):
        """Check whether state is a goal state
        Returns:
            type(bool), True if the state is the goal False otherwise
        """
        return self.missionaries_left == 0 and self.cannibals_left == 0

    def is_reachable(self):
        """Check whether the state is reachable by checking the conditions
        Returns:
            type(bool), True if the state is reachable False otherwise
        """

        # Constraints on number of missionaries and cannibals
        if (
            self.missionaries_left < 0
            or self.cannibals_left < 0
            or self.missionaries_left > self.nof_missionaries
            or self.cannibals_left > self.nof_cannibals
        ):
            return False
        # Number of cannibals can't exceed number of missionaries in either side
        if (
            self.missionaries_left != 0 and self.cannibals_left > self.missionaries_left
        ) or (
            self.missionaries_right != 0
            and self.cannibals_right > self.missionaries_right
        ):
            return False

        return True

    def get_next(self):
        """Returns the possible next states from the given state
        Returns:
            next states, type([State]), List of next possible reachable states
        """
        possible_states = []
        action = (
            "right" if self.current_action == "left" else "left"
        )  # Next Action is the reverse of current action
        """
            According to the value of action, these if-else and nested for loops try each possible combination of missionaries and
            cannibals and create a new state. If this state is reacbale it is appended to the possible_state.
        """
        if action == "left":
            for nof_passangers in range(1, self.boat_size + 1):
                for nof_cannibal_passengers in range(0, nof_passangers + 1):
                    nof_missionary_passengers = nof_passangers - nof_cannibal_passengers
                    new_state = State(
                        self.missionaries_left - nof_missionary_passengers,
                        self.cannibals_left - nof_cannibal_passengers,
                        action,
                    )
                    if new_state.is_reachable():
                        possible_states.append(new_state)

        else:
            for nof_passangers in range(1, self.boat_size + 1):
                for nof_cannibal_passengers in range(0, nof_passangers + 1):
                    nof_missionary_passengers = nof_passangers - nof_cannibal_passengers
                    new_state = State(
                        self.missionaries_left + nof_missionary_passengers,
                        self.cannibals_left + nof_cannibal_passengers,
                        action,
                    )
                    if new_state.is_reachable():
                        possible_states.append(new_state)
        return possible_states

    def __repr__(self):
        return "State()"

    def __str__(self):
        """String representation of the state
        Returns:
            type(str), formatted string
        """
        state_str = "{0:6s} {1:6s} {2:6s}".format(
            "C" * self.cannibals_left, "  " * 9, "C" * self.cannibals_right
        )
        state_str += "\n"
        state_str += "{0:6s} {1:6s} {2:6s}".format(
            "M" * self.missionaries_left, "  " * 9, "M" * self.missionaries_right
        )
        return state_str

    def __eq__(self, other):
        """Comparison function for states
        Args:
            other: type(State), state to be compared
        Returns:
            type(bool) true if they are equal, false otherwise
        """
        return (
            self.missionaries_left == other.missionaries_left
            and self.cannibals_left == other.cannibals_left
            and self.missionaries_right == other.missionaries_right
            and self.cannibals_right == other.cannibals_right
            and self.current_action == other.current_action
        )

    def __hash__(self):
        """Calculates an hash number from the properties indicated.
        Hash can be used in comparison of two instances.
        Returns:
            type(int) hash number
        """
        return hash(
            (
                self.missionaries_left,
                self.cannibals_left,
                self.missionaries_right,
                self.cannibals_right,
                self.current_action,
            )
        )


def get_state_change_log(current_state, next_state):
    """Returns the string representation of state transition
    Args:
        current_state: type(State) that will be used to decide how many missionaries and cannibals will be send/return
        next_state: type(State) that will be used to decide how many missionaries and cannibals will be send/return
    Returns:
        type(str) The string representation of the state transition
    """
    action = (
        "SEND"
        if (
            current_state.missionaries_left < next_state.missionaries_left
            or current_state.cannibals_left < next_state.cannibals_left
        )
        else "RETURN"
    )
    if action == "SEND":
        change_missionaries = abs(
            current_state.missionaries_left - next_state.missionaries_left
        )
        change_cannibals = abs(current_state.cannibals_left - next_state.cannibals_left)
    else:
        change_missionaries = abs(
            current_state.missionaries_right - next_state.missionaries_right
        )
        change_cannibals = abs(
            current_state.cannibals_right - next_state.cannibals_right
        )
    state_change = "{0:6s} {1:6s} {2:6s}".format(
        action,
        " " + str(change_cannibals) + " CANNIBALS",
        str(change_missionaries) + " MISSIONARIES",
    )

    return state_change


def get_short_log(state):
    """Returns the short representation of a state

    It is denoted by three consecutive integers like: 660
    First integer denotes the number of missionaries on the left side of the river
    Second integer denotes the number of cannibals on the left side of the river
    Third integer denotes the positon of boat (0 if it is on the left side of the river, 1 otherwise)
    """

    return (
        str(state.missionaries_left)
        + str(state.cannibals_left)
        + ("0" if state.current_action == "right" else "1")
    )


def get_path_log(path, seperator):
    """Returns the string representation of a path with a seperator"""
    return seperator.join(map(lambda state: get_short_log(state), path))


def nondeterministic_search(initial_state, traceMode=False):
    """Performs nondeterministic to find possible solutions to the problem.
        In our implementation we continue to search until finding the path or making queue empty.
        At first, we are giving the initial state to add the first path to queue.
        If it is a goal state, nondeterministic search is completed with a success.
        Otherwise the other paths are added to random locations of the queue one by one in each iteration.
        At this point, visited states are marked to prevent loops in the paths.
        Also, in each iteration the first element of the queue is examined.
        If the path does not finish with the goal state, the path is removed from the queue.
        If it terminates with the goal state, the search is completed with success and sthe current path is returned from the function.
    Args:
        intitial_state: type(State), initial state
        traceMode: type(bool), flag to control displaying contents of the queues
    Returns:
        path: type([State]) list of states that visited throughout the search routine
    """
    # return if initial_state is the goal
    if initial_state.is_goal():
        return [initial_state]

    # path to be added in the queue
    current_path = [initial_state]

    # queue for the search
    queue = deque([current_path])

    if traceMode:
        print(
            "You are in tracing mode. At every iteration, current content of the queue, first path in the queue"
        )
        print("and new paths extending the first path will be prompted.\n")
        print("Every state will be represented with three numbers:")
        print(
            "First one denotes the number of missionaries on the left side of the river"
        )
        print(
            "Second one denotes the number of cannibals on the left side of the river"
        )
        print(
            "Third one denotes the positon of boat (0 if it is on the left side of the river, 1 otherwise)\n"
        )
        print(
            "To continue iteration, press Enter and to terminate trace mode, enter q\n"
        )

    # if there are states not yet covered, continue to the loop
    while queue:
        # trace mode
        if traceMode:
            print("Current queue:")
            for path in queue:
                print(get_path_log(path, "-"))

        # visited is the set to keep states that has been visited.
        # it helps the algorithm to not get into the loop.
        visited = set()
        current_path = queue.popleft()
        current_state = current_path[len(current_path) - 1]

        # trace mode
        if traceMode:
            print("\nFirst path of queue: " + get_path_log(current_path, "-"))

        # add each state to visited in the path
        for state in current_path:
            visited.add(state)

        # return if current_state is the goal
        if current_state.is_goal() and len(current_path) <= 8:
            # trace mode
            if traceMode:
                print("Goal path is found: " + get_path_log(path, "-"))
            return current_path

        # calculate next states that can be achived after current state
        next_states = current_state.get_next()

        # trace mode
        if traceMode:
            print("\nNew paths extending the first path:")

        for next_state in next_states:
            # avoids loop by checking visited set
            if next_state in visited:
                continue

            # add state to the current path
            current_path.append(next_state)
            if traceMode:
                print(get_path_log(current_path, "-"))

            # random is found to obtain a nondeterministic approach
            random_idx = randint(0, len(queue))

            # inster path to queue randomly
            if random_idx < len(queue):
                queue.insert(random_idx, current_path.copy())
            else:
                queue.append(current_path.copy())
            current_path.remove(next_state)
        if traceMode:
            quit = input("\nEnter q for quit, press Enter to continue tracing: ")
            if quit == "q":
                traceMode = False
            print("-" * 10)


def print_solution(path):
    """Prints the solution from the given path
    Args:
        path: type([State]) List of states obtained via nondeterministic search
    """
    prev = path[0]
    path_len = len(path)
    for i in range(1, path_len):
        print(prev)
        current = path[i]
        print(get_state_change_log(current, prev))
        prev = current
    print(prev)
    print("Solution consists of " + str(path_len - 1) + " river crossings")


def main(trace):
    """Main body to run the program"""
    CANNIBALS = 6
    MISSIONARIES = 6
    initial_state = State(MISSIONARIES, CANNIBALS, "right")
    traceMode = "0"
    if trace != "1":
        traceMode = input("Enter 1 for trace mode, 0 otherwise: ")
    path = nondeterministic_search(initial_state, (traceMode == "1" or trace == "1"))
    print_solution(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a tracing flag")
    parser.add_argument(
        "--trace",
        metavar="path",
        required=False,
        help="tracing option for the program ('1': True / '0': False)",
    )
    args = parser.parse_args()
    main(trace=args.trace)
