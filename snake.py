import random
import curses

# Setup window
curses.initscr()
win = curses.newwin(20, 60, 0, 0)  # y, x
win.keypad(1)
win.timeout(100)

# Initial snake and food
snk_x = 30
snk_y = 10
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

food = [random.randint(1, 18), random.randint(1, 58)]
win.addch(food[0], food[1], curses.ACS_PI)

# Initial direction
key = curses.KEY_RIGHT

score = 0

try:
    while True:
        next_key = win.getch()
        key = key if next_key == -1 else next_key

        # Calculate next head position
        head = snake[0].copy()
        if key == curses.KEY_DOWN:
            head[0] += 1
        if key == curses.KEY_UP:
            head[0] -= 1
        if key == curses.KEY_LEFT:
            head[1] -= 1
        if key == curses.KEY_RIGHT:
            head[1] += 1

        # Check for collision with borders or self
        if (
            head[0] in [0, 19] or
            head[1] in [0, 59] or
            head in snake
        ):
            curses.endwin()
            print(f"Game Over! Final score: {score}")
            break

        # Insert new head
        snake.insert(0, head)

        # Check if food eaten
        if head == food:
            score += 1
            food = None
            while food is None:
                nf = [random.randint(1, 18), random.randint(1, 58)]
                if nf not in snake:
                    food = nf
            win.addch(food[0], food[1], curses.ACS_PI)
        else:
            # Remove tail
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')

        # Draw snake
        win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
except KeyboardInterrupt:
    curses.endwin()
finally:
    curses.endwin()
