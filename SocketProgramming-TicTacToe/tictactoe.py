cells = '_________'
state = [[cells[i],cells[i+1],cells[i+2]] for i in range(len(cells)) if i%3 == 0]
players = ['X','O']
move_count = 0


def check_for_winning_pattern(patterns):
    winning_patterns = ['XXX', 'OOO']
    for winner in winning_patterns:
        if winner in patterns:
            return winner

    return None


def find_winner():
    patterns = []

    # Check rows
    for i in range(3):
        pattern = ''
        pattern += state[i][0] + state[i][1] + state[i][2]
        patterns.append(pattern)

    # Check cols
    for i in range(3):
        pattern = ''
        pattern += state[0][i] + state[1][i] + state[2][i]
        patterns.append(pattern)

    # Check diags
    pattern = ''
    for i in range(3):
        pattern += state[i][i]
    patterns.append(pattern)

    pattern = ''
    for i in range(3):
        pattern += state[i][2 - i]
    patterns.append(pattern)

    # Find if winner is there
    winner = check_for_winning_pattern(patterns)

    return winner[0] if winner else None


def check_status():
    winner = find_winner()

    if winner:   # Winner found
        return winner
    elif not winner and not is_empty():    # Draw
        return "Draw"
    else:                   # Match still going on
        return None


def is_empty():
    for i in range(3):
        for j in range(3):
            if state[i][j] == '_':
                return True

    return False


def get_state_str():
    cells = ''
    for row in state:
        for item in row:
            cells += item

    return cells

def add_to_state(coords, symbol):
    x, y = coords
    state[x][y] = symbol