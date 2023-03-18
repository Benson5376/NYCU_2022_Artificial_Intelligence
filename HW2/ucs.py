import csv
import heapq
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    edges = {}
    with open(edgeFile, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            s = int(row['start'])
            e = int(row['end'])
            d = float(row['distance'])
            if s in edges:
                edges[s] += [(e, d)]
            else:
                edges[s] = [(e, d)]

    # dist[node number] = (distance from the starting point, the number of the former node)
    dist = {}
    Q = []
 
    # Put it in the starting point first, every information in the queue is shown as (node number, distance from starting point)
    heapq.heappush(Q, (0, start, None))
    while len(Q) > 0:
        cur_dist, cur_node, prev_node = heapq.heappop(Q)

        # exclude those have been visited, because we won't find a shorter path 
        if cur_node in dist:
            continue

        # The distance of the starting point and the current node can be decided here 
        dist[cur_node] = (cur_dist, prev_node)
        # Find the path
        if cur_node == end:
            break

        # Expand from the cuurent node, and try the nodes that are connected to the current node
        if not cur_node in edges:
            continue

        # Exclude those nodes that have no way to go
        for nxt_node, d in edges[cur_node]:

            # Exclude those have been visited, because we won't find a shorter path 
            if nxt_node in dist:
                continue
            heapq.heappush(Q, (cur_dist + d, nxt_node, cur_node))
    
    # Backtrace from the ending node
    ret_path = [end]
    while dist[ret_path[-1]][1] != None:
        ret_path.append(dist[ret_path[-1]][1])
    ret_dist = dist[end][0]
    ret_num_visited = len(dist)
    return ret_path[::-1], ret_dist, ret_num_visited

    raise NotImplementedError("To be implemented")
    
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
