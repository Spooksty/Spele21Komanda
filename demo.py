#Ātri uzmesta spēles demo versija
#Pašlaik tikai komandrindā un cilvēks pret cilvēku

import random

#Klase kurā tiek glabāti spēlētāju punkti, bankas punkti un pašreizējais skaitlis
class score:
    def __init__(self, num1, num2, num3, num4):
        self.p1 = num1
        self.p2 = num2
        self.banka = num3
        self.number = num4
    
    def __str__(self):
        return f"NumberSet({self.p1}, {self.p2}, {self.banka}, {self.number})"
    
    def get_all(self):
        return [self.p1, self.p2, self.banka, self.number]


#Funkcija, kas ģenerē 5 nejaušus skaitļus, kas ir dalāmi ar 6 un ļauj spēlētājam izvēlēties vienu no tiem kā sākuma skaitli
def startgame():
    
    numbers = [random.randint(10000 // 6, 20000 // 6) * 6 for _ in range(5)]

    print("Pick the starting number:")
    for i, num in enumerate(numbers, 1):
        print(f"{i}. {num}")

    while True:
        try:
            choice = int(input("\nChoose a number (1-5): "))
            if 1 <= choice <= 5:
                selected = numbers[choice - 1]
                print(f"\nYou selected: {selected}")
                return selected
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

#Funkcija, kas izvada spēlētāju punktus un bankas punktus
def printscore(tablo):
    print(f"Player 1 Score: {tablo.p1}")
    print(f"Player 2 Score: {tablo.p2}")
    print(f"Points in bank: {tablo.banka}")
    print("")

#Funkcija, kas izvada tikai spēlētāju punktus, bez bankas punktiem
def printscorenobank(tablo):
    print("")
    print(f"Player 1 Score: {tablo.p1}")
    print(f"Player 2 Score: {tablo.p2}")
    print("")

#Funkcija, kas kontrolē spēles gaitu
def game(tablo):
    print("Game start")
    while tablo.number > 10:
        print("Current number: ",  tablo.number)
        print("")
        while True:
            p1move = input("Player 1  move: ").strip().lower()
            if p1move not in ['2', '3']:
                print("Invalid move. Please enter 2 or 3.")
                continue
            if not tablo.number % int(p1move) == 0:
                print("The number is not divisible by :", p1move)
                continue
            tablo.number = tablo.number / int(p1move)
            if p1move == '2':
                tablo.p2 += 1
            elif p1move == '3':
                tablo.p1 += 1
            if tablo.number%5 == 0:
                tablo.banka += 1
            break
        if tablo.number <= 10:
            tablo.p1 = tablo.p1 + tablo.banka
            return tablo
        if not tablo.number % 2 == 0 and not tablo.number % 3 == 0:
            tablo.number += 1
        print("")
        printscore(tablo)
        print("Current number: ",  tablo.number)
        print("")
        while True:
            p2move = input("Player 2  move: ").strip().lower()
            if p2move not in ['2', '3']:
                print("Invalid move. Please enter 2 or 3.")
                continue
            if not tablo.number % int(p2move) == 0:
                print("The number is not divisible by :", p2move)
                continue
            tablo.number = tablo.number / int(p2move)
            if p2move == '2':
                tablo.p1 += 1
            elif p2move == '3':
                tablo.p2 += 1
            if tablo.number%5 == 0:
                tablo.banka += 1
            break
        if tablo.number <= 10:
            tablo.p2 = tablo.p2 + tablo.banka
            return tablo
        if not tablo.number % 2 == 0 and not tablo.number % 3 == 0:
            tablo.number += 1
        print("")
        printscore(tablo)

#Funkcija, kas nosaka spēles beigas un izvada uzvarētāju
def gameend(tablo):
    print("Game end")
    printscorenobank(tablo)
    if tablo.p1 > tablo.p2:
        print("Player 1 wins!")
    elif tablo.p2 > tablo.p1:
        print("Player 2 wins!")
    else:
        print("It's a tie!")
    print("")
            


#Galvenā cilpa, kas ļauj spēlētājam sākt jaunu spēli vai iziet no programmas
while True:
    user_input = input("To start a new game type 's' to exit type 'e': ").strip().lower()
    if user_input == 's':
        number =startgame()
        tablo = score(0, 0, 0, number)
        results = game(tablo)
        gameend(results)
    elif user_input == 'e':
        break
    else:
        print("Invalid input. Please enter 's' to start a new game or 'e' to exit.")