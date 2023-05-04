import tkinter as tk
from PIL import Image, ImageTk
import os
import random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self):
        self.cards = [Card(suit, rank)
                      for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino War")
        self.root.geometry("1200x800")
        self.root.config(bg="green")

        self.deck = Deck()
        self.player_card = None
        self.dealer_card = None

        self.cards_left = 52

        self.player_wins = 0
        self.dealer_wins = 0

        self.card_images = {}
        self.load_card_images()

        self.create_widgets()

    def load_card_images(self):
        image_dir = "Images"
        for suit in Deck.suits:
            for rank in Deck.ranks:
                filename = f"{rank.lower()}_of_{suit.lower()}.png"
                filepath = os.path.join(image_dir, filename)
                img = Image.open(filepath)
                img = img.resize((200, 250))
                self.card_images[f"{rank} of {suit}"] = ImageTk.PhotoImage(img)

    def create_widgets(self):
        # Title of game
        self.title_label = tk.Label(
            self.root, text="Casino War", font=("Arial", 24))
        self.title_label.pack(pady=10)

        # Frame for the game
        self.game_frame = tk.Frame(self.root, bg="green")
        self.game_frame.pack(pady=20)

        # Cards left frame
        self.cards_left_frame = tk.LabelFrame(
            self.root, font=("Arial", 12), fg="black", bd=0)
        self.cards_left_frame.pack(pady=10)

        # Cards left label
        self.cards_left_label = tk.Label(
            self.cards_left_frame, text="52", font=("Arial", 12), fg="black")
        self.cards_left_label.pack(pady=10)

        # Frames for the dealer and player
        self.dealer_frame = tk.LabelFrame(
            self.game_frame, text="Dealer", font=("Arial", 18), fg="black", bd=0)
        self.dealer_frame.grid(row=0, column=0, padx=20, ipadx=20)

        self.player_frame = tk.LabelFrame(
            self.game_frame, text="Player", font=("Arial", 18), fg="black", bd=0)
        self.player_frame.grid(row=0, column=1, padx=20, ipadx=20)

        # Labels for dealer and player
        self.dealer_label = tk.Label(self.dealer_frame)
        self.dealer_label.pack(pady=20)

        self.player_label = tk.Label(self.player_frame)
        self.player_label.pack(pady=20)

        self.result_label = tk.Label(self.root, font=("Arial", 12))
        self.result_label.pack(pady=10)

        # Win count frames
        self.win_count = tk.Label(
            self.root, text="Win counts", font=("Arial", 16), fg="purple")
        self.win_count.pack(pady=10)

        # Dealer win count label
        self.dealer_wins_label = tk.Label(
            self.win_count, text="Dealer wins: 0", font=("Arial", 14), fg="black")
        self.dealer_wins_label.pack(pady=10)

        # Player win count label
        self.player_wins_label = tk.Label(
            self.win_count, text="Player wins: 0", font=("Arial", 14), fg="black")
        self.player_wins_label.pack(pady=10)

        # Deal button
        self.deal_button = tk.Button(
            self.root, text="Deal", font=("Arial", 14), command=self.deal)
        self.deal_button.pack(pady=10)

        # Reshuffle button
        self.reshuffle_button = tk.Button(
            self.root, text="Reshuffle", font=("Arial", 14), command=self.reshuffle)
        self.reshuffle_button.pack(pady=10)

    def deal(self):
        self.player_card = self.deck.deal_card()
        self.dealer_card = self.deck.deal_card()

        self.player_label.config(
            image=self.card_images[str(self.player_card)])
        self.dealer_label.config(
            image=self.card_images[str(self.dealer_card)])

        if self.get_card_value(self.player_card) > self.get_card_value(self.dealer_card):
            self.result_label.config(text="Player wins!", fg="blue")
            self.player_wins += 1
            self.cards_left -= 2
            self.player_wins_label.config(
                text=f"Player wins: {self.player_wins}")
            self.cards_left_label.config(
                text=f"Cards left: {self.cards_left}")
        elif self.get_card_value(self.player_card) < self.get_card_value(self.dealer_card):
            self.result_label.config(text="Dealer wins!", fg="red")
            self.dealer_wins += 1
            self.cards_left -= 2
            self.dealer_wins_label.config(
                text=f"Dealer wins: {self.dealer_wins}")
            self.cards_left_label.config(
                text=f"Cards left: {self.cards_left}")
        else:
            self.result_label.config(text="Tie!")
            self.cards_left -= 2
            self.cards_left_label.config(
                text=f"Cards left: {self.cards_left}")

    def reshuffle(self):
        self.deck = Deck()
        self.cards_left = 52
        self.player_wins = 0
        self.dealer_wins = 0
        self.player_wins_label.config(text="Player wins: 0")
        self.dealer_wins_label.config(text="Dealer wins: 0")
        self.cards_left_label.config(text="Cards left: 52")
        self.result_label.config(text="")
        self.player_label.config(image="")
        self.dealer_label.config(image="")

    def get_card_value(self, card):
        if card.rank == "Ace":
            return 14
        elif card.rank == "King":
            return 13
        elif card.rank == "Queen":
            return 12
        elif card.rank == "Jack":
            return 11
        else:
            return int(card.rank)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
