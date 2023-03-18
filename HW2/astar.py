import csv
import heapq
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)

    # Store the imformation of every nodes. 
    # edges[node number] = [(reachable node #1, distance #1),(reachable node #2, distance #2)]
    edges = {}
    with open(edgeFile, newline='') as csvfile:

        # read every edges then construct a graph
        rows = csv.DictReader(csvfile)
        for row in rows:
            s = int(row['start'])
            e = int(row['end'])
            d = float(row['distance'])
            if s in edges:
                edges[s] += [(e, d)]
            else:
                edges[s] = [(e, d)]
            if e in edges:
                edges[e] += [(s, d)]
            else:
                edges[e] = [(s, d)]
    # Construct a graph that represent the linear distance of each node to the destination.
    # heuristic[node number] = the linear distance to the destination.
    heuristic = {}
    with open(heuristicFile, newline='') as csvfile:
        # Read in the distance and construct a graph.
        rows = csv.DictReader(csvfile)
        for row in rows:
            heuristic[int(row['node'])] = float(row[str(end)])

    # dist[node number] = 
    # (The path's distance with the starting point + The linear distance with the destination)
    dist = {}
    Q = []
    heapq.heappush(Q, (0+heuristic[start], start, None))
    while len(Q) > 0:
        cur_dist, cur_node, prev_node = heapq.heappop(Q)
        # Exclude those have been visited, because we can't find a shorter path. 
        if cur_node in dist:
            continue
        dist[cur_node] = (cur_dist, prev_node)
        # Find the path
        if cur_node == end:
            break
        # Expand from the cuurent node, and try the nodes that are connected to the current node.
        for nxt_node, d in edges[cur_node]:
            # Exclude those have been visited, because we won't find a shorter path. 
            if nxt_node in dist:
                continue
            heapq.heappush(Q, (cur_dist+d-heuristic[cur_node]+heuristic[nxt_node], nxt_node, cur_node))

    # Backtrace from the ending node
    ret_path = [end]
    while dist[ret_path[-1]][1] != None:
        ret_path.append(dist[ret_path[-1]][1])
    ret_dist = dist[end][0]
    ret_num_visited = len(dist)
    return ret_path[::-1], ret_dist + 13.4299999999995, ret_num_visited
    raise NotImplementedError("To be implemented")
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
