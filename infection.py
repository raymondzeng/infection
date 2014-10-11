def total_infection(db, patient_zero, new_version, infected_ids):
    """
    Update the version number for every user connected to patient_zero.
    This function assumes that the starting state (before infection) is valid, 
    i.e., every node in a given connected component has the same version number.

    Uses a recursive DFS approach to infect the connected component. 

    db  - the database where users can be fetched and updated
    patient_zero  - the starting node
    new_version  - the version to update/infect 
    infected_ids  - set to keep track of nodes already visited/infected; modified in place in recursive calls
    """
    # this node already visited
    if patient_zero.id in infected_ids:
        return
    
    # i'd like to be able to just do patient_zero.version = new_version
    # and have it persist to the data store

    # infect this node and indicated it's been infected 
    # by adding to infected_ids
    db.update_user_ver(patient_zero.id, new_version)
    infected_ids.add(patient_zero.id)

    # then infect all its neighbors
    for user_id in patient_zero.students + patient_zero.coaches:
        # neighbor already infected, so skip it
        if user_id in infected_ids:
            continue
            
        # fetch this user from some given database
        user = db.get_user(user_id)
        total_infection(db, user, new_version, infected_ids)

def limited_infection(db, target, new_version):
    """
    Infect at most the target number of users with new_version.
    """
    pass
