"""
M I L E S T O N E  P R O J E C T  2  -  B L A C K J A C K
"""

# We'll use this later
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


# === G A M E  C L A S S E S ==================================================

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):

        # Note this only happens once upon creation of a new Deck
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                # This assumes the Card class has already been defined!
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):

        # Note this doesn't return anything
        random.shuffle(self.all_cards)

    def deal_one(self):

        # Note we remove one card from the list of all_cards
        return self.all_cards.pop()


class Player:

    def __init__(self, name):

        self.name = name

        # New players don't have any cards to start but do get £1000
        self.all_cards = []
        self.wallet = 1000

    def add_cards(self, new_cards):

        if isinstance(new_cards, list):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)

    def __str__(self):
        return f"{self.name} has {len(self.all_cards)} cards."

    def __len__(self):
        """
        :return: The sum of the all the player's card values
        """
        return sum([card.value for card in self.all_cards])


class Dealer(Player):

    def __init__(self):
        super().__init__(Player)


# === G A M E =========================================================================================================

if __name__ == "__main__":

    # === G A M E  S E T U P ==========================================================================================
    name = input("Welcome to Blackjack,\nPlease enter your name\n>>>")
    player_one = Player(name)
    dealer = Dealer()
    cash_out = False

    # === G A M E  S T A R T ==========================================================================================

    print("Let's start!")

    while not cash_out and player_one.wallet > 0:

        # Reset deck
        new_deck = Deck()
        new_deck.shuffle()

        # Reset card hands to empty
        player_one.all_cards = []
        dealer.all_cards = []

        # === B E T T I N G  T I M E ==================================================================================

        bet = 0

        # Validation to insure that the player can only bet what the have and in positive numbers
        while bet <= 0 or bet > player_one.wallet:

            try:  # Won't run if a non-integer is entered
                bet = int(input(f"\nYou have £{player_one.wallet}.\nHow much will you bet?\n>>>"))

            except ValueError:  # Runs if the player doesn't enter an integer
                print("\nYou have not entered a valid amount.\nPlease only enter an integer...\n")

            else:
                if bet < 0:  # Informs the player that they can't enter negative integers
                    print("\nYou cannot enter negative integers.\nTry again...\n")

                elif bet == 0:  # Informs the player that they have not bet anything
                    print("\nYou have to bet something.\nTry again...\n")

                else:
                    if player_one.wallet < bet:  # Informs the player that they have bet above their allowance
                        print("\nYou can't bet more than you have in your wallet.\nPlease try again...\n")
                    else:  # Successful bet
                        print(f"\nYou have bet £{bet}.\n")

        player_one.wallet -= bet

        # === R O U N D  S T A R T ====================================================================================

        for x in range(2):
            # Give both the dealer and the player two cards
            player_one.add_cards(new_deck.deal_one())
            dealer.add_cards(new_deck.deal_one())

        # Check if the player has a winning hand before the round truly begins
        if len(player_one) == 21 and "Ace" in [card.rank for card in player_one.all_cards]:

            print(f"\nYour cards are {[card.__str__() for card in player_one.all_cards]} ({len(player_one)})\nB L A C K  J A C K ! !")

            if len(dealer) == 21 and "Ace" in [card.rank for card in dealer.all_cards]:
                print(f"\nThe Dealer's cards are {[card.__str__() for card in dealer.all_cards]} ({len(dealer)})\n\nP U S H ! !\nNo one wins...\n")
                player_one.wallet += bet
            else:
                player_one.wallet += bet * 2

        else:
            # Reveal one of the dealer's cards to the player
            print(f"The Dealer's up card is the {dealer.all_cards[-1]} ({dealer.all_cards[-1].value}).")

            # === P L A Y E R ' S  T U R N ============================================================================

            choice = " "

            while choice not in ("STAND", "S"):

                # Initial Check at the start of the round to check if the player has gotten 21
                if len(player_one) == 21:

                    print(f"\nYour cards are {[card.__str__() for card in player_one.all_cards]} ({len(player_one)})\n")

                    while len(dealer) < 17:
                        # While the dealer's hand is less than 17, keep drawing cards
                        dealer.add_cards(new_deck.deal_one())
                        print(f"\nThe dealer has drawn a {dealer.all_cards[-1]} ({dealer.all_cards[-1].value})\nDealer's Hand: {[card.__str__() for card in dealer.all_cards]}\nDealer's total: {len(dealer)}\n")

                    else:
                        # Check if the dealer also has a 21 hand
                        if len(dealer) == 21:
                            print(f"Dealer's Hand: {[card.__str__() for card in dealer.all_cards]} ({len(dealer)})\n\nP U S H ! !\nNo one wins...\n")
                            player_one.wallet += bet

                        # Check if the dealer's hand has lost
                        elif len(dealer) > 21:
                            print("\nThe Dealer has BUST!\nYou win.\n")
                            player_one.wallet += bet * 2

                        # Compare the player's hand to the dealer's to see if the player has lost
                        elif len(dealer) > len(player_one):
                            print("The Dealer wins.")

                        # If none of the above is true, it must mean the player has a higher hand and has won.
                        else:
                            print(f"\nDealer's Final Total: {len(dealer)}\nYou win.\n")
                            player_one.wallet += bet * 2
                    break

                # Don't allow the player to choose hit or double if they've already chosen double
                if choice in ("DOUBLE", "D"):
                    choice = "STAND"
                else:
                    # TODO: Still lets the player double even though they don't have the money to
                    if player_one.wallet - bet < 0:

                        # Prompt a choice to hit or stand
                        choice = input(f"\nYour cards are {[card.__str__() for card in player_one.all_cards]} ({len(player_one)}).\nWould you like to: Stand (S) or Hit (H)?\n>>>").upper()

                        while choice not in ("STAND", "S", "HIT", "H"):
                            # Validation to insure the player only uses the correct inputs
                            choice = input("You did not enter a valid choice, please try again...\n>>>").upper()

                    else:
                        # Prompt a choice to hit or stand
                        choice = input(
                            f"\nYour cards are {[card.__str__() for card in player_one.all_cards]} ({len(player_one)}).\nWould you like to: Stand (S), Hit (H) or Double (D)?\n>>>").upper()

                        while choice not in ("STAND", "S", "HIT", "H", "DOUBLE", "D"):
                            # Validation to insure the player only uses the correct inputs
                            choice = input("You did not enter a valid choice, please try again...\n>>>").upper()

                if choice in ("HIT", "H"):
                    # Deal the player another card and tell them what it is
                    player_one.add_cards(new_deck.deal_one())
                    print(f"\nThe card is the {player_one.all_cards[-1]} ({player_one.all_cards[-1].value})")

                elif choice in ("DOUBLE", "D"):
                    # Deal the player a card, tell them what it is, double their wager, and end the player's turn
                    player_one.add_cards(new_deck.deal_one())
                    print(f"\nThe card is the {player_one.all_cards[-1]} ({player_one.all_cards[-1].value})")
                    player_one.wallet -= bet
                    bet *= 2

                # If the player's total is over 21 it's a bust
                if len(player_one) > 21:
                    try:
                        # Try to change an ace in the player's hand to a 1 value
                        player_one.all_cards[[card.value for card in player_one.all_cards].index(11)].value = 1
                    except ValueError:
                        # If there is no ace, an error will occur and the player will bust
                        print(f"\nB U S T\nDealer wins.\n")
                        break

                print(f"Your total is {len(player_one)}.\n")

            # === D E A L E R ' S  T U R N ============================================================================
            if len(player_one) < 21:

                print(f"\nDealer's Hand: {[card.__str__() for card in dealer.all_cards]}\nDealer's total: {len(dealer)}\n")

                # Keep drawing cards until dealer has higher hand than player or is above 17
                while len(dealer) < len(player_one) and len(dealer) < 17:
                    dealer.add_cards(new_deck.deal_one())

                    # Check if the dealer's hand has lost
                    if len(dealer) > 21:
                        # Try to convert the ace value to 1, if there's no ace then an error will occur and the dealer will bust
                        try:
                            dealer.all_cards[[card.value for card in dealer.all_cards].index(11)].value = 1
                        except ValueError:
                            print(f"\nThe dealer has drawn a {dealer.all_cards[-1]} ({dealer.all_cards[-1].value})\nThe Dealer has BUST!\nYou win.\n")
                            player_one.wallet += bet * 2
                            break

                    print(f"\nThe dealer has drawn a {dealer.all_cards[-1]} ({dealer.all_cards[-1].value})\nDealer's Hand: {[card.__str__() for card in dealer.all_cards]}\nDealer's total: {len(dealer)}\n")

                else:
                    # Check if the dealer has a 21 hand, if so, they've won
                    if len(dealer) == 21:
                        print(f"\n\nDealer's Final Total: {len(dealer)}\nDealer has Blackjack\n")

                    # See if the dealer has the same hand value, if so, no one wins and wager is returned
                    elif len(dealer) == len(player_one):
                        # TODO: Check if the dealer is still supposed to draw cards even if their hand matches the player's while under 17 value
                        print(f"\nP U S H ! !\nNo one wins...\n")
                        player_one.wallet += bet

                    # Compare the player's hand to the dealer's to see if the player has lost
                    elif len(dealer) > len(player_one):
                        print("The Dealer wins.")

                    # If none of the above is true, it must mean the player has a higher hand and has won.
                    else:
                        print(f"\nDealer's Final Total: {len(dealer)}\nYou win.\n")
                        player_one.wallet += bet * 2
    else:

        # After the player has either gone bankrupt or cashed out, the code below will determine whether they have lost or won
        if player_one.wallet == 0:
            print("\n\nYou have no money left.\nYou lose.")

        else:
            print(f"\n\nYou cashed out with £{player_one.wallet}.")

            # Simple inequalities check to see if the player made a profit or a loss
            if player_one.wallet - 1000 < 0:
                print(f"\nThat is £{player_one.wallet - 1000} less than what you started with.\nYou lose.")
            elif player_one.wallet - 1000 > 0:
                print(f"\nThat is £{player_one.wallet - 1000} more than what you started with.\nYou win.")


# TODO: Need way to end game other than going broke i.e. cash out option
