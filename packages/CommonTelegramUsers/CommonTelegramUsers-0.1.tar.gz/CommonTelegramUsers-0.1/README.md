# CommonTelegramUsers

A library for finding common users between multiple telegram groups, supergroups or channels

## Installation

You can install this library with pip:

```bash
pip install CommonTelegramUsers
```
## Usage

To use the library, simply import the library and use the find function to retrieve the common users

## Syntax

```python
find(api_id, api_hash, name, blacklist, chat1, chat2, ....., chatN)
```
api_id: int (Retrieve from my.telegram.org)

api_hash: str (Retrieve from my.telegram.org)

name: str (Any random name for session file, make sure to use the same name if you don't want to log in everytime)

blacklist: set (Set of telegram user ids to be ignored from final common users set)

chat1 -> chatN: str or int (Username, link or id of the group/channel/supergroup)
