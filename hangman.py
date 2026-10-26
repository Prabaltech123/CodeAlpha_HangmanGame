
import tkinter as tk
import random

# ------------------ GAME SETTINGS ------------------

WORDS = ["PYTHON", "HANGMAN", "COMPUTER", "PROGRAM", "DEVELOPER"]
MAX_WRONG = 6

root = tk.Tk()
root.title("Hangman Game")
root.geometry("650x650")
root.resizable(False, False)
root.configure(bg="#f4f6f9")

secret_word = ""
guessed_letters = set()
wrong_guesses = 0
game_over = False

# ------------------ TITLE ------------------

title = tk.Label(
    root,
    text="HANGMAN GAME",
    font=("Arial", 24, "bold"),
    bg="#f4f6f9",
    fg="#243b55"
)
title.pack(pady=12)

# ------------------ DRAWING AREA ------------------

canvas = tk.Canvas(
    root,
    width=600,
    height=220,
    bg="white",
    highlightthickness=1,
    highlightbackground="#d9e0e8"
)
canvas.pack(padx=20, pady=5)

def draw_hangman():
    canvas.delete("all")

    # Draw the gallows
    canvas.create_line(60, 195, 180, 195, width=5, fill="#243b55")
    canvas.create_line(90, 195, 90, 25, width=5, fill="#243b55")
    canvas.create_line(90, 25, 240, 25, width=5, fill="#243b55")
    canvas.create_line(240, 25, 240, 50, width=4, fill="#243b55")

    # Each wrong guess draws another body part
    if wrong_guesses >= 1:
        canvas.create_oval(
            220, 50, 260, 90,
            width=4, outline="#e74c3c"
        )

    if wrong_guesses >= 2:
        canvas.create_line(
            240, 90, 240, 140,
            width=4, fill="#e74c3c"
        )

    if wrong_guesses >= 3:
        canvas.create_line(
            240, 105, 210, 130,
            width=4, fill="#e74c3c"
        )

    if wrong_guesses >= 4:
        canvas.create_line(
            240, 105, 270, 130,
            width=4, fill="#e74c3c"
        )

    if wrong_guesses >= 5:
        canvas.create_line(
            240, 140, 215, 175,
            width=4, fill="#e74c3c"
        )

    if wrong_guesses >= 6:
        canvas.create_line(
            240, 140, 265, 175,
            width=4, fill="#e74c3c"
        )

# ------------------ WORD DISPLAY ------------------

word_label = tk.Label(
    root,
    text="",
    font=("Consolas", 25, "bold"),
    bg="#f4f6f9",
    fg="#243b55"
)
word_label.pack(pady=12)

status_label = tk.Label(
    root,
    text="Guess a letter!",
    font=("Arial", 12),
    bg="#f4f6f9",
    fg="#34495e"
)
status_label.pack(pady=3)

attempt_label = tk.Label(
    root,
    text="Incorrect guesses left: 6",
    font=("Arial", 11, "bold"),
    bg="#f4f6f9",
    fg="#e67e22"
)
attempt_label.pack(pady=3)

# ------------------ UPDATE WORD ------------------

def update_word():
    displayed = " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )
    word_label.config(text=displayed)

# ------------------ GUESS LETTER ------------------

def guess_letter(letter):
    global wrong_guesses, game_over

    if game_over or letter in guessed_letters:
        return

    guessed_letters.add(letter)
    letter_buttons[letter].config(
        state="disabled",
        bg="#cbd5e1",
        fg="#64748b"
    )

    if letter in secret_word:
        status_label.config(
            text="Correct guess!",
            fg="#198754"
        )
    else:
        wrong_guesses += 1
        status_label.config(
            text="Wrong guess! Try again.",
            fg="#e74c3c"
        )

    draw_hangman()
    update_word()

    attempt_label.config(
        text=f"Incorrect guesses left: {MAX_WRONG - wrong_guesses}"
    )

    # Check win
    if all(letter in guessed_letters for letter in secret_word):
        game_over = True
        status_label.config(
            text="Congratulations! You won!",
            fg="#198754"
        )
        disable_all_buttons()

    # Check loss
    elif wrong_guesses >= MAX_WRONG:
        game_over = True
        word_label.config(
            text=" ".join(secret_word)
        )
        status_label.config(
            text="Game Over! Better luck next time.",
            fg="#e74c3c"
        )
        disable_all_buttons()

# ------------------ LETTER BUTTONS ------------------

letters_frame = tk.Frame(root, bg="#f4f6f9")
letters_frame.pack(pady=10)

letter_buttons = {}

for index, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    button = tk.Button(
        letters_frame,
        text=letter,
        width=4,
        height=1,
        font=("Arial", 11, "bold"),
        bg="#e3eaf2",
        fg="#243b55",
        activebackground="#b8cbe0",
        relief="raised",
        command=lambda ch=letter: guess_letter(ch)
    )

    button.grid(
        row=index // 9,
        column=index % 9,
        padx=3,
        pady=4
    )

    letter_buttons[letter] = button

# ------------------ DISABLE BUTTONS ------------------

def disable_all_buttons():
    for button in letter_buttons.values():
        button.config(state="disabled")

# ------------------ NEW GAME ------------------

def new_game():
    global secret_word, guessed_letters, wrong_guesses, game_over

    secret_word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0
    game_over = False

    draw_hangman()
    update_word()

    status_label.config(
        text="Guess a letter!",
        fg="#34495e"
    )

    attempt_label.config(
        text="Incorrect guesses left: 6"
    )

    for letter, button in letter_buttons.items():
        button.config(
            state="normal",
            bg="#e3eaf2",
            fg="#243b55"
        )

new_game_button = tk.Button(
    root,
    text="NEW GAME",
    font=("Arial", 12, "bold"),
    bg="#243b55",
    fg="white",
    activebackground="#3d5a80",
    activeforeground="white",
    padx=20,
    pady=7,
    command=new_game
)
new_game_button.pack(pady=10)

# Start the game
new_game()
root.mainloop()
