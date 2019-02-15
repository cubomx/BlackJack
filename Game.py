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
    def __init__(self, name):
        self.__name = name
        self.__hand = list()
        self.__Score = Score()

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
        self.Score.hidden_score = card.value
        if len(self.hand) > 1:
            self.Score.score = card.value


class User(Player):
    def __init__(self, name):
        super().__init__(name)
        self.__stand = False


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



    @property
    def hand(self):
        return self.__hand

    @hand.setter
    def hand(self, card):
        self.hand.append(card)

    def who_won(self, player, croupier):
        self.winner = True
        if player.Score.hidden_score > croupier.Score.hidden_score:
            return 'Player won'
        else:
            return 'Crupier won'

    def busts(self, player):
        if player.Score.hidden_score > 21:
            for card in player.hand:
                if card.value == 11:
                    card.value = 1
                    player.Score.hidden_score -= 10
                    if not card.hidden:
                        player.Score.score -= 10
                if player.Score.hidden_score <= 21:
                    return False
            print("Perdiste: {0}".format(player.Score.hidden_score))
            return True
        return False


class Crupier(Player):
    def __init__(self, name):
        super().__init__(name)

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
        while card in game_manager.hand:
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

    def ask_player(self, player, cards, type):
        choice = 'c'
        while choice != 'a' and choice != 'h':
            choice = str(input('Do you want another(a) or want to stand(h)?'))

        if choice == 'a':
            player.hand = self.give_aleatory_card(cards, type)
        elif choice == 'h':
            player.stand = True


def aleatory_card():
    cards = ['Ace']
    others = ["Jack", "Queen", "King"]
    for i in range(2, 11):
        cards.append(i)
    cards += others
    return cards


def show_cards(player):
    for card in player.hand:
        print(card.name + " {0}".format(card.value))
    print("\n")


def main():
    user = User(str(input()))
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
        while True:
            crupier.ask_player(user, cards, type)
            show_cards(user)
            show_cards(crupier)
            if game_manager.busts(user):
                print("Busts\nCrupier won")
                game_manager.winner = True
            if user.stand and game_manager.winner is not True:
                crupier.play_another(crupier, cards, type, game_manager)
                show_cards(user)
                show_cards(crupier)
                if game_manager.busts(crupier):
                    print("Crupier busts\nPlayer won")
                    game_manager.winner = True
                else:
                    print(game_manager.who_won(user, crupier))

            if game_manager.winner:
                break
        break


if __name__ == '__main__':
    main()
