"""
--- Part Two ---

To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
    KK677 is now the only two pair, making it the second-weakest hand.
    T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.

With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

"""
import re
import logging
import math
from collections import Counter
import time

start_time = time.time()

logger = logging.Logger("logger", level=logging.DEBUG)
logger.addHandler(logging.StreamHandler())

INPUT_FILE = "2023/inputs/day7.txt"


if __name__ == "__main__":
    total = 0
    hands = []
    row = 0
    with open(INPUT_FILE, "r") as file:
        for line in file:
            hand, bet = line.strip().split(" ")
            hands.append({"hand": hand, "bet": bet})
            row += 1

    # SORT
    # 1. pre-sort lexicographically hands - move J to weakest
    def char_mapper(char: str) -> str:
        mapper = {"A": "E", "K": "D", "Q": "C", "J": "0", "T": "A"}
        if char in mapper:
            return mapper[char]
        else:
            return char

    def string_mapper(hand: str) -> str:
        return "".join([char_mapper(char) for char in hand])

    hands.sort(key=lambda x: string_mapper(x["hand"]))

    # 2. sort by card type - stable sort will keep the lex pre-sort whenever types agree
    def _type_from_counter(counter: dict) -> int:
        """
        Plain type without jokers.
        """
        counts = sorted(list(counter.values()), reverse=True)

        # 5-poker
        if counts == [5]:
            return 6
        # poker
        elif counts == [4, 1]:
            return 5
        # FH
        elif counts == [3, 2]:
            return 4
        # 3-of-a-kind
        elif counts == [3, 1, 1]:
            return 3
        # 2-pairs
        elif counts == [2, 2, 1]:
            return 2
        elif counts == [2, 1, 1, 1]:
            return 1
        else:
            return 0

    char_list = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    def hand_type(hand: str) -> int:
        """
        Assign 0 -> 6  to hands describing the type.
        """
        counter = Counter(hand)
        # if no joker, usual type calc
        if counter["J"] == 0:
            return _type_from_counter(counter)
        # reduce number of jokers and recursive call
        else:
            return max([hand_type(hand.replace("J", char, 1)) for char in char_list])

    for x in hands:
        x["type"] = hand_type(x["hand"])

    hands.sort(key=lambda x: x["type"])

    total = sum([(rank + 1) * int(x["bet"]) for rank, x in enumerate(hands)])

    logger.debug(hands)
    logger.info(f"Total {total}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
