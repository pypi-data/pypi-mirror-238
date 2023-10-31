# CommonTelegramUsers

A library for finding common users between multiple telegram groups, supergroups or channels

## Installation

You can install this library with pip:

Recommended:
```bash
pip install CommonTelegramUsers[tgcrypto]
```
or

Slower:
```bash
pip install CommonTelegramUsers
```

## Usage

To use the library, simply import the library and use the find function to retrieve the common users

## Syntax

```python
finds(api_id, api_hash, name, blacklist, verbose, chat1, chat2, ....., chatN)
```
or
```python
find(api_id, api_hash, (chat1, chat2, ....., chatN), name, blacklist, verbose)
```
api_id: int (Retrieve from my.telegram.org)

api_hash: str (Retrieve from my.telegram.org)

name: str (Any random name for session file, make sure to use the same name if you don't want to log in everytime)

blacklist: set (Set of telegram user ids to be ignored from final common users set)

verbose: bool (Print processing logs)

chat1 -> chatN: str or int (Username, link or id of the group/channel/supergroup)
