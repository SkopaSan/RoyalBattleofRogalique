from game import Game, OutMessage
from events import DialogMessage
import statistics
number_of_tests = 1
#char_class = "Mage"
#char_class = "Rogue"
char_class = "Warrior"

print_rep = False

class MyMessageTest:
    def __init__(self, text):
        self.text = text
        self.chatid = 1


    def get_type(self):
        """
        Returns message type
        """
        return "text"

    def get_content(self):
        """
        Returns message content
        """
        return self.text

    def get_chat_id(self):
        """
        Returns message chat id
        """
        return self.chatid

    def get_user_id(self):
        """
        Returns message user id
        """
        id = {"id":1}
        return id


class GameManager():
    """Holds games for all players, rutes and manages them"""

    def __init__(self):
        self.user_list = dict()

    def merge_messages(self, messages):
        """
        Takes a list of messages
        Merges every subsequent message to one player, into bigger message
        """
        from itertools import groupby
        result = []
        separator = "\n\n"
        for key, group in groupby(messages, lambda x: x.chat_id):
            res = ""
            for message in group:
                if res:
                    res += separator + message.text
                else:
                    res += message.text
            result.append(OutMessage(res, key, key))
        return result

    def generate_replays(self, text):

        messages_to_send = []
        new_message = MyMessageTest(text)
        if new_message.get_type() != 'text':
            pass
        else:
            player_id = new_message.get_user_id()
            chat_id = new_message.get_chat_id()
            content = new_message.get_content()
            if player_id['id'] not in self.user_list.keys() and content == '/start':
                messages_to_send.append(OutMessage(
                    'Ready Player One', chat_id, player_id))
                messages_to_send.append(OutMessage(DialogMessage(
                    'start_game').get_message(), chat_id, player_id))
                player_game = Game(chat_id, player_id)
                self.user_list[player_id['id']] = player_game
            elif player_id['id'] in self.user_list:
                if new_message.get_content() == '/restart':
                    self.user_list.pop(player_id['id'])
                    messages_to_send.append(OutMessage(
                        'Game reset', chat_id, player_id))
                else:
                    player_game = self.user_list[player_id['id']]
                    game_state = player_game.check_state()
                    if game_state == 'Game Start':
                        player_game.game_start(content)
                    elif game_state == 'Base':
                        player_game.base(content)
                    elif game_state == 'Battle Choice':
                        player_game.battle_choice(content)
                    elif game_state == 'Item Choice':
                        player_game.item_choice(
                            content)
                    elif game_state == 'Shop':
                        player_game.shop(content)
                    messages_to_send += player_game.send_all_messages()
            else:
                messages_to_send.append(OutMessage(
                    'Type /start to enter the game', chat_id, player_id))
        return self.merge_messages(messages_to_send)

game_manager = GameManager()
def get_replay(text):
    replays = game_manager.generate_replays(text)
    if print_rep:
        print(replays[0].text)
def buy_potion(game):
    get_replay("B")
    while game.get_playerchar().get_gold() > 20:
        get_replay("P")
    get_replay("E")
def compare(game):
    char_item = game.playerchar.get_inventory()[game.item.get_type()]
    #print(char_item.get_bonus_attack())
    compare_atk = game.item.get_bonus_attack() - char_item.get_bonus_attack()
    compare_def = game.item.get_bonus_defence() - char_item.get_bonus_defence()
    compare_hp = game.item.get_bonus_hp() - char_item.get_bonus_hp()
    compare_mp = game.item.get_bonus_mp() - char_item.get_bonus_mp()
    #print(compare_atk," ",compare_def," ",compare_hp," ",compare_mp)
    if compare_atk < 0 or compare_def < 0:
        get_replay("N")
    else:
        get_replay("E")
    #print(replays[0].text)
#def monster_cheking(game):
    #print()
def main():
    get_replay("/start")
    lvllist = []
    for _ in range(number_of_tests):
        get_replay(char_class)
        game = game_manager.user_list[1]
        player = game.get_playerchar()
        while player.is_alive() and player.get_lvl() < 100:
            # #text = input()
            # get_replay(text)
            if game._game_state == "Base":
                if player.get_current_hp() < player.get_maxhp() and player.get_gold() > 10:
                    buy_potion(game)
                text = "Y"
            elif game._game_state == "Battle Choice":
                text = "Y"
                #print(game.battle_choice().enemies)
            elif game._game_state == "Item Choice":
                text = "E"
                # print(game.item.get_bonus_attack())
                item = game.playerchar.get_inventory()[game.item.get_type()]
                if item is not None:
                    compare(game)
            get_replay(text)
            lvl = player.get_lvl()
        #print(count)
        lvllist.append(lvl)
    print(lvllist)
    print("Class: ", char_class)
    print("Number of tests: ", number_of_tests)
    print("Max level: ", max(lvllist))
    print("Average level: ", sum(lvllist)/number_of_tests)
    print("Median: ", statistics.median(lvllist))
if __name__ == '__main__':
    main()

