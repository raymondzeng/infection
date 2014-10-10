"""
Infection algorithms are agnostic to how the user is stored and retrieved. 
The data could all be in memory, a database, or online for example.

I also designed this with the intention that User objects should be retrieved lazily because given enough users, the data can't completely fit in memory.
"""

class User:
    def __init__(self, id, init_version, coaches=set(), students=set()):
        self.id = id
        self.version = init_version 

        # coaches and students could be combined for infection purposes,
        # but it may be useful to have them separate
        self.coaches = coaches # set of ids, not User objects
        self.students = students # set of ids, not User objects

    def __str__(self):
        return str({'id': self.id,
                   'version': self.version,
                   'coaches': self.coaches,
                   'students': self.students})

class Database:
    def __init__(self):
        # this could easily be switched out with a 
        # connection to a db for example, but don't forget to
        # modify the other class functions as necessary 
        self.users = { '1': User('1', 0, [], ['2', '3']),
                       '2': User('2', 0, ['1'], []),
                       '3': User('3', 0, ['1'], ['4']),
                       '4': User('4', 0, ['3'], []),
                       '5': User('5', 0, ['6'], []),
                       '6': User('6', 0, [], ['5']) }

    def get_user(self, user_id):
        return self.users[user_id]
        
    def update_user_ver(self, user_id, new_ver):
        self.users[user_id].version = new_ver

    def __str__(self):
        s = ''
        for u in self.users.values():
            s = s + str(u) + '\n'
        return s
            
