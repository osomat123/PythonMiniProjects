# Write your code here
import random

defeats = {'rock': ['paper'], 'paper': ['scissors'], 'scissors': ['rock']}

def findWinner(user,computer):

    if user == computer:
        return 0

    if user in defeats[computer]:
        return 1

    else:
        return -1

def get_rating(name):
    #name = name.upper()

    rating_file = open('rating.txt')
    data = rating_file.read()
    rating_file.close()

    if name in data:
     player_data = [player for player in data.split('\n') if name in player]
     rating = int(player_data[0].split()[1])

    else:
        rating = 0

    return rating

def write_data(name,new_rating,old_rating):
    #name = name.upper()
    new_data = name + " " + str(new_rating)
    old_data = name + " " + str(old_rating)

    rating_file = open('rating.txt', 'r')
    data = rating_file.read()
    rating_file.close()

    update_file = open('rating.txt','w')

    if name in data:
        data = data.replace(old_data,new_data)
    else:
        data += new_data

    print(data, end='\n', file=update_file)

    update_file.close()


def set_precedence(options):
    global defeats
    defeats = {}

    for option in options:
        i = options.index(option)
        part1 = options[:i]
        others = options[i+1:]
        others.extend(part1)
        defeats[option] = others[:len(others)//2]

    print(defeats)

name = input('Enter your name:')
print("Hello,",name)

rating = get_rating(name)
old_rating = rating

options = input().split(',')

if '' not in options:
    set_precedence(options)
else:
    options = ['rock','paper','scissors']

print("Okay, let's start")

valid_input = options + ['!exit','!rating']

while True:

    user = input()
    computer = random.choice(options)

    if user not in valid_input:
        print('Invalid input')
        continue

    if user == '!exit':
        print('Bye!')
        write_data(name,rating,old_rating)
        break

    if user == '!rating':
        print("Your rating:",rating)
        continue

    outcome = findWinner(user,computer)

    if outcome == 0:
        print(f'There is a draw ({user})')
        rating += 50

    elif outcome == 1:
        print(f'Well done. The computer chose {computer} and failed')
        rating += 100

    else:
        print(f'Sorry, but the computer chose {computer}')