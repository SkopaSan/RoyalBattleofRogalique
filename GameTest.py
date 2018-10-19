from game import Game, OutMessage
from events import DialogMessage
from item import Item
number_of_tests = 100
char_class = "Warrior"
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

                # print(
                #      f"Player: {player_id}, Chat: {chat_id}, Content: {content}")
                messages_to_send.append(OutMessage(
                    'Ready Player One', chat_id, player_id))
                messages_to_send.append(OutMessage(DialogMessage(
                    'start_game').get_message(), chat_id, player_id))
                player_game = Game(chat_id, player_id)
                self.user_list[player_id['id']] = player_game
            elif player_id['id'] in self.user_list:
                if new_message.get_content() == '/restart':
                    # print(
                    #     f"Player: {player_id}, Chat: {chat_id}, Content: {content}")
                    self.user_list.pop(player_id['id'])
                    messages_to_send.append(OutMessage(
                        'Game reset', chat_id, player_id))
                else:
                    player_game = self.user_list[player_id['id']]
                    game_state = player_game.check_state()
                    # print(
                    #      f"Player: {player_id}, Chat: {chat_id}, Content: {content}, Game State: {game_state}")
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

def main():
    game_manager = GameManager()
    text = "/start"
    replays = game_manager.generate_replays(text)
    print(replays[0].text)
    lvllist = []
    for _ in range(number_of_tests):
        text = char_class
        replays = game_manager.generate_replays(text)
        print(replays[0].text)

        game = game_manager.user_list[1]
        count = 0
        while game.get_playerchar().is_alive():
            #text = input()
            replays = game_manager.generate_replays(text)
            print(replays[0].text)
            game = game_manager.user_list[1]
            print(game._game_state)
            game = game_manager.user_list[1]
            if game._game_state == "Base":
                if game.get_playerchar().get_current_hp() < game.get_playerchar().get_maxhp() and game.get_playerchar().get_gold() > 10:
                    text = "B"
                    replays = game_manager.generate_replays(text)
                    print(replays[0].text)
                    while game.get_playerchar().get_gold() > 20:
                        text = "P"
                        replays = game_manager.generate_replays(text)
                        print(replays[0].text)
                    text = "E"
                    replays = game_manager.generate_replays(text)
                    print(replays[0].text)
                text = "Y"
            elif game._game_state == "Battle Choice":
                text = "Y"
            elif game._game_state == "Item Choice":
                bonus_atk = game.item.get_bonus_attack()
                current_atk = game.item._bonus_attack
                bonus_def = game.item.get_bonus_defence()
                current_def = game.item._bonus_defence
                print("ATTAK_BONUS= ",bonus_atk)
                print("CURRENT ATTACK= ", current_atk)
                print(current_atk - bonus_atk)
                print(current_def - bonus_def)
                if (current_atk - bonus_atk) < 0 or (current_def - bonus_def) < 0:
                    text = "N"
                    print("ШМОТ ГОВНО!")
                    print("ШМОТ ГОВНО!")
                    print("ШМОТ ГОВНО!")
                    print("ШМОТ ГОВНО!")
                    print("ШМОТ ГОВНО!")

                else:
                    text = "E"
                    print("Отличный шмот!")
                    print("Отличный шмот!")
                    print("Отличный шмот!")
                    print("Отличный шмот!")
                    print("Отличный шмот!")
                    print("Отличный шмот!")

            replays = game_manager.generate_replays(text)
            print(replays[0].text)
            HP = game.get_playerchar().get_current_hp()
            print("HP = ",  HP)
            count += 1
            lvl = game.get_playerchar().get_lvl()
        #print(count)
        lvllist.append(lvl)
    print(lvllist)
    print(max(lvllist))
    print(sum(lvllist)/number_of_tests)
    #print(max(lvllist))
if __name__ == '__main__':
    main()