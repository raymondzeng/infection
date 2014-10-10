from infection import total_infection
from database import Database, User

"""
Two connected components:
1, 2, 3, 4 and
5, 6
"""

""" 
Infect the first component (1,2,3,4) and not the second (5,6)
"""
# infecting any of 1, 2, 3, or 4 should infect all four
db = Database()

# starting version is 0 for all users
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
for i in range(1, 5):
    assert(db.get_user(str(i)).version == 2)
for i in range(5, 7):
    assert(db.get_user(str(i)).version == 0)

u5 = db.get_user('5')

# infect users 5 and 6 with version # -3
total_infection(db, u5, -3, set())

for i in range(1, 5):
    assert(db.get_user(str(i)).version == 2)
# and that users 5 and 6 are unaffected
for i in range(5, 7):
    assert(db.get_user(str(i)).version == -3)


""" 
Test that infecting works in both directions ("coaches" and "is coached by").
"""
# user 6 coaches just user 5 and is coached by no one
# user 5 is coached by user 6 and coaches no one

# Test "is coached by"
u5 = db.get_user('5')
total_infection(db, u5, 11, set())
assert(db.get_user('5').version == 11)
assert(db.get_user('6').version == 11)

# Test "coaches"
u6 = db.get_user('6')
total_infection(db, u6, 15, set())
assert(db.get_user('5').version == 15)
assert(db.get_user('6').version == 15)
