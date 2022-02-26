import socket

HOST = "127.0.0.1"
PORT = 12345

players = ['X','O']

def print_state(state):
    print('---------')
    for row in state:
        print('|', end=' ')
        for ele in row:
            if ele == '_':
                print(' ', end=' ')
                continue
            print(ele, end=' ')
        print('|')
    print('---------')


def get_input(state):
    coords = None
    while not isinstance(coords, tuple):
        move = [int(i) for i in input("Enter the coordinates: ").split(maxsplit=1) if i.isdigit()]

        if len(move) == 2:
            x = move[0] - 1
            y = move[1] - 1

            if x in range(3) and y in range(3):
                if state[x][y] == '_':
                    coords =  (x, y)
                else:
                    print("This cell is occupied! Choose another one!")
            else:
                print("Coordinates should be from 1 to 3!")

        elif len(move) < 2:
            print("You should enter numbers!")

    return coords


def receive_data(s):
    received_data = s.recv(50).decode().split("|")

    data = received_data[0]
    code = int(received_data[-1])

    if len(received_data) == 2:
        info = None
    else:
        info = received_data[1]

    state = [[data[i], data[i + 1], data[i + 2]] for i in range(len(data)) if i % 3 == 0]
    if code:
        return state, info, code

    return state, info, code


def receive_player_id(s):
    data = s.recv(50).decode()
    print(data)

    player_id = 0 if "'X'" in data else 1
    print(f"Your Player id: {player_id}")
    return player_id


def send_data(s, coords):
    x, y = coords
    data = bytes(f"{x} {y}", encoding="utf-8")
    s.sendall(data)


def play_game(s):
    player_id = receive_player_id(s)
    state, info, code = receive_data(s)
    print_state(state)
    move_id = 0
    while True:
        if code:
            if player_id == move_id:
                coords = get_input(state)
                send_data(s, coords)

                x, y = coords
                state[x][y] = players[move_id]

            else:
                state, info, code = receive_data(s)

            print_state(state)
            move_id = (move_id * -1) + 1

        else:
            if player_id == move_id:
                print_state(state)

            print(info)
            break

        print()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(s.recv(1024).decode())
    play_game(s)
