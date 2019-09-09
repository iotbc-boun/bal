#!/usr/bin/python
import random
from mininet.net import Mininet
from mininet.node import OVSBridge, CPULimitedHost
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

import math
#make a class this module
def graph_to_str(adj_matrix):
    str_matrix = []
    v = int(math.sqrt(len(adj_matrix)))
    for i in range (1, v):
        for j in range(i+1, v+1):
            index = ( i - 1 ) * v + j - 1
            if adj_matrix[ index ]:
                str_matrix.append(str(i) + " " + str(j) + " " + str(adj_matrix[index]))
    return str_matrix

# Return a random integer between 0 and k-1 inclusive.
def ran( k ):
    return random.randint(0, k-1)

def random_connected_graph(v, e, w):
    adj_matrix = [0] * v * v
    tree = [0] * v
    init_array(tree, v)

    tree = permute(tree)

    for i in range(1, v):
        j = ran( i )
        adj_matrix[ tree[ i ] * v + tree[ j ] ] = ran(w) + 1
        adj_matrix[ tree[ j ] * v + tree[ i ] ] = ran(w) + 1

    count = v - 1
    while count < e:
        i = ran( v )
        j = ran( v )

        if i == j:
            continue

        if i > j :
            i, j = j, i

        index = i * v + j
        if not adj_matrix[ index ]:
            adj_matrix[ index ] = ran(w) + 1
            count += 1

    return adj_matrix

def permute(arr):
    return random_permutation(arr)

def random_permutation(iterable, r=None):
    "Random selection from itertools.permutations(iterable, r)"
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(random.sample(pool, r))

def init_array(arr, end):
   for i in range(0, end):
      arr[i] = i

def mininet_topo(switch_matrix, host_number, net_params):
    switch_number = int(math.sqrt(len(switch_matrix)))
    net = Mininet(**net_params)
    switches = [None] * switch_number
    for i in range(1, switch_number+1):
        switches[i-1] = net.addSwitch('s' + str(i), failMode = 'standalone', stp=1)

    for i in range(1, host_number+1):
        ran_bw = ran(max_bw)+1
        cpu_f = (ran_bw*1.0 / max_bw)
        host = net.addHost('h'+ str(i), defaultRoute=None, cpu=cpu_f)
        selected_sw = random.choice(switches)
        net.addLink(selected_sw, host, bw=ran_bw)

    for i in range (1, switch_number):
        for j in range(i+1, switch_number+1):
            index = ( i - 1 ) * switch_number + j - 1
            if switch_matrix[ index ]:
                net.addLink(switches[i-1], switches[j-1], bw=switch_matrix[index])
    return net

if __name__ == '__main__':
    setLogLevel( 'info' )
    switch_number = int(input("Number of switches:"))
    host_number = int(input("Number of hosts:"))
    edge_number = switch_number * 2

    max_bw = int(input("Maximum Bandwidth:"))
    print("switch=%d hosts=%d MaxBW=%d\n" % (switch_number, host_number, max_bw))
    net_params = {'switch': OVSBridge, 'link': TCLink, 'host': CPULimitedHost,
                    'ipBase': '10.0.0.0/8', 'waitConnected' : True}
    switch_matrix = random_connected_graph(switch_number, edge_number, max_bw)
    net = mininet_topo(switch_matrix, host_number, net_params)
    net.build()
    net.start()
    CLI( net )
    net.stop()
