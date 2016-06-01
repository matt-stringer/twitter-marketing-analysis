#!/usr/bin/env python
"""
An example using networkx.Graph().

miles_graph() returns an undirected graph over the 128 US cities from
the datafile miles_dat.txt. The cities each have location and population
data.  The edges are labeled with the distance betwen the two cities.

This example is described in Section 1.1 in Knuth's book [1,2].

References.
-----------

[1] Donald E. Knuth,
    "The Stanford GraphBase: A Platform for Combinatorial Computing",
    ACM Press, New York, 1993.
[2] http://www-cs-faculty.stanford.edu/~knuth/sgb.html
"""


__author__ = """Aric Hagberg (hagberg@lanl.gov)"""


import networkx as nx
from collections import defaultdict

d = defaultdict(list)
installers_studied = ['SolarCity', 'Sunrun', 'Verengo', 'Real Goods Solar']

partner_colors = {'hardware store':'g',
                    'solar installer': '#EEAD51',
                    'Car company': '#8CC43D',
                    'utility':'#2B292A',
                    'Financing': '#FED700',
                    'home improvement': '#426986',
                    'car manufacturer': '#8B8878',
                    'Government': '#426986',
                    'energy efficiency': '#FED700',
                    'Non profit': '#b03060',
                    'Home builder': '#A5BDD7',
                    'tech company': '#F1F0AD',
                    'Sidwell': '#996699',
                    '':'b',
                    'manage referrals':'#CCCCCC',
                    'manufacturer':'#CCFFFF',
                    'solar manufacturer':'b'}


def miles_graph():
    """ Return the cites example graph in miles_dat.txt
        from the Stanford GraphBase.
    """
    # open file miles_dat.txt.gz (or miles_dat.txt)
    f = open('SolarPartnerships.csv', 'r')
    accounts = f.readlines()

    f.close()


    G=nx.Graph()
    G.position={}
    G.population={}
    G.color={}

    cities=[]
    for row in accounts:
        row = row.split(',')


        if row[0] in installers_studied:

            arrangement = row[1]
            partner = row[2]
            partner_company_type = row[3]
            installer = row[0]
            date_started = row[4]
            d[installer].append((partner, partner_company_type))

    for installer in d:
        G.color[installer] = 'r'
        for (partner, partner_type) in d[installer]:

            G.add_edge(installer, partner)
            G.color[partner] = partner_colors[partner_type]
            G.color['Real Goods Solar'] = 'r'



        # else: # this line is a city, position, population
        #     i=1
        #     (city,coordpop)=line.split("[")
        #     cities.insert(0,city)
        #     (coord,pop)=coordpop.split("]")
        #     (y,x)=coord.split(",")
        
        #     G.add_node(city)
        #     # assign position - flip x axis for matplotlib, shift origin
        #     G.position[city]=(-int(x)+7500,int(y)-3000)
        #     G.population[city]=float(pop)/1000.0

    return G            

if __name__ == '__main__':
    import networkx as nx
    import re
    import sys

    G=miles_graph()


    print("Loaded miles_dat.txt containing 128 cities.")
    print("digraph has %d nodes with %d edges"\
          %(nx.number_of_nodes(G),nx.number_of_edges(G)))
    H=nx.Graph()


    print len(G.nodes())
    print len(G.color)

    for v in G:

        H.add_node(v)
    for (u,v,s) in G.edges(data=True):
        H.add_edge(u,v)
      
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(15,10))
        nx.draw(H, node_color=G.color.values())



# partner_colors = {'hardware store':'#7C8FB0',
#                     'solar installer': '#EEAD51',
#                     'Car company': '#8CC43D',
#                     'utility':'#2B292A',
#                     'Financier': '#FED700',
#                     'home improvement': '#426986',
#                     'car manufacturer': '#8B8878',
#                     'Government': '#426986',
#                     'energy efficiency': '#FED700',

#                     'Non profit': '#b03060',
#                     'Home builder': '#A5BDD7',
#                     'tech company': '#F1F0AD',
#                     'Sidwell': '#996699',
#                     '':'b',
#                     'manage referrals':'#CCCCCC',
#                     'manufacturer':'#CCFFFF',
#                     'solar manufacturer':'b'}

        line_width = 8
        l1 = plt.Line2D([], [], linewidth=line_width, color='#7C8FB0')
        l2 = plt.Line2D([], [], linewidth=line_width, color='#EEAD51')
        l3 = plt.Line2D([], [], linewidth=line_width, color='#8CC43D')
        l4 = plt.Line2D([], [], linewidth=line_width, color='#8B8878')
        l4a = plt.Line2D([], [], linewidth=line_width, color='#FED700')
        l6 = plt.Line2D([], [], linewidth=line_width, color='#FED700') 
        l7 = plt.Line2D([], [], linewidth=line_width, color='#b03060')
        l8 = plt.Line2D([], [], linewidth=line_width, color='#A5BDD7')
        l9 = plt.Line2D([], [], linewidth=line_width, color='#F1F0AD')
        l10 = plt.Line2D([], [], linewidth=line_width, color='#CCFFFF')
        plt.legend([l1, l2, l3, l4, l4a, l6, l7, l8, l9, l10], ['Hardware Store', 'Solar Installer', 'Car Company', 'Utility', 'Financing', 'Energy Efficiency', 'Non Profit',  'Home builder', 'Tech Company', 'Referral Management','solar manufacturer'], loc="lower left")    

        plt.show()
        plt.savefig("network.png")


    except:
        pass



