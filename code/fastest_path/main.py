import os
import time
import naive
import allsimplepathdist

#loader = loader.Loader()
#loader.create_graph(7.5256,54.4125,12.7881,57.6336) #aalborg
#loader.load_graph()
#G=loader.graph
#start = time.time()

#print len(G.nodes()), len(G.edges())
#P = nx.dijkstra_predecessor_and_distance(G,loader.street_node('Oxholmvej'), cutoff=None, weight='weight')

#shortpath = nx.shortest_path(G,loader.street_node('Oxholmvej'), loader.street_node('Naurve#j'), 'weight')
#cut = allsimplepathdist.path_time(G, shortpath)
#print cut
#p = allsimplepathdist.all_simple_paths(G,loader.street_node('Oxholmvej'), loader.street_node('Naurvej'), cutoff=cut)
#print P[0]
#print allsimplepathdist.path_time(G, p)
print time.time() - start
print 'end'


'''import networkx as nx
=======
#print time.time() - start
#print 'end'
import networkx as nx
>>>>>>> cc587eed162e0ad1271a5f16221bca920d147423
from loader import Loader
import vehicle
from rn_algorithms import fastest_path_greedy




def main():
    loader = Loader()
    loader.create_graph(9.95842,57.007187,10.002193,57.022981)
    loader.load_graph()
    road_network = loader.rn
    road_network.generate_charge(10, 20)
    G = nx.connected_components(road_network)
    for node in road_network.nodes():
        if node not in G[0]:
            road_network.remove_node(node)
                #print nx.shortest_path(road_network, road_network.nodes()[0], road_network.nodes()[-1])
    
    for e in road_network.edges():
        if e[0] == e[1]:
            road_network.remove_edge(e[0], e[1])

    print road_network.edges()
    print road_network.nodes()[0]
    print road_network.nodes()[-1]
    for e in road_network.edges([1394577375L], data=True):
        print e
    
    fastest_path_greedy(road_network,road_network.nodes()[0], road_network.nodes()[-1], 0)
#road_network.visualize_roadnetwork()
    
    #===========================================================================
    # print len(G.nodes()), len(G.edges())
    # p = shortest_path_through_all(G,loader.street_node('Selma LagerlÃ¸fs Vej'), loader.street_node('Niels Bohrs Vej'))
    # for x in xrange(1,10):
    #     print p[x]
    # print len(p)
    #===========================================================================
    
main()

     
def shortest_path_through_all(G,s,t):
        shortest_paths = []
        for node in G.nodes():
            if node != s and node != t:
                try:
                    p = nx.shortest_path(G,s,node) + nx.shortest_path(G,node,t)
                    shortest_paths.append(p)
                except:
                    pass
        return shortest_paths

def fastest_path(G):
	pass
 
def timecalculator(edges=[]):
	pass
 
 
def BFS(G, s):
    loader = loader.Loader()
    loader.create_graph(9.972153,57.007566,10.005369,57.020594) ##aalborg øst
    loader.load_graph()
    G=loader.graph
    return nx.bfs_tree(G, s)
 
loader = Loader()
loader.create_graph(9.972153,57.007566,10.005369,57.020594) ##aalborg øst
loader.load_graph()
G=loader.graph
s = loader.street_node('Selma Lagerløfs Vej')
print BFS(G, s)
 
def CR(v):
	return v*v+v 

main()
'''
