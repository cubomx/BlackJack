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


class Player:
    def __init__(self, name):
        self.__name = name
        self.__hand = list()
        self.__score = 0

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
        self.__score += card.value

    @property
    def score(self):
        return self.__score


class User(Player):
    def __init__(self, name):
        super().__init__(name)


class Crupier(Player):
    def __init__(self, name):
        super().__init__(name)


def aleatory_card():
    cards = list()
    type = ["Clovers", "Pikes" "Diamonds", "Hearts"]
    others = ["Jack", "Queen", "King", "Ace"]
    for i in range(1, 11):
        cards.append(i)
    cards += others
    print(cards)


def main():
    user = User(str(input()))
    crupier = Crupier('Crupier')
    aleatory_card()
    

if __name__ == '__main__':
    main()
