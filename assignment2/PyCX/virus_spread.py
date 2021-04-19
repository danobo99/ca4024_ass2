import pycxsimulator
from pylab import *

import copy as cp

nr = 1000. # carrying capacity of healthys
nf = 500 # carrying capacity of infected
nimm = 500 #carrying capacity of immune

r_init = 800 # initial healthy population
mr = 0.05 # magnitude of movement of healthys
dr = 0.75 # infection rate of healthys when they collide with infected
rr = 0.1 # reproduction rate of healthys- irrelevant


f_init = 15 # initial infected population
mf = 0.05 # magnitude of movement of infected
df = 0.1 # death rate of infected(turn to immune)
rf = 0.2 # reproduction rate of infected


imm_init = 1 # initial immune population
mimm = 0.05 # magnitude of movement of immune
dimm = 0.05 # death rate of immune - back to infected again


cd = 0.02 # radius for infection detection
cdsq = cd ** 2

class agent:
    pass

def initialize():
    global agents, rdata, fdata, immdata
    agents = []
    rdata = []
    fdata = []
    immdata = []

    #the position of each agent is a random x and y between 0 and 1
    #range(initial number of healthy and infected people)
    #max number of agents is sum of initials, appending ag to agents list
    for i in range(r_init + f_init + imm_init):
        ag = agent()
        ag.type = 'r' if i < r_init else 'f' if i < r_init+ f_init else 'imm'
        ag.x = random()
        ag.y = random()
        agents.append(ag)


#healthys is the list of healthy agents, same with infected
#subplot(nrows, ncolumns, index). The subplot will take the index position on a grid with nrows rows and ncols columns.
#plot b. means blue dots, r.= red dots


def observe():
    global agents, rdata, fdata, immdata

    subplot(2, 1, 1)
    cla()
    healthys = [ag for ag in agents if ag.type == 'r']
    if len(healthys) > 0:
        x = [ag.x for ag in healthys]
        y = [ag.y for ag in healthys]
        plot(x, y, 'b.')
    infected = [ag for ag in agents if ag.type == 'f']
    if len(infected) > 0:
        x = [ag.x for ag in infected]
        y = [ag.y for ag in infected]
        plot(x, y, 'r.')
    immune = [ag for ag in agents if ag.type == 'imm']
    if len(immune) > 0:
        x = [ag.x for ag in immune]
        y = [ag.y for ag in immune]
        plot(x, y, 'g.')
    axis('image')
    axis([0, 1, 0, 1])
    #axis([xmin, xmax, ymin, ymax])
    subplot(2, 1, 2)
    cla()
    plot(rdata, label = 'healthy')
    #plot healthy total- rdata= sum of healthy, fdata= sum of infected
    plot(fdata, label = 'infected')
    plot(immdata, label = 'immune')
    legend()

def update_one_agent():
    global agents
    if agents == []:
        return

    #random.choice(list) = returns a random agent from agents
    ag = choice(agents)

    #uniform(-m, m) gives a random float between the two numbers
    # simulating random movement
    #mr = magnitude of movement of healthy
    #mf = magnitude of movement of infected
    #x and y values moving at a random displacement in either direction at a max of m
    # if the x or y tries to leave the edge of the grid it stays at the edge
    m = mr if ag.type == 'r' else mf if ag.type == 'f' else mimm
    ag.x += uniform(-m, m)
    ag.y += uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # detecting collision and simulating death or birth
    #second part is just calculating euclidean distance between the agent and its neighbour
    #neighbours is a list of all other agents within collision distance which aren't agents type
    neighbors = [nb for nb in agents if nb.type != ag.type
                 and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]

#need to change this- currently removes the healthy person if an infected is within the collision dist
#dr = deathrate of healthys when they meet infected- agents only die if there are infected nearby
#don't think death rate is needed
    if ag.type == 'r':
        if len(neighbors) > 0: # if there are infected nearby
            if random() < dr:
                agents.remove(ag)
                #agnew = agent()
                #agnew.type = 'f'
                #agents.append(agnew)
                near_inf = [n for n in neighbors if n.type == 'f']
                if len(near_inf) > 0:
                    agents.append(cp.copy(near_inf[0])) 
                #ag.type == 'f'
                else:
                    return
        # if random float(0,1) is less than (reproduction rate of healthys X 1 - sum of healthy/ max capacity of healthys
        # if healthy aren't at capacity then let them reproduce at current rate      
        #if random() < rr*(1-sum([1 for x in agents if x.type == 'r'])/nr): 
            #agents.append(cp.copy(ag))
            #then add another rabbit as they reproduced
    elif ag.type == 'f':
        if random() < df:
            agents.remove(ag)
            #agnew = agent()
            #agnew.type = 'f'
            #agents.append(agnew)
            immns = [n for n in agents if n.type == 'imm']
            if len(immns) > 0:
                agents.append(cp.copy(immns[0])) 
            #ag.type == 'f'
            else:
                    return

    else:
        if len(neighbors) > 0:
            if random() < dimm:
                #likelihood of immune becoming infected again    
                agents.remove(ag)
                #agnew = agent()
                #agnew.type = 'f'
                #agents.append(agnew)
                near_inf = [n for n in neighbors if n.type == 'f']
                if len(near_inf) > 0:
                    agents.append(cp.copy(near_inf[0])) 
                else:
                    return            

def update():
    global agents, rdata, fdata, immdata
    t = 0.
    while t < 1. and len(agents) > 0:
        t += 1. / len(agents)
        update_one_agent()
    #while time goes on and there are agents still in the grid, update
    rdata.append(sum([1 for x in agents if x.type == 'r']))
    fdata.append(sum([1 for x in agents if x.type == 'f']))
    immdata.append(sum([1 for x in agents if x.type == 'imm']))
    #update the amount of healthy and infected
pycxsimulator.GUI().start(func=[initialize, observe, update])
