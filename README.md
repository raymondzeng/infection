## Run Tests
python tests.py

## Files
Infection logic is in infection.py.  
User info management is in database.py.  

## Definitions 
A connected component (cc for short) is a graph of users where for every user in the cc, there is a path to every other user.

Since "caoches" and "is coached by" are treated equally in terms of ability to pass on an infection, every cc is undirected. 

A valid state is defined to be a state where every user in a given cc has the same version number.


## Total Infection Spec
Given a user, infects every user in the same cc.
Assumes the precondition that all users are in a valid state. Otherwise may cause the algorithm to terminate early.


## Limited Infection Spec
Given a target infection number, infects at most that many users. There is a flag (target_or_none) so that you can tell it to infect no one if the exact number is not possible. 

I interpretted limited infection to mean that the post-state should also be a valid state (all users in a given cc have same version). 

If we wanted limited infection to be such that you want to infect exactly target and are okay with an invalid state (users in a given cc can have different versions), you can modify total_infection to check the size of how many people infected so far, and if target has been reached, terminate. Then just use _find_optimal_groups to infect as many fully as possible, then pick the next largest group to infect partially.


## Limited Infection Design
I chose to keep track of the size of each cc (every cc has an id and every user in a cc stores that id). This is a time tradeoff that is well worth the space because otherwise we would have to iterate through all users and calculate sizes of each cc every time. One negative is that we have to be careful to keep this size information updated which may be non trivial: we have to update the sizes when users are added to/removed from/switch cc and when cc combine or merge. 
  
We can store cc sizes separately allowing for more modular and distributed design. Because we know the sizes of every cc, we can calculate which groups should be infected to reach our target without looking at any users. If we don't reach our target and target_or_none is True, we never even have to access users. 


## Data Interface Design
Database in databse.py is an interface for handling User objects, specifically retrieving and updating them. Where and how user info is stored and retrieved is completely abstracted away from infection.py and can easily be switched out (as long as the interface is maintained). 

For example, let's say user info is stored in a SQL database locally or remotely. When infection.py needs to retrieve a user, if that user hasn't been retrieved before and thus has not been cached, Database can go to the SQL db, get it, and cache it. 

This takes into account the fact that all user info probably can't be loaded into memory. Since infection.py will rarely need to look at all users anyways, we save ourselves time and space. 

