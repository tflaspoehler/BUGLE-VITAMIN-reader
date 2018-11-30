import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np
from math import *
from reader import *

try:
    file_name = os.path.join( os.getcwd(), sys.argv[1] )
except:
    file_name = 'Bugle7T.bcd'
    
book = multigroup_library(file_name)
energy = np.array([float(b.replace('\n','').replace('\r','')) for b in open('neutron_groups.dat').readlines()])
n = len(energy) - 1

## 1137 u235, 2065 fe56, 2001 h1 (h20) downcomer, 95 c, 249 eu153
iso = 249
values = book.get_mt(iso, [0, 2])
values.append(book.sigt(iso))
titles = ['siga','sigt','sigs']

isos = [1137, 2065, 2001, 249, 95]
values = []
titles = []
for i in isos:
    values += book.get_mt(i, [2])
    titles.append(book.nuclides[i].name)


h = open('h1.dat', 'w')
for g in range(0, len(book.nuclides[iso].xs[0][0])):
    xs = book.nuclides[iso].xs[0]
    h.write(' '.join(['%.4E' % xs[0][g], '%.4E' % xs[1][g], '%.4E' % xs[2][g]] + ['%.4E' % x for x in xs[3][g]]) + '\n')
h.close()

for i in range(0, len(values)):
    values[i] = values[i][:n] + [values[i][n-1]]
    values[i] = np.array(values[i])  
    
def get_ticks(mini,maxi):
    if mini == 0:
        mini = 1
    mini = 10**floor(log10(mini))
    maxi = 10**ceil(log10(maxi))
    a = [ np.linspace(mini,mini*10,10)[:-1] ]
    while a[-1][0]*10 < maxi:
        a.append(a[-1]*10)
    a = np.array(a)
    return np.append(a, a[-1][0]*10).flatten()

# plot it!
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 9}
plt.rc('font', family='serif')
fig = plt.figure(facecolor="white")
ax = fig.add_subplot(111)
ax.grid(which='both', linestyle="-", color="0.95")
ax.set_axisbelow(True)

for i in range(0, len(values)):
    ax.step(energy, values[i], lw=2, label=titles[i], color='C'+repr(i), where='pre', linewidth=1)
if (n>1):
    ax.legend(loc='lower left')
xlabel = ax.set_xlabel('energy ($eV$)')
ax.set_ylabel('cross section ($cm^{-1}$)')

ax.loglog()
    

min, max = ax.yaxis.get_data_interval()
min = np.min( values )
ticks = get_ticks( min, max )
ax.set_yticks(ticks, minor=True)
plt.yticks([])

min, max = ax.xaxis.get_data_interval()
ticks = get_ticks( min, max )
ax.set_xticks(ticks, minor=True)
plt.xticks([])

fig.set_size_inches(2*4.36,2*2.23)
plt.savefig('test.png',dpi=300, bbox_extra_artists=[xlabel], bbox_inches='tight')
plt.show()