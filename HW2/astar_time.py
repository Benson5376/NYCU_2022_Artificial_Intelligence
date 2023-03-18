import csv
import heapq
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Store the imformation of every nodes. 
    # edges[node number] = [(reachable node #1, distance #1),(reachable node #2, distance #2)]
    edges = {}
    max_speed = 0
    with open(edgeFile, newline='') as csvfile:
        # read every edges then construct a graph
        rows = csv.DictReader(csvfile)
        for row in rows:
            s = int(row['start'])
            e = int(row['end'])
            d = float(row['distance'])
            t = d/(float(row['speed limit'])/3.6)
            if s in edges:
                edges[s] += [(e, d, t)]
            else:
                edges[s] = [(e, d, t)]
            if float(row['speed limit']) > max_speed:
                max_speed = float(row['speed limit'])
    # Construct a graph that represent the linear distance of each node to the destination.
    # heuristic[node number] = the linear distance to the destination.
    heuristic = {}
    with open(heuristicFile, newline='') as csvfile:
        # Read in the distance and construct a graph.
        rows = csv.DictReader(csvfile)
        for row in rows:
            heuristic[int(row['node'])] = float(row[str(end)])/(max_speed/3.6)
    # times[node number] =
    # (path's time with the starting point + linear distance with the destination / maximum speed m/s, the previous node )
    times = {}
    Q = []
    heapq.heappush(Q, (0+heuristic[start], start, None))
    while len(Q) > 0:
        cur_time, cur_node, prev_node = heapq.heappop(Q)
        # Exclude those have been visited, because we can't find a shorter path. 
        if cur_node in times:
            continue
        times[cur_node] = (cur_time, prev_node)
        # Find the path
        if cur_node == end:
            break
        if not cur_node in edges:
            continue
        # Expand from the cuurent node, and try the nodes that are connected to the current node.
        for nxt_node, d, t in edges[cur_node]:
        # Exclude those have been visited, because we won't find a shorter path. 
            if nxt_node in times:
                continue
            heapq.heappush(Q, (cur_time+t-heuristic[cur_node]+heuristic[nxt_node], nxt_node, cur_node))
    
    # Backtrace from the ending node
    ret_path = [end]
    while times[ret_path[-1]][1] != None:
        ret_path.append(times[ret_path[-1]][1])
    ret_time = times[end][0]
    ret_num_visited = len(times)
    return ret_path[::-1], ret_time, ret_num_visited



if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
