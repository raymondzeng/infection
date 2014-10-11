def total_infection(db, patient_zero, new_version, infected_ids):
    """
    Update the version number for every user connected to patient_zero.
    This function assumes that the starting state (before infection) is valid, 
    i.e., every node in a given connected component has the same version number.

    Uses a recursive DFS approach to infect the connected component. 

    db  - the Database where users can be fetched and updated
    patient_zero  - the starting node
    new_version  - the version to update/infect 
    infected_ids  - set to keep track of nodes already visited/infected; modified in place in recursive calls
    """
    # this node already visited
    if patient_zero.id in infected_ids:
        return
    
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
    

def limited_infection(db, target=0, new_ver=0, target_or_none=False):
    """
    Infect at most the target number of users with new_version.
    
    db  - the Database where users can be fetched and updated
    target  - at most how many users to infect (unless @target_or_none)
    new_ver  - the version to infect users with
    target_or_none  - if True, only infect if exactly target can be infected.
                      If False, infect as many as possible <= target

    Returns the number of users infected.
    """
    # a group is synonymous with a connected component
    groups, infected = _find_optimal_groups(list(db.sizes.items()), target)
    
    # not possible to infect exactly @target users
    # and @target_or_none flag is True so infect no one
    if target_or_none and infected != target:
        return 0

    for group_id in groups:
        # find a user with in the group
        user = db.find_one_in(group_id) 
        # infect everyone in that group
        total_infection(db, user, new_ver, set())

    return infected
        

def _find_optimal_groups(sizes, target):
    """
    A solution to the subset sum problem where the threshold is @target.
    
    If multiple solution sets have the same best sum, the solution set with
    the least number of groups is selected. 
    i.e. If sizes = [('group1',10), ('group2',2), ('group3',1), ('group4',1)]
    and target = 12, 'group1' and 'group2' will be selected instead of 
    groups 1, 3 and 4.
    
    Also, when groups have the same size and one of them needs to be chosen,
    the one chosen is determined by the ordering of the list @size.
    i.e. In a solution where only one group of size 1 is chosen, 
    group3 has precendence over group4.

    Returns tuple (list of group_ids, number of would-be infected)
    Reference: https://www.cs.cmu.edu/~ckingsf/class/02713-s13/lectures/lec15-subsetsum.pdf
    """
    # create the dynamic programming lookup table
    dp_table = [[0 for _ in xrange(target + 1)] for _ in xrange(len(sizes) + 1)]
 
    for n, (group_id, size) in enumerate(sizes):
        for w in range(target):
            if size > w + 1: # including this group exceeds the limit
                dp_table[n + 1][w + 1] = dp_table[n][w + 1]
            else:
                # choose the maximum of including this gruop or not
                dp_table[n + 1][w + 1] = max(dp_table[n][w + 1],
                                             dp_table[n][w + 1 - size] + size)
 
    # backtrack the table to get the 
    groups = []
    s = target
    for n in range(len(sizes), 0, -1):
        added = dp_table[n][s] != dp_table[n-1][s]
 
        if added:
            group_id, size = sizes[n - 1]
            groups.append(group_id)
            s -= size
            
    return (groups, target - s)
