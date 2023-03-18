import csv
import sys
edgeFile = 'edges.csv'

#sys.setrecursionlimit(100000)

# Store the imformation of every nodes 
# EDGES[node number] = [(reachable node #1, distance #1),(reachable node #2, distance #2)]
EDGES = {}
with open(edgeFile, newline='') as csvfile:

    # read every edges then construct a graph
    rows = csv.DictReader(csvfile)
    for row in rows:
        s = int(row['start'])
        e = int(row['end'])
        d = float(row['distance'])
        if s in EDGES:
            EDGES[s] += [(e, d)]
        else:
            EDGES[s] = [(e, d)]
# Variables have to be put outside of the function because we applied the recursive version
PATH = []
DIST = 0
VISITED = set()
BEGIN = True

def dfs(start, end):
    # Begin your code (Part 2)
    global PATH
    global DIST
    global VISITED

    PATH.append(start)
    VISITED.add(start)

    # The end of the recursion
    if(start == end):
        return PATH, DIST, len(VISITED)+1

    # Visit every node which 'start' can reach and we nver tried
    for nxt_node, d in EDGES[start]:
       
        if not nxt_node in EDGES:
            continue
        # If the node have been visited, then skip. 
        if nxt_node in VISITED:
            continue
        
        # Keep going
        DIST += d
        ret_path, ret_dist, ret_num_visited = dfs(nxt_node, end)
        if ret_path != []:

            # Find a path successfully, and return the path
            return ret_path, ret_dist, ret_num_visited
        else:

            # No way to go, try the next one
            DIST -= d
    
    # No way to go
    PATH.pop()
    return [],None,None
    raise NotImplementedError("To be implemented")
   
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(426882161, 1737223506)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
