from reader import *
from xs_plot import *

try:
    file_name = os.path.join( os.getcwd(), sys.argv[1] )
except:
    file_name = 'Bugle7T.bcd'
    
book = multigroup_library(file_name)
energy = [float(b.replace('\n','').replace('\r','')) for b in open('neutron_groups.dat').readlines()]

## ========================================= 
##     this section shows how to plot 
## individual reactions from a single isotope
##   for example ... 
## 1137 u235, 2065 fe56, 2001 h1 (h20) downcomer, 95 c, 249 eu153
iso = 2001
values = book.get_mt(iso, [0, 2])
values.append(book.sigt(iso))
titles = ['siga','sigt','sigs']
## ========================================= 
##            actualy plot it 
xs_plot(energy, values, titles)
## ========================================= 

## ========================================= 
##     this section shows how to plot 
## the same reactino from multiple compositions
isos = [1137, 2065, 2001, 249, 95]
values = []
titles = []
for i in isos:
    values += book.get_mt(i, [2])
    titles.append(book.nuclides[i].name)
## ========================================= 
##            actualy plot it 
xs_plot(energy, values, titles)
## ========================================= 

## ========================================= 
##   demo of how to write a xs file for SN
h = open('last.dat', 'w')
for g in range(0, len(book.nuclides[iso].xs[0][0])):
    xs = book.nuclides[iso].xs[0]
    h.write(' '.join(['%.4E' % xs[0][g], '%.4E' % xs[1][g], '%.4E' % xs[2][g]] + ['%.4E' % x for x in xs[3][g]]) + '\n')
h.close()
## ========================================= 


