import tkinter as tk
from tkinter import messagebox
from blackjack import Game  # Make sure to import the Game class

class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack Game")
        self.game = Game()

        # Balance Label
        self.balance_label = tk.Label(master, text=f"Balance: ${self.game.player.balance}")
        self.balance_label.pack()

        # Hand Labels
        self.player_hand_label = tk.Label(master, text="Your Hand: ")
        self.player_hand_label.pack()

        self.dealer_hand_label = tk.Label(master, text="Dealer's Hand: ")
        self.dealer_hand_label.pack()

        # Bet Entry
        self.bet_entry = tk.Entry(master)
        self.bet_entry.pack()
        self.bet_entry.insert(0, "Enter your bet")

        # Action Buttons
        self.hit_button = tk.Button(master, text="Hit", command=self.hit)
        self.hit_button.pack()

        self.stand_button = tk.Button(master, text="Stand", command=self.stand)
        self.stand_button.pack()

        self.double_button = tk.Button(master, text="Double Down", command=self.double_down)
        self.double_button.pack()

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

        self.start_game()

    def start_game(self):
        self.game = Game()  # Initialize a new game
        self.game.player.hand = Hand()  # Ensure the player hand is fresh
        self.game.dealer_hand = Hand()   # Ensure the dealer hand is fresh
        self.game.start_round()  # Start the round to deal cards
        self.update_balance()
        self.update_hands()
    
 
    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.game.player.balance}")

    def update_hands(self):
        player_value = self.game.player.hand.calculate_value()
        self.player_hand_label.config(text=f"Your Hand: {self.game.player.hand} (Value: {player_value})")
        
        # Show the dealer's first card and keep the second card hidden
        dealer_visible_card = self.game.dealer_hand.cards[0] if self.game.dealer_hand.cards else "No cards"
        self.dealer_hand_label.config(text=f"Dealer's Hand: {dealer_visible_card} (Hidden)")

    def hit(self):
        self.game.player.hand.add_card(self.game.deck.deal_card())
        if self.game.player.hand.calculate_value() > 21:
            messagebox.showinfo("Busted!", "You busted! Dealer wins.")
            self.start_game()
        else:
            self.update_hands()

    def stand(self):
        self.game.dealer_turn()
        self.end_round()

    def double_down(self):
        try:
            bet_amount = int(self.bet_entry.get())
            self.game.player.bet(bet_amount)
            self.game.player.hand.add_card(self.game.deck.deal_card())
            if self.game.player.hand.calculate_value() > 21:
                messagebox.showinfo("Busted!", "You busted! Dealer wins.")
                self.start_game()
                return
            self.game.dealer_turn()
            self.end_round()
        except ValueError:
            messagebox.showwarning("Invalid Bet", "Please enter a valid bet.")

    def end_round(self):
        player_value = self.game.player.hand.calculate_value()
        dealer_value = self.game.dealer_hand.calculate_value()
        
        if dealer_value > 21:
            messagebox.showinfo("Result", "Dealer busted! You win!")
            self.game.player.win_bet(int(self.bet_entry.get()) * 2)
        elif player_value > dealer_value:
            messagebox.showinfo("Result", "You win!")
            self.game.player.win_bet(int(self.bet_entry.get()) * 2)
        elif player_value < dealer_value:
            messagebox.showinfo("Result", "Dealer wins!")
        else:
            messagebox.showinfo("Result", "Push!")
        
        self.update_balance()
        self.update_hands()

if __name__ == "__main__":
    root = tk.Tk()
    gui = BlackjackGUI(root)
    root.mainloop()
