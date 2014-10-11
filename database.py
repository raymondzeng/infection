"""
Infection algorithms are agnostic to how the user is stored and retrieved. 
The data could all be in memory, a database, or online for example.

I also designed this with the intention that User objects should be retrieved lazily because given enough users, the data can't completely fit in memory.
"""

class User:
    def __init__(self, id, init_version, group_id, coaches, students):
        self.id = id
        self.version = init_version 
        self.group_id = group_id

        # coaches and students could be combined for infection purposes,
        # but it may be useful to have them separate
        self.coaches = coaches # set of ids, not User objects
        self.students = students # set of ids, not User objects

    def __str__(self):
        return str({'id': self.id,
                    'version': self.version,
                    'group_id': self.group_id,
                    'coaches': self.coaches,
                    'students': self.students})

class Database:
    def __init__(self):
        # keep track of the sizes of each individual connected component 
        # so limited_infection is easy(er). Trading space for time.
        # Need to make sure to keep this updated whenever 
        # you add/remove user(s) from a connected component or link/merge
        # two together
        self.sizes = { 'group_1': 4,
                       'group_2': 2 }
        
        # this could be an interface to an actual database (SQL, NoSQL etc)
        # or to a web store, or just a file on the hard drive
        # for retrieving users that haven't already been retrieved and cached
        # for testing purposes, I won't be using this
        self.database = None

        # maintain a cache of users that have already been retrieved 
        # for testing purposes, all users will already be cached
        self.user_cache = { '1': User('1', 0, 'group_1', [], ['2', '3']),
                            '2': User('2', 0, 'group_1', ['1'], []),
                            '3': User('3', 0, 'group_1', ['1'], ['4']),
                            '4': User('4', 0, 'group_1', ['3'], []),
                            '5': User('5', 0, 'group_2', ['6'], []),
                            '6': User('6', 0, 'group_3', [], ['5']) }

    def get_user(self, user_id):
        if user_id in self.user_cache:
            return self.user_cache[user_id]
        
        # not used for my testing purposes but the general gist of
        # how self.user_cache and self.database are intended to be used
        try:
            user = self.database.retrieve(user_id)
            # cache it
            self.user_cache[user_id] = user
            return user
        except:
            raise Exception("User doesn't exist: " + user_id)

    def update_user_ver(self, user_id, new_ver):
        self.user_cache[user_id].version = new_ver
        # would also need to propogate the changes to the database 
        
    def __str__(self):
        s = ''
        for u in self.users.values():
            s = s + str(u) + '\n'
        return s
            
