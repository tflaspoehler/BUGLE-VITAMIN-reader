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
values = np.array(book.nuclides[4725].xs[0][0][:n])
print len(energy), len(values)
print energy
print values

def get_ticks(mini,maxi):
    if mini == 0:
        mini = 1
    print mini, maxi
    mini = 10**floor(log10(mini))
    maxi = 10**ceil(log10(maxi))
    print "MIN/MAX",'%.6E'%mini, '%.6E'%maxi
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

for i in range(0, n):
    ax.step(energy, values[i], lw=2, label="data set "+repr(i), color=repr((0.5*float((i+1)/n))), where='pre', linewidth=1)
if (n>1):
    ax.legend(loc='lower left')
xlabel = ax.set_xlabel('energy ($eV$)')
ax.set_ylabel('cross section ($cm^{-1}$)')
try:
    print sys.argv[2]
    log = False
except:
    log = True
if log:
    ax.loglog()
min, max = ax.yaxis.get_data_interval()
min = np.min( values )
print min
ticks = get_ticks( min, max )
##ax.set_yticks(ticks, minor=True)
min, max = ax.xaxis.get_data_interval()
ticks = get_ticks( min, max )
##ax.set_xticks(ticks, minor=True)
##ax.xaxis.set_ticks(np.exp(np.logspace(start, end, 4)))
fig.set_size_inches(2*4.36,2*2.23)
plt.savefig('test.png',dpi=300, bbox_extra_artists=[xlabel], bbox_inches='tight')
plt.show()