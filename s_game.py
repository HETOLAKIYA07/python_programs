import curses
import random
import time

def create_food(snake, window):
    food = None
    while food is None:
        food = [random.randint(1, window[0] - 2), random.randint(1, window[1] - 2)]
        if food in snake:
            food = None
    return food

def snake_game(window):
    curses.curs_set(0)
    window.timeout(100)

    # Get the dimensions of the terminal window
    window_height, window_width = window.getmaxyx()

    # Create the snake and initialize its position
    snake = [
        [window_height // 2, window_width // 2],
        [window_height // 2, window_width // 2 - 1],
        [window_height // 2, window_width // 2 - 2]
    ]

    # Initial direction
    direction = curses.KEY_RIGHT

    # Create the food and display it on the window
    food = create_food(snake, (window_height, window_width))
    window.addch(food[0], food[1], curses.ACS_PI)

    while True:
        # Get the new direction from the user input
        next_direction = window.getch()
        direction = direction if next_direction == -1 else next_direction

        # Calculate the new head position
        head = [snake[0][0], snake[0][1]]
        if direction == curses.KEY_DOWN:
            head[0] += 1
        if direction == curses.KEY_UP:
            head[0] -= 1
        if direction == curses.KEY_LEFT:
            head[1] -= 1
        if direction == curses.KEY_RIGHT:
            head[1] += 1

        # Insert the new head to the snake list
        snake.insert(0, head)

        # Check if the snake collided with the border
        if (
            head[0] in [0, window_height - 1] or
            head[1] in [0, window_width - 1] or
            head in snake[1:]
        ):
            window.addstr(window_height // 2, window_width // 2, "Game Over!")
            window.refresh()
            time.sleep(2)
            break

        # Check if the snake ate the food
        if head == food:
            food = create_food(snake, (window_height, window_width))
            window.addch(food[0], food[1], curses.ACS_PI)
        else:
            # If the snake didn't eat the food, remove the tail
            tail = snake.pop()
            window.addch(tail[0], tail[1], ' ')

        # Display the snake on the window
        window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

if __name__ == "__main__":
    curses.wrapper(snake_game)
