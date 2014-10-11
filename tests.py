from infection import total_infection, limited_infection
from database import Database, User

"""
Four connected components:
{1, 2, 3, 4}, {5, 6}, {7}, and {8}
"""

""" Test total infection. Entire connected components should be infected. """

""" 
Infect the first component (1,2,3,4) and not the second (5,6)
"""
# infecting any of 1, 2, 3, or 4 should infect all four
db = Database()

# starting version is 0 for all users b/c I hardcoded it that way for testing
for i in range(1, 5):
    assert(db.get_user(str(i)).version == 0)

for i in range(5, 7):
    assert(db.get_user(str(i)).version == 0)

u4 = db.get_user('4')

# infect the four users with version # 2
total_infection(db, u4, 2, set())

for i in range(1, 5):
    assert(db.get_user(str(i)).version == 2)
# and that users 5 and 6 are unaffected
for i in range(5, 7):
    assert(db.get_user(str(i)).version == 0)



"""
Infect the second (5,6) without affecting the first (1,2,3,4)
"""
db = Database()
u5 = db.get_user('5')

# infect users 5 and 6 with version # -3
total_infection(db, u5, -3, set())

for i in range(1, 5):
    assert(db.get_user(str(i)).version == 0)
# and that users 5 and 6 are unaffected
for i in range(5, 7):
    assert(db.get_user(str(i)).version == -3)



""" 
Test that infecting works in both directions ("coaches" and "is coached by").
"""
# user 6 coaches just user 5 and is coached by no one
# user 5 is coached by user 6 and coaches no one

# Test "is coached by"
db = Database()
u5 = db.get_user('5')
total_infection(db, u5, 11, set())
assert(db.get_user('5').version == 11)
assert(db.get_user('6').version == 11)

# Test "coaches"
db = Database()
u6 = db.get_user('6')
total_infection(db, u6, 15, set())
assert(db.get_user('5').version == 15)
assert(db.get_user('6').version == 15)







""" Test limited_infection. Will infect at most the target amount. """

"""
Exactly target can be infected. Only one combo of group sizes. target = 1
"""
db = Database()
limited_infection(db, target=1, new_ver=6)

# user 7 and 8 are both in groups of size 1
# it's not deterministic which one is chosen because groups are stored in a
# dictionary which has no order
u7 = db.get_user('7')
u8 = db.get_user('8')

# only one of user 7 or 8 should have version 6
for i in range(1, 7):
    assert(db.get_user(str(i)).version == 0)

assert((u7.version == 6 and u8.version == 0) or 
       (u7.version == 0 and u8.version == 6))



"""
Exactly target can be infected. Multiple combo of group sizes. target = 4.
Solution set should be just the one group of 4, instead of group of 2 + 1 + 1.
"""
db = Database()
limited_infection(db, target=4, new_ver=53)

# Users 1 - 4 should be infected
for i in range(1, 5):
    assert(db.get_user(str(i)).version == 53)

# and the rest not
for i in range(6, 9):
    assert(db.get_user(str(i)).version == 0)



"""
Exactly target can be infected. Multiple combo. target = 6.
Solution should be group of 4 + 2.
"""
db = Database()
limited_infection(db, target=6, new_ver=39)

# Users 1 - 6 should be infected
for i in range(1, 7):
    assert(db.get_user(str(i)).version == 39)

# and the rest not
for i in range(7, 9):
    assert(db.get_user(str(i)).version == 0)



"""
Exact target can NOT be infected. target = 9.
target_or_none = False
Solution should be group of 4 + 2 + 1 + 1.
"""
db = Database()
infected_num = limited_infection(db, target=9, new_ver=72)

assert(infected_num == 8)

# all Users infected
for i in range(1, 9):
    assert(db.get_user(str(i)).version == 72)



"""
Exact target can NOT be infected. target = 9.
target_or_none = True, so infect no one
"""
db = Database()
infected_num = limited_infection(db, target=9, new_ver=72, target_or_none=True)

assert(infected_num == 0)

# No one infected
for i in range(1, 9):
    assert(db.get_user(str(i)).version == 0)

