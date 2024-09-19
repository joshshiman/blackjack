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

        # Check for split
        if player_hand[0]['rank'] == player_hand[1]['rank']:
            print("\nYour hand:")
            for card in player_hand:
                print(f"{card['rank']} of {card['suit']}")
            print(f"Value: {calculate_hand_value(player_hand)}")
            action = input("Do you want to 'split', 'hit', or 'stand'? ")
            if action.lower() == 'split':
                # Split logic
                split_bet = bet
                if balance < split_bet:
                    print("Insufficient balance to split. Please try again.")
                    continue
                balance -= split_bet
                player_hand1 = [player_hand[0], deal_card()]
                player_hand2 = [player_hand[1], deal_card()]
                print("\nHand 1:")
                for card in player_hand1:
                    print(f"{card['rank']} of {card['suit']}")
                print(f"Value: {calculate_hand_value(player_hand1)}")
                print("\nHand 2:")
                for card in player_hand2:
                    print(f"{card['rank']} of {card['suit']}")
                print(f"Value: {calculate_hand_value(player_hand2)}")
                # Play out each hand
                for hand in [player_hand1, player_hand2]:
                    while True:
                        print("\nDo you want to 'hit' or 'stand'?")
                        action = input().lower()
                        if action == 'hit':
                            hand.append(deal_card())
                            print("\nHand:")
                            for card in hand:
                                print(f"{card['rank']} of {card['suit']}")
                            print(f"Value: {calculate_hand_value(hand)}")
                            if calculate_hand_value(hand) > 21:
                                print("\nYou busted! Dealer wins this hand.")
                                break
                        elif action == 'stand':
                            break
                        else:
                            print("Invalid input. Please try again.")
                # Determine winner for each hand
                for hand in [player_hand1, player_hand2]:
                    if calculate_hand_value(hand) > 21:
                        continue
                    # Dealer's turn
                    while calculate_hand_value(dealer_hand) < 17:
                        dealer_hand.append(deal_card())
                    print("\nDealer's hand:")
                    for card in dealer_hand:
                        print(f"{card['rank']} of {card['suit']}")
                    print(f"Value: {calculate_hand_value(dealer_hand)}")
                    if calculate_hand_value(dealer_hand) > 21:
                        print("\nDealer busted! You win this hand!")
                        balance += split_bet
                    elif calculate_hand_value(dealer_hand) < calculate_hand_value(hand):
                        print("\nYou win this hand!")
                        balance += split_bet
                    elif calculate_hand_value(dealer_hand) > calculate_hand_value(hand):
                        print("\nDealer wins this hand.")
                    else:
                        print("\nPush!")
                continue

        # Check for double down
        if calculate_hand_value(player_hand) in [9, 10, 11]:
            print("\nYour hand:")
            for card in player_hand:
                print(f"{card['rank']} of {card['suit']}")
            print(f"Value: {calculate_hand_value(player_hand)}")
            action = input("Do you want to 'double down', 'hit', or 'stand'? ")
            if action.lower() == 'double down':
                # Double down logic
                double_bet = bet
                if balance < double_bet:
                    print("Insufficient balance to double down. Please try again.")
                    continue
                balance -= double_bet
                player_hand.append(deal_card())
                print("\nYour hand:")
                for card in player_hand:
                    print(f"{card['rank']} of {card['suit']}")
                print(f"Value: {calculate_hand_value(player_hand)}")
                if calculate_hand_value(player_hand) > 21:
                    print("\nYou busted! Dealer wins!")
                    continue
                # Dealer's turn
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand.append(deal_card())
                print("\nDealer's hand:")
                for card in dealer_hand:
                    print(f"{card['rank']} of {card['suit']}")
                print(f"Value: {calculate_hand_value(dealer_hand)}")
                # Determine winner
                if calculate_hand_value(dealer_hand) > 21:
                    print("\nDealer busted! You win!")
                    balance += double_bet * 2
                elif calculate_hand_value(dealer_hand) < calculate_hand_value(player_hand):
                    print("\nYou win!")
                    balance += double_bet * 2
                elif calculate_hand_value(dealer_hand) > calculate_hand_value(player_hand):
                    print("\nDealer wins!")
                else:
                    print("\nPush!")
                continue

        # Normal game logic
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
