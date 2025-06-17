"""Simple terminal-based Snake game demo using curses."""

import random
import curses


def main(stdscr: curses.window) -> None:
    """Run the Snake game inside the provided curses window."""

    curses.curs_set(0)
    win = curses.newwin(20, 60, 0, 0)  # y, x
    win.keypad(True)
    win.timeout(100)

    # Initial snake and food positions
    snk_x = 30
    snk_y = 10
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2],
    ]

    food = [random.randint(1, 18), random.randint(1, 58)]
    win.addch(food[0], food[1], curses.ACS_PI)

    key = curses.KEY_RIGHT
    score = 0

    while True:
        next_key = win.getch()
        key = key if next_key == -1 else next_key

        head = snake[0].copy()
        if key == curses.KEY_DOWN:
            head[0] += 1
        elif key == curses.KEY_UP:
            head[0] -= 1
        elif key == curses.KEY_LEFT:
            head[1] -= 1
        elif key == curses.KEY_RIGHT:
            head[1] += 1

        # Collision detection
        if (
            head[0] in [0, 19]
            or head[1] in [0, 59]
            or head in snake
        ):
            msg = f"Game Over! Final score: {score}"
            stdscr.addstr(10, 30 - len(msg) // 2, msg)
            stdscr.refresh()
            curses.napms(1500)
            break

        snake.insert(0, head)

        if head == food:
            score += 1
            while True:
                nf = [random.randint(1, 18), random.randint(1, 58)]
                if nf not in snake:
                    food = nf
                    break
            win.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], " ")

        win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

    stdscr.addstr(11, 30 - len("Press any key to exit") // 2, "Press any key to exit")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except curses.error:
        print("Error: This environment does not support curses-based windows.")
