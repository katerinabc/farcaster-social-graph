import pandas as pd
import networkx as nx

nodes = pd.read_json('nodes.json')
edges = pd.read_json('edges.json')
# some nodes aren't included in edges 
# some sender/receiver not included in nodes

G = nx.from_pandas_edgelist(edges, 'from', 'to')
nx.set_node_attributes(G, pd.Series(nodes.username, index = nodes.fid).to_dict(), 'username')


# I don't care about the graph. I want metrics

# Community metrics
dens = nx.density(G)
# sw = nx.sigma(G) #not feasible. takes too long. more than 1m with 500 nodes
# density

# Cluster membership
# ok, the smart local moving algorithm should be better but lib isn't working
# http://www.ludowaltman.nl/slm/

fccom = nx.community.louvain_communities(G)
# this returns a list with node ids. So list 1 is cluster 1
# the numbers are fids or node ids?
# I'm going to assume it is node ids
# wrong. I only have 500 nodes. so it must be fids

# can I turn the set into a dictionary where the index is the number of the set
# nx.set_node_attributes(G, fccom, 'cluster') does not work


# set node attribute  
# G.nodes[number] where number = index

for count, cluster in enumerate(fccom):
    tmp = [x for x in cluster]
    #create a dictionary of cluster id and fid
    nx.set_node_attributes(G, pd.Series(count, tmp).to_dict(), 'Tribe')


# individual metrics

# leadership/facilitator score
tmp = nx.centrality.betweenness_centrality(G)
nx.set_node_attributes(G, tmp, "Leadership score")

# Neighbourhood density
tmp = nx.clustering(G)
nx.set_node_attributes(G, tmp, 'Neighourhood density')