import random

# Define card ranks and suits
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Define card values
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Function to deal a card
def deal_card():
    return {'rank': random.choice(ranks), 'suit': random.choice(suits)}

# Function to calculate hand value
def calculate_hand_value(hand):
    value = sum([values[card['rank']] for card in hand])
    # Adjust for Aces
    for card in hand:
        if card['rank'] == 'A' and value > 21:
            value -= 10
    return value

# Function to play Blackjack
def play_blackjack():
    balance = 100
    while True:
        print(f"\nYour current balance is: ${balance}")
        bet = input("Please enter your bet (or 'q' to quit): ")
        if bet.lower() == 'q':
            print(f"\nThanks for playing! Your final balance is: ${balance}")
            break
        try:
            bet = int(bet)
            if bet <= 0 or bet > balance:
                print("Invalid bet. Please try again.")
                continue
        except ValueError:
            print("Invalid bet. Please try again.")
            continue

        # Initialize player and dealer hands
        player_hand = [deal_card(), deal_card()]
        dealer_hand = [deal_card(), deal_card()]

        # Show dealer's up card
        print(f"\nDealer's up card: {dealer_hand[0]['rank']} of {dealer_hand[0]['suit']}")

        # Player's turn
        while True:
            print("\nYour hand:")
            for card in player_hand:
                print(f"{card['rank']} of {card['suit']}")
            print(f"Value: {calculate_hand_value(player_hand)}")
            print("Do you want to 'hit' or 'stand'?")
            action = input().lower()
            if action == 'hit':
                player_hand.append(deal_card())
                if calculate_hand_value(player_hand) > 21:
                    print("\nYou busted! Dealer wins!")
                    balance -= bet
                    break
            elif action == 'stand':
                break
            else:
                print("Invalid input. Please try again.")

        if calculate_hand_value(player_hand) > 21:
            continue

        # Dealer's turn
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card())

        # Show final hands
        print("\nYour hand:")
        for card in player_hand:
            print(f"{card['rank']} of {card['suit']}")
        print(f"Value: {calculate_hand_value(player_hand)}")
        print("Dealer's hand:")
        for card in dealer_hand:
            print(f"{card['rank']} of {card['suit']}")
        print(f"Value: {calculate_hand_value(dealer_hand)}")

        # Determine winner
        if calculate_hand_value(dealer_hand) > 21:
            print("\nDealer busted! You win!")
            balance += bet
        elif calculate_hand_value(dealer_hand) < calculate_hand_value(player_hand):
            print("\nYou win!")
            balance += bet
        elif calculate_hand_value(dealer_hand) > calculate_hand_value(player_hand):
            print("\nDealer wins!")
            balance -= bet
        else:
            print("\nPush!")

# Run the game
play_blackjack()
