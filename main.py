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

        self.card_images = {}
        self.load_card_images()

        self.create_widgets()

    def load_card_images(self):
        image_dir = "Images"
        for suit in Deck.suits:
            for rank in Deck.ranks:
                filename = f"{rank.lower()}_of_{suit.lower()}.png"
                filepath = os.path.join(image_dir, filename)
                self.card_images[f"{rank} of {suit}"] = ImageTk.PhotoImage(
                    Image.open(filepath))

    def create_widgets(self):
        self.title_label = tk.Label(
            self.root, text="Casino War", font=("Arial", 16))
        self.title_label.pack(pady=10)

        self.deal_button = tk.Button(
            self.root, text="Deal", font=("Arial", 12), command=self.deal)
        self.deal_button.pack(pady=10)

        self.player_label = tk.Label(
            self.root, text="Player", font=("Arial", 12))
        self.player_label.pack()

        self.player_card_label = tk.Label(self.root)
        self.player_card_label.pack()

        self.dealer_label = tk.Label(
            self.root, text="Dealer", font=("Arial", 12))
        self.dealer_label.pack()

        self.dealer_card_label = tk.Label(self.root)
        self.dealer_card_label.pack()

        self.result_label = tk.Label(self.root, font=("Arial", 12))
        self.result_label.pack(pady=10)

    def deal(self):
        self.player_card = self.deck.deal_card()
        self.dealer_card = self.deck.deal_card()

        self.player_card_label.config(
            image=self.card_images[str(self.player_card)])
        self.dealer_card_label.config(
            image=self.card_images[str(self.dealer_card)])

        if self.get_card_value(self.player_card) > self.get_card_value(self.dealer_card):
            self.result_label.config(text="Player wins!")
        elif self.get_card_value(self.player_card) < self.get_card_value(self.dealer_card):
            self.result_label.config(text="Dealer wins!")
        else:
            self.result_label.config(text="Tie!")

    def get_card_value(self, card):
        if card.rank == "Ace":
            return 14
        elif card.rank == "King":
            return 13
        elif card.rank == "Queen":
            return 12


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
