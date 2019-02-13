from . import Card, User, Crupier
from random import randint
def aleatory_card():
    cards = list()
    type = ["Clubs", "Diamonds", "Hearts"]
    for i in range(1, 11):
        cards.append(i)



def main():
    user = User(str(input()))
    crupier = Crupier('Crupier')
    while True:



if __name__ == '__main__':
    main()