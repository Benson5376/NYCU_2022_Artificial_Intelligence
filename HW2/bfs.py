import csv
from queue import Queue
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)

    # Store the imformation of every node.
    # edges[node number] = [(reachable node #1, distance #1),(reachable node #2, distance #2)] 
    edges = {}
    with open(edgeFile, newline='') as csvfile:
        # read every edges and construct a graph
        rows = csv.DictReader(csvfile)
        for row in rows:
            s = int(row['start'])
            e = int(row['end'])
            d = float(row['distance'])
            if s in edges:
                edges[s] += [(e, d)]
            else:
                edges[s] = [(e, d)]
    # dist[number] = (distance from the starting point, the previous node's number)
    dist = {start: (0, None)}
    Q = Queue()
    # Put it in the starting point first, every information in the queue is shown as (node number, distance from starting point)
    Q.put_nowait((start,0))
    while not Q.empty():
        cur_node,cur_dist = Q.get_nowait()
        # Expand from the cuurent node, and try the nodes that are connected to the current node
        if not cur_node in edges:
            continue
        for nxt_node, d in edges[cur_node]:
            # Exclude those that have been visited
            if nxt_node in dist:
                continue
            dist[nxt_node] = (cur_dist + d, cur_node)
            Q.put_nowait((nxt_node, cur_dist+d))
            # The path is found, but not necessarily the shortest path
            if nxt_node == end:
                break

    # Backtrace from the ending node, by the previous node of each nodes
    ret_path = [end]
    while dist[ret_path[-1]][1] != None:
        ret_path.append(dist[ret_path[-1]][1])
    ret_dist = dist[end][0]
    ret_num_visited = len(dist)
    return ret_path[::-1], ret_dist, ret_num_visited

    raise NotImplementedError("To be implemented")
    
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
