from pyrogram import Client
from typing import Set, Tuple

def get_all_participants(app: Client, chat: int) -> Set[int]:
    all_participants: Set = set()
    n: int = 0

    for member in app.get_chat_members(chat_id=chat):
        all_participants.add(member.user.id)
        n += 1

    return all_participants

def process_chat(chat) -> int|str:
    if chat.isdigit(): return int(chat)
    elif chat == "exit" or chat.strip() == "": exit()
    else: return chat.replace("@", "").replace("https://t.me/", "")

def find(api_id: int, api_hash: str, name: str = "CTU", blacklist: Set[int] = set(), *args: Tuple[str|int]) -> Set[int]:
    app: Client = Client(name=name, api_id=api_id, api_hash=api_hash)

    with app:
        init: Set[int] = get_all_participants(app=app, chat=process_chat(args[0])) - blacklist
        
        for chat in args[1:]:
            init: Set[int] = init & get_all_participants(app=app, chat=process_chat(chat))

        return init
