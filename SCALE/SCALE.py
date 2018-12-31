from reader import *
from xs_plot import *

try:
    file_name = os.path.join( os.getcwd(), sys.argv[1] )
except:
    file_name = 'u235.pun'

print 'opening file', file_name
book = multigroup_library(file_name)
energy = [float(b.replace('\n','').replace('\r','')) for b in open('neutron_groups.dat').readlines()]

## ========================================= 
##     this section shows how to plot 
## individual reactions from a single isotope
##   for example ... 
## 1137 u235, 2065 fe56, 2001 h1 (h20) downcomer, 95 c, 249 eu153
iso = 1001
values = book.get_mt(iso, [0])
iso = 3006
values.append(book.get_mt(iso, [0])[0])
iso = 2065
values.append(book.get_mt(iso, [0])[0])
iso = 92235
values.append(book.get_mt(iso, [0])[0])

new = []
for value in values:
    new.append([])
    for v in value:
        new[-1].append(abs(v))
values = new        
titles = ['h-1 (n, total)', 'li-6 (n, total)', 'fe-56 (n, total)', 'u-235 (n, total)']
## ========================================= 
##            actualy plot it 
xs_plot(energy, values, titles)
## ========================================= 