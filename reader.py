## =========================================       
##               cross sections
##        for individual compositions
## could be an isotope, element, mixture, etc.
##  also some isotopes/elements have different
##     sets weighted by different spectra
## for specific regions of shielding problems
##            such as 1/4T iron
class isotope:
    def __init__(self, lines):
        title = lines[0]
        self.id = int(title.split()[3])
        self.name = title.split()[5]
        self.n_groups = int(title.split()[0])
        self.n_responses = int(title.split()[1])
        self.xs = []
        self.add_legendre(lines)
        
    def add_legendre(self, lines):
        data = []
        for line in lines[1:]:
            values = line.split()[:-1]
            for v in range(0, len(values)):
                if 'r' in values[v]:
                    fido = values[v].split('r')
                    for null in range(0, int(fido[0])):
                        data.append(convert_ascii_number(''+fido[1]))
                else:
                    data.append(convert_ascii_number(values[v]))
        next = []
        for r in range(0, self.n_responses):
            next.append([response for response in data[:self.n_groups]])
            data[:self.n_groups] = []
        self.xs.append(next)
## =========================================    
        
## =========================================       
##        read in all cross sections
##            from a '.bcd' file
class multigroup_library:
    def __init__(self, file_name):
        lines = [line.replace('\r','').replace('\n','') for line in open(file_name, 'r').readlines()]
        start = 0
        self.nuclides = {}
        for l in range(1, len(lines)):
            if len(lines[l]) < 80:
                finish = l-1
                title = lines[start]
                if title.split() == ['7', '7', '7', '7']:
                    break
                nuclide = int(title.split()[3])
                if nuclide < 7000:
                    nuclide = int(title.split()[6])
                if nuclide not in self.nuclides:
                    self.nuclides[nuclide]    = isotope(lines[start:finish+1])
                else:
                    self.nuclides[nuclide].add_legendre(lines[start:finish+1])
                start = l
                break
    def get_mt(self, id, mts=[1]):
        if not isinstance(mts, list):
            mts = [mts]
        sigmas = []
        for mt in mts:
            sigmas.append(self.nuclides[id].xs[0][mt])
        if len(sigmas) == 1:
            return sigmas[0]
        else:
            return sigmas
            
        
## =========================================   

## =========================================   
def convert_ascii_number(value):
    sign = 1.0
    if value[0] == '-':
        sign = -1.0
        value = value[1:]
    if '-' in value:
        return sign*float(value.split('-')[0])*(10.0**(-1.0*float(value.split('-')[1])))
    elif '+' in value:
        return sign*float(value.split('+')[0])*(10.0**(1.0*float(value.split('+')[1])))
    else:
        return sign*float(value)
## ========================================= 


        
        


