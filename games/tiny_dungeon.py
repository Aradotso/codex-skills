#!/usr/bin/env python3
"""A tiny terminal dungeon game with no external dependencies."""

from __future__ import annotations

import random


BOARD_SIZE = 5
MOVES = {
    "w": (-1, 0),
    "a": (0, -1),
    "s": (1, 0),
    "d": (0, 1),
}


def place_items() -> dict[str, tuple[int, int]]:
    cells = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)]
    cells.remove((0, 0))
    cells.remove((BOARD_SIZE - 1, BOARD_SIZE - 1))
    key, trap = random.sample(cells, 2)
    return {
        "player": (0, 0),
        "exit": (BOARD_SIZE - 1, BOARD_SIZE - 1),
        "key": key,
        "trap": trap,
    }


def draw(positions: dict[str, tuple[int, int]], has_key: bool) -> None:
    print()
    for row in range(BOARD_SIZE):
        tiles = []
        for col in range(BOARD_SIZE):
            spot = (row, col)
            if spot == positions["player"]:
                tiles.append("@")
            elif spot == positions["exit"]:
                tiles.append("E")
            elif spot == positions["key"] and not has_key:
                tiles.append("K")
            elif spot == positions["trap"]:
                tiles.append("^")
            else:
                tiles.append(".")
        print(" ".join(tiles))
    print()


def step(position: tuple[int, int], move: str) -> tuple[int, int]:
    row_delta, col_delta = MOVES[move]
    row = min(max(position[0] + row_delta, 0), BOARD_SIZE - 1)
    col = min(max(position[1] + col_delta, 0), BOARD_SIZE - 1)
    return row, col


def main() -> None:
    positions = place_items()
    has_key = False

    print("Tiny Dungeon")
    print("Move with WASD. Pick up K, avoid ^, then reach E.")

    while True:
        draw(positions, has_key)
        move = input("move> ").strip().lower()

        if move in {"q", "quit"}:
            print("You leave the dungeon.")
            return
        if move not in MOVES:
            print("Use W, A, S, D, or Q.")
            continue

        positions["player"] = step(positions["player"], move)

        if positions["player"] == positions["trap"]:
            draw(positions, has_key)
            print("You stepped on the trap. Game over.")
            return
        if positions["player"] == positions["key"]:
            has_key = True
            print("You picked up the key.")
        if positions["player"] == positions["exit"]:
            if has_key:
                draw(positions, has_key)
                print("You unlocked the exit and won.")
                return
            print("The exit is locked. Find the key first.")


if __name__ == "__main__":
    main()
