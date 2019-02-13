from . import Card


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

