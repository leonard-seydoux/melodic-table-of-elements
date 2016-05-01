import matplotlib.pyplot as plt
import numpy as np
import csv 

fig = plt.figure()
fig.set_size_inches(1, 1)
ax = plt.axes()

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

circlex = np.cos(np.linspace(0, 2*np.pi, 200))
circley = np.sin(np.linspace(0, 2*np.pi, 200))

path = 'atom-icons/'

with open('periodic-table.csv') as ptable:
    ptable = csv.DictReader(ptable, delimiter=',')
    for e in ptable:
        if len(e['Electron Configuration']) != 0:
            
            # if "[" not in e['Electron Configuration'][0]:

            #     n_orb = int(e['Electron Configuration'][0])
            #     n_ele = int(e['Electron Configuration'][-1])
            #     elx = 0.5*np.cos(np.linspace(0, 2*np.pi, n_ele, endpoint=False))
            #     ely = 0.5*np.sin(np.linspace(0, 2*np.pi, n_ele, endpoint=False))
            #     ax.plot(0, 0, 'w.', markersize=15)
            #     ax.plot(circlex, circley, lw=0.3, color='#0bb8ee', dashes=[1, 1])
            #     ax.plot(elx, ely, '.', markersize=4, color='#0bb8ee')
            #     ax.set_axis_off()
            #     plt.savefig(path+e['Symbol'], dpi=300, transparent=True)

            if "[He]" in e['Electron Configuration']:
                
                print e['Electron Configuration'].split(' ')
                n_orb = 4
                n_ele = 4
                
                ax.plot(0, 0, 'w.', markersize=15)
                for n in xrange(n_orb):
                    n_ele = int(2*np.random.rand())
                    print n_ele
                    r = 0.8*float(n+1)/n_orb
                    elx = r*np.cos(2*np.pi*np.random.rand(n_ele))
                    ely = r*np.sin(2*np.pi*np.random.rand(n_ele))
                    ax.plot(r*circlex, r*circley, lw=0.3, color='#0bb8ee', dashes=[1, 1])
                    ax.plot(elx, ely, '.', markersize=4, color='#0bb8ee')
                ax.set_axis_off()
                plt.savefig(path+'H', dpi=300, transparent=True)

