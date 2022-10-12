from PIL import ImageTk, Image
import random
import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTTOM, CENTER, COMMAND, LEFT, RIGHT, TOP, END

INPUT_FONT= ("Verdana", 22)

def new_game(root):
    with open('words.txt') as f:
        words = f.readlines()
        newwords = []
        for word in words:
            newword = word[:-1]
            newwords.append(newword)
    chosenNum = random.randrange(1,(len(newwords)-1))
    chosenWord = newwords[chosenNum]
    guessed_chars_list = []
    guess_no = 0
    first_frame = NewFrame(root, chosenWord, guessed_chars_list, guess_no)
    show_frame(first_frame)


def show_frame(frame):
    frame.tkraise()

def next_guess(entry, game, word, guessed, guess_no):
    answer = entry.get().lower()
    if answer.isalpha() and len(answer) == 1:
        if answer in word:
            guessed.append(answer)
            next_frame = NewFrame(game, word, guessed, guess_no)
            show_frame(next_frame)
        else:
            guess_no += 1
            guessed.append(answer)
            next_frame = NewFrame(game, word, guessed, guess_no)
            show_frame(next_frame)
    else:
        next_frame = NewFrame(game, word, guessed, guess_no)
        show_frame(next_frame)

class NewFrame(tk.Frame):
    def __init__(self, main, word, guessed_chars, guess_no):
       super().__init__(main)
       self.word = word
       self.guessed_chars = guessed_chars

       game_frame_list.append(self)
       for frame in game_frame_list:
           frame.grid(row=0, column=0, sticky="nsew")

       new_game_button = tk.Button(self, text="New Game", command= lambda: show_frame(startpage))
       new_game_button.grid()

       entry_box = tk.Entry(self)
       entry_box.grid()

       guess_button = tk.Button(self, text="Guess",
                                command= lambda: next_guess(entry_box, main, word, guessed_chars, guess_no))
       guess_button.grid()

       main.bind('<Return>', lambda event: next_guess(entry_box, main, word, guessed_chars, guess_no))

       blanked_word = []
       winner = 1
       for char in word:
           if char in guessed_chars:
               blanked_word.append(char)
           else:
               blanked_word.append("_")
               winner = 0
       text = blanked_word

       hangman_word = tk.Canvas(self, width=400, height=150)
       hangman_word.create_text(250, 25, text=text, font=INPUT_FONT)
       hangman_word.grid()

       remaining_guesses = tk.Canvas(self, width=1000, height=550)
       number_left = 9 - guess_no
       if winner == 1:
           message = "You won"
       elif number_left > 0:
           message = "You have " + str(number_left) + " guesses left"
       else:
           message = "You have lost"

       remaining_guesses.create_text(350, 55, text=message, font=INPUT_FONT)
       remaining_guesses.grid()


       image_list = ["images/1.jpg", "images/2.jpg", "images/3.jpg", "images/4.jpg", "images/5.jpg", "images/6.jpg", "images/7.jpg", "images/8.jpg", "images/9.jpg", "images/10.jpg", ]

       hangman = ImageTk.PhotoImage(Image.open(image_list[9-number_left]))

       img = tk.Label(self, image=hangman, anchor="center")
       img.image = hangman
       img.place(x=100,y=400)

       if len(guessed_chars) > 0:
           letter_list = "Guessed letters: "
           chars = "".join(guessed_chars)
           letter_list = letter_list + chars + ' '
           remaining_guesses.create_text(350, 125, text=letter_list, font=INPUT_FONT)



if __name__ == "__main__":

    root = tk.Tk()
    startpage = tk.Frame(root)
    game_frame_list = [startpage]
    for frame in game_frame_list:
        frame.grid(row=0, column=0, sticky="nsew")


################## Start Page ##################
    button = tk.Button(startpage, width=25, text="Start Game", command= lambda: new_game(root))
    root.bind('N', lambda event: new_game(root))
    button.grid()
    image1 = Image.open("images/hangman.jpg")
    image2 = image1.resize((1000, 550), Image.Resampling.LANCZOS)
    hangman = ImageTk.PhotoImage(image2)
    introImg = ttk.Label(startpage, image=hangman)
    introImg.grid()
################################################

    show_frame(startpage)


    root.title('Hangman')
    root.geometry('1000x900')
    root.resizable(0, 0)


    root.mainloop()
