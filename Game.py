from random import randint


class Card:
    def __init__(self, name, value):
        self.__name = name
        self.__value = value
        self.__hidden = False

    @property
    def hidden(self):
        return self.__hidden

    @hidden.setter
    def hidden(self, value):
        self.__hidden = value

    @property
    def name(self):
        if not self.hidden:
            return self.__name
        return '<hidden card>'

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Score:
    def __init__(self):
        self.__hiddenScore = 0
        self.__score = 0

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, points):
        self.__score += points

    @property
    def hidden_score(self):
        return self.__hiddenScore

    @hidden_score.setter
    def hidden_score(self, points):
        self.__hiddenScore += points


class Player:
    def __init__(self, name, mount):
        self.__name = name
        self.__hand = list()
        self.__Score = Score()
        self.__mount = mount
        self.__bet = 0

    @property
    def bet(self):
        return self.__bet

    @bet.setter
    def bet(self, bet):
        self.__bet = bet

    @property
    def mount(self):
        return self.__mount

    @mount.setter
    def mount(self, mount):
        self.__mount = mount

    @property
    def Score(self):
        return self.__Score

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def hand(self):
        return self.__hand

    @hand.setter
    def hand(self, card):
        self.__hand.append(card)
        if isinstance(card, Card):
            self.Score.hidden_score = card.value
            if len(self.hand) > 1:
                self.Score.score = card.value
        else:
            self.__hand = card
            self.Score.hidden_score = -self.Score.hidden_score
            self.Score.score = -self.Score.score
            print("{0}  {1}".format(self.Score.hidden_score, self.Score.score))


class User(Player):
    def __init__(self, name, mount=10000):
        super().__init__(name, mount)
        self.__stand = False

    def push(self):
        print('mount: ' + (str)(self.mount))
        push = self.mount + 1
        while push >= self.mount:
            push = int(input('How much do you want to push: '))
            if push <= self.mount:
                self.bet = push

    @property
    def stand(self):
        return self.__stand

    @stand.setter
    def stand(self, value):
        self.__stand = value


class GameManager:
    def __init__(self):
        self.__name = 'Manager'
        self.winner = None
        self.__hand = list()
        self.__cards = list()

    @property
    def cards(self):
        return self.__cards

    @cards.setter
    def cards(self, card_name):
        if isinstance(card_name, list):
            self.__cards = []
        else:
            self.__cards.append(card_name)

    @property
    def hand(self):
        return self.__hand

    @hand.setter
    def hand(self, card):
        if isinstance(card, list):
            self.cards = list()
            self.__hand = []
        else:
            self.hand.append(card)

    def who_won(self, player, croupier):
        self.winner = True
        if  croupier.Score.hidden_score < player.Score.hidden_score <= 21 or croupier.Score.hidden_score >21:
            player.mount = player.mount + player.bet
            return 'Player won'
        else:
            player.mount = player.mount - player.bet
            return 'Crupier won'

    def busts(self, player):
        if player.Score.hidden_score > 21:
            for card in player.hand:
                if card.value == 11:
                    card.value = 1
                    player.Score.hidden_score = -10
                    if not card.hidden:
                        player.Score.score = -10
                if player.Score.hidden_score <= 21:
                    return False
            print("Perdio {0}: {1}".format(player.name, player.Score.hidden_score))
            return True
        return False

    def cleanHands(self, player, crupier):
        self.hand = list()
        player.hand = list()
        player.stand = False
        self.winner = False
        crupier.hand = list()


class Crupier(Player):
    def __init__(self, name, mount=100000000):
        super().__init__(name, mount)

    @staticmethod
    def give_aleatory_card(cards, type):
        rand_card = randint(0, len(cards) - 1)
        rand_type = randint(0, len(type) - 1)
        if rand_card > 9:
            value = 10
        elif rand_card == 0:
            value = 11
        else:
            value = rand_card+1
        card = Card(str(cards[rand_card]) + " of " + type[rand_type], value)
        return card

    def card_available(self, cards, type, game_manager, player):
        card = self.give_aleatory_card(cards, type)
        while card.name in game_manager.cards:
            card = self.give_aleatory_card(cards, type)
        player.hand = card
        game_manager.hand = card

    def give_entry(self, player, cards, type, game_manager):
        for i in range(0, 2):
            self.card_available(cards, type, game_manager, player)
        if isinstance(player, Crupier):
            player.hand[0].hidden = True

    def play_another(self, player, cards, type, game_manager):
        while player.Score.hidden_score < 17:
            self.card_available(cards, type, game_manager, self)

    def ask_player(self, player, cards, type, game_manager):
        choice = 'c'
        while choice not in "ah":
            choice = str(input('Do you want another(a) or want to stand(h)?')).lower()

        if choice == 'a':
            player.hand = self.give_aleatory_card(cards, type)
        elif choice == 'h':
            print("hola")
            player.stand = True
            game_manager.winner = False


def aleatory_card():
    cards = ['Ace']
    others = ["Jack", "Queen", "King"]
    for i in range(2, 11):
        cards.append(i)
    cards += others
    return cards


def show_cards(player):
    for card in player.hand:
        print(card.name)
    print("\n")


def continuePlaying():
    play = True
    option = input("Do you want to continue playing: (y) (n)" + "\n ")
    if option.lower() == "n":
        play = False
    return play


def main():
    user = User(str(input('Enter your name: \n')))
    crupier = Crupier('Crupier')
    type = ["Clovers", "Pikes", "Diamonds", "Hearts"]
    cards = aleatory_card()
    game_manager = GameManager()
    while True:
        # Crupier gives the user his card/s
        crupier.give_entry(user, cards, type, game_manager)
        # Crupier gives himself cards
        crupier.give_entry(crupier, cards, type, game_manager)
        show_cards(user)
        show_cards(crupier)
        user.push()
        while True:
            crupier.ask_player(user, cards, type, game_manager)
            if game_manager.busts(user):
                print("Busts\n")
                game_manager.winner = True
            elif user.stand and game_manager.winner is not True:
                while crupier.Score.hidden_score < 17:
                    crupier.play_another(crupier, cards, type, game_manager)
                    show_cards(user)
                    show_cards(crupier)
                    if game_manager.busts(crupier):
                        game_manager.winner = True
                        print("Crupier busts\n")
                print(game_manager.who_won(user, crupier))
                print("mount: " + str(user.mount))
            if game_manager.winner:
                break
            show_cards(user)
            show_cards(crupier)
        if not continuePlaying():
            break
        else:
            game_manager.cleanHands(user, crupier)


if __name__ == '__main__':
    main()
