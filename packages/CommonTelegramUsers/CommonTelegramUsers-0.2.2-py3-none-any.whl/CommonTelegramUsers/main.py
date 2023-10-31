from pyrogram import Client
from typing import Set, Tuple

def get_all_participants(app: Client, chat: int, verbose: bool = False) -> Set[int]:
    all_participants: Set = set()
    
    if verbose:
        n: int = 0
        for member in app.get_chat_members(chat_id=chat):
            all_participants.add(member.user.id)
            n += 1
            print(f"{n} users processed", end="\r")
    else:
        for member in app.get_chat_members(chat_id=chat):
            all_participants.add(member.user.id)

    return all_participants

def process_chat(chat) -> int|str:
    if chat.isdigit(): return int(chat)
    else: return chat.replace("@", "").replace("/", "").replace("https:t.me", "")

def find(args: Tuple[str|int], api_id: int, api_hash: str, name: str = "CTU", blacklist: Set[int] = set(), verbose: bool = False) -> Set[int]:
    app: Client = Client(name=name, api_id=api_id, api_hash=api_hash)

    with app:
        init: Set[int] = get_all_participants(app=app, chat=process_chat(args[0]), verbose=verbose) - blacklist
        
        for chat in args[1:]:
            init: Set[int] = init & get_all_participants(app=app, chat=process_chat(chat))

        return init

def finds(api_id: int, api_hash: str, name: str = "CTU", blacklist: Set[int] = set(), verbose: bool = False, *args: Tuple[str|int]) -> Set[int]:
    app: Client = Client(name=name, api_id=api_id, api_hash=api_hash)

    with app:
        init: Set[int] = get_all_participants(app=app, chat=process_chat(args[0]), verbose=verbose) - blacklist
        
        for chat in args[1:]:
            init: Set[int] = init & get_all_participants(app=app, chat=process_chat(chat))

        return init
