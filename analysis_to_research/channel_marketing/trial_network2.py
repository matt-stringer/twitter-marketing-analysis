import networkx as nx

from collections import defaultdict




def miles_graph():
    """ Return the cites example graph in miles_dat.txt
        from the Stanford GraphBase.
    """
    # open file miles_dat.txt.gz (or miles_dat.txt)

    f = open('SolarPartnerships.csv', 'r')
    fh = f.readlines()
    f.close()


    # G=nx.Graph()
    # G.position={}
    # G.population={}



    d = defaultdict(list)
    installers_studied = ['SolarCity', 'Sunrun', 'Verengo', 'Real Goods Solar', 'Sungevity']

    cities=[]
    for row in fh:
        print row

        row = row.split(',')
        arrangement = row[1]
        partner = row[2]
        partner_company_type = row[3]
        installer = row[0]
        date_started = row[4]

        if installer in installers_studied:
            d[installer].append(partner)




    #     line = line.decode()
    #     if line.startswith("*"): # skip comments
    #         continue


    #     numfind=re.compile("^\d+") 

    #     if numfind.match(line): # this line is distances
    #         dist=line.split()
    #         for d in dist:

    #             G.add_edge(city,cities[i],weight=int(d))
    #             i=i+1
    #     else: # this line is a city, position, population
    #         i=1
    #         (city,coordpop)=line.split("[")
    #         cities.insert(0,city)
    #         (coord,pop)=coordpop.split("]")
    #         (y,x)=coord.split(",")
        
    #         G.add_node(city)
    #         # assign position - flip x axis for matplotlib, shift origin
    #         G.position[city]=(-int(x)+7500,int(y)-3000)
    #         G.population[city]=float(pop)/1000.0
    # return G            

if __name__ == '__main__':
    import networkx as nx
    import re
    import sys

    # G=miles_graph()

    # print("Loaded miles_dat.txt containing 128 cities.")
    # print("digraph has %d nodes with %d edges"\
    #       %(nx.number_of_nodes(G),nx.number_of_edges(G)))


    # # make new graph of cites, edge if less then 300 miles between them
    # H=nx.Graph()
    # for v in G:
    #     H.add_node(v)
    # for (u,v,d) in G.edges(data=True):
    #     if d['weight'] < 300:
    #         H.add_edge(u,v)

    # # draw with matplotlib/pylab            

    # try:
    #     import matplotlib.pyplot as plt
    #     plt.figure(figsize=(8,8))
    #     # with nodes colored by degree sized by population
    #     node_color=[float(H.degree(v)) for v in H]
    #     print len(node_color)
    #     print len(G.population)
    #     nx.draw(H,G.position,
    #          node_size=[G.population[v] for v in H],
    #          node_color=node_color,
    #          with_labels=False)

    #     # scale the axes equally
    #     plt.xlim(-5000,500)
    #     plt.ylim(-2000,3500)

    #     plt.show()
    #     # plt.savefig("knuth_miles.png")
    # except:
    #     pass


