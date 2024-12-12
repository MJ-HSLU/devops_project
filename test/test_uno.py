import pytest
import sys

sys.path += '../'

from server.py.uno import Uno, Card, Action, PlayerState, GameState, GamePhase

LIST_COLOR = ['red', 'blue', 'yellow', 'green']

def get_list_action_as_str(list_action) -> any:
    "helper function"
    line = ''
    for action in list_action:
        line += f'    - {action}\n'
    if len(line) > 0:
        line = line[:-1]
    return line

def test_set_state() -> None:
    """Test setting the game state."""
    game = Uno()
    state = GameState(
        cnt_player=2
    )
    game.set_state(state)
    assert game.state == state
    print(game.print_state())


def test_set_state_initial_setup() -> None:
    """Test setting the game state."""
    game = Uno()
    state = GameState(
        cnt_player=2
    )
    game.set_state(state)

    # check state
    print(game.state.list_card_discard)
    print(game.state.idx_player_active)
    print(game.state.direction)
    print(game.state.color)
    print(game.state.cnt_to_draw)
    print(game.state.has_drawn)

    # check total cards
    assert len(game.state.list_card_draw) + (game.state.CNT_HAND_CARDS * game.state.cnt_player) + len(game.state.list_card_discard) == 108, game.state

    # check player
    print(game.state.list_player)

def test_initialize_game_state():
    """Test if the game state initializes correctly."""
    game = Uno()
    state = GameState(cnt_player=3)
    game.set_state(state)
    assert game.state.cnt_player == 3
    assert len(game.state.list_player) == 3
    assert len(game.state.list_card_draw) == 108  # Standard UNO deck size
    assert game.state.phase == GamePhase.RUNNING
    assert game.state.idx_player_active is not None

def test_play_card():
    """Test if a card is played correctly, including color and discard updates."""
    game = Uno()
    state = GameState(
        cnt_player=2,
        list_player=[
            PlayerState(name="Player 1", list_card=[Card(color="red", number=5)]),
            PlayerState(name="Player 2", list_card=[]),
        ],
        list_card_discard=[Card(color="red", number=3)],
        idx_player_active=0,
        phase=GamePhase.RUNNING,
    )
    game.set_state(state)

    action = Action(card=Card(color="red", number=5))
    game.apply_action(action)

    assert len(game.state.list_card_discard) == 2
    assert game.state.list_card_discard[-1].number == 5
    assert game.state.idx_player_active == 1

def test_draw_card():
    """Test if drawing a card adds it to the player's hand and updates the state."""
    game = Uno()
    state = GameState(
        cnt_player=2,
        list_player=[
            PlayerState(name="Player 1", list_card=[]),
            PlayerState(name="Player 2", list_card=[]),
        ],
        list_card_draw=[Card(color="blue", number=7)],
        idx_player_active=0,
        phase=GamePhase.RUNNING,
    )
    game.set_state(state)

    action = Action(draw=1)
    game.apply_action(action)

    assert len(game.state.list_card_draw) == 0
    assert len(game.state.list_player[0].list_card) == 1
    assert game.state.list_player[0].list_card[0].number == 7
    assert game.state.has_drawn

def test_uno_call():
    """Test the UNO call functionality."""
    game = Uno()
    state = GameState(
        cnt_player=2,
        list_player=[
            PlayerState(name="Player 1", list_card=[Card(color="red", number=5), Card(color="blue", number=2)]),
            PlayerState(name="Player 2", list_card=[]),
        ],
        list_card_discard=[Card(color="red", number=3)],
        idx_player_active=0,
        phase=GamePhase.RUNNING,
    )
    game.set_state(state)

    action = Action(card=Card(color="red", number=5), uno=True)
    game.apply_action(action)

    assert len(game.state.list_player[0].list_card) == 1
    assert action.uno

def test_reverse_card():
    """Test if the reverse card updates direction and skips correctly for two players."""
    game = Uno()
    state = GameState(
        cnt_player=2,
        list_player=[
            PlayerState(name="Player 1", list_card=[Card(color="blue", symbol="reverse")]),
            PlayerState(name="Player 2", list_card=[]),
        ],
        list_card_discard=[Card(color="red", number=3)],
        idx_player_active=0,
        phase=GamePhase.RUNNING,
    )
    game.set_state(state)

    action = Action(card=Card(color="blue", symbol="reverse"))
    game.apply_action(action)

    assert game.state.direction == -1
    assert game.state.idx_player_active == 0

def test_list_action_card_matching_1() -> None:
    """Test 003: Test player card matching with discard pile card - simple cards [3 points]"""
    # self.game_server.game = Uno()

    for c, color in enumerate(LIST_COLOR):

        for number in range(10):

            # self.game_server.reset()
            game_server = Uno()

            idx_player_active = 0

            list_card_draw = []
            for color2 in LIST_COLOR:
                for number2 in range(10):
                    card = Card(color=color2, number=number2, symbol=None)
                    list_card_draw.append(card)

            card1 = Card(color=color, number=number, symbol=None)                               # same color, same number
            card2 = Card(color=color, number=(number + 1) % 10, symbol=None)                    # same color, different number
            card3 = Card(color=LIST_COLOR[(c + 1) % 4], number=number, symbol=None)             # different color, same number
            card4 = Card(color=LIST_COLOR[(c + 1) % 4], number=(number + 1) % 10, symbol=None)  # different color, different number
            list_card_discard = [card1]

            state = GameState(
                cnt_player=2,
                idx_player_active=idx_player_active,
                list_card_draw=list_card_draw,
                list_card_discard=list_card_discard,
                color=card1.color
            )
            game_server.set_state(state)
            state = game_server.get_state()
            player = state.list_player[idx_player_active]
            player.list_card = [card1, card2, card3, card4]
            game_server.set_state(state)
            state = game_server.get_state()
            str_state = f'GameState:\n{game_server.print_state()}\n'

            list_action_found = game_server.get_list_action()
            list_action_expected = []
            action = Action(card=card1, color=card1.color, draw=None)
            list_action_expected.append(action)
            action = Action(card=card2, color=card2.color, draw=None)
            list_action_expected.append(action)
            action = Action(card=card3, color=card3.color, draw=None)
            list_action_expected.append(action)
            action = Action(card=None, color=None, draw=1)
            list_action_expected.append(action)

            print("State Attributes: \n")
            print(' discard' )
            print( game_server.state.list_card_discard)
            print(' idx ' )
            print(game_server.state.idx_player_active)
            print(' dire ' )
            print(game_server.state.direction)
            print(' colo ' )
            print(game_server.state.color)
            print(' draw cnt ' )
            print(game_server.state.cnt_to_draw)
            print(' drawn ' )
            print(game_server.state.has_drawn)

            hint = str_state
            hint += '\nDiscard: '
            hint += str(list_card_discard)
            hint += '\nstatediscard: '
            hint += str(state.list_card_discard)
            hint += '\nplayer1 hand: '
            hint += str(state.list_player[idx_player_active])
            hint += '\nplayer2 hand: '
            hint += str(state.list_player[idx_player_active+1])
            hint += '\nError: "get_list_action" result is wrong.\n'
            hint += '  - Expected:\n'
            hint += f'{get_list_action_as_str(list_action_expected)}\n'
            hint += '  - Found:\n'
            hint += f'{get_list_action_as_str(list_action_found)}'
            assert sorted(list_action_found) == sorted(list_action_expected), hint



if __name__ == "__main__":

    test_set_state_initial_setup()