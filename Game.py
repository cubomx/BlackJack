from random import randint


class Card:
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    @property
    def name(self):
        return self.__name

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


class User(Player):
    def __init__(self, name):
        super().__init__(name)


class Crupier(Player):
    def __init__(self, name):
        super().__init__(name)

    @staticmethod
    def give_aleatory_card(cards, type):
        rand_card = randint(0, len(cards) - 1)
        rand_type = randint(0, len(type) - 1)
        card = Card(str(cards[rand_card]) + " of " + type[rand_type], rand_card)
        return card

    def give_entry(self, player, cards, type):
        if player.Score.score == 0:
            for i in range(0, 2):
                player.hand = self.give_aleatory_card(cards, type)


def aleatory_card():
    cards = list()
    others = ["Jack", "Queen", "King", "Ace"]
    for i in range(1, 11):
        cards.append(i)
    cards += others
    return cards


def main():
    user = User(str(input()))
    crupier = Crupier('Crupier')
    type = ["Clovers", "Pikes", "Diamonds", "Hearts"]
    cards = aleatory_card()
    crupier.give_entry(user, cards, type)

    for i in user.hand:
        print(i.name)


if __name__ == '__main__':
    main()
