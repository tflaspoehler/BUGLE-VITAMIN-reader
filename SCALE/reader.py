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
        print lines[0]
        title = lines[0][1:]
        self.id = int(title.split()[-1])
        self.name = ' '.join(title.split()[5:])
        self.n_groups = int(title.split()[0])
        self.n_neutrons = 200
        self.n_gammas = self.n_groups - self.n_neutrons
        self.n_responses = int(title.split()[1])
        self.xs = []
        if self.id < 7000:
            self.read_data(lines)
        else:
            self.read_data(lines)
        
    def read_data(self, lines):
        data = []
        for line in lines[1:]:
            values = line[:75].split()
            for v in range(0, len(values)):
                if 'r' in values[v]:
                    fido = values[v].split('r')
                    for null in range(0, int(fido[0])):
                        data.append(convert_ascii_number(''+fido[1]))
                elif 'z' in values[v]:
                    for i in range(0, int(values[v].split('z')[0])):
                        data.append(0.0)
                else:
                    data.append(convert_ascii_number(values[v]))
            if line == line[1]:
                print " ".join(["%+.4e" % d for d in data[:self.n_responses]])
            ## raw_input()
        ## if self.id < 7000:
        print len(data), self.n_groups*self.n_responses, len(data) - self.n_groups*self.n_responses
        print self.n_groups, self.n_responses, float(len(data)) / float(self.n_groups)
        if True:
            siga = []
            nsgf = []
            sigt = []
            sigs = []
            if len(self.xs) < 1:
                f = open('test.dat', 'w')
            for g in range(0, self.n_groups):
                if len(self.xs) < 1:
                    f.write(" ".join(["%+.4e" % d for d in data[0:self.n_responses]])+'\n')
                # print data[0]
                siga.append(data[4])
                nsgf.append(data[2])
                sigt.append(data[6])
                data[:6] = []
                sigs.append([response for response in data[:self.n_responses-6]])
                data[:self.n_responses-6] = []
            self.xs.append([siga, nsgf, sigt, sigs])
            self.siga = siga
            self.nusigf = nsgf
            self.sigt = sigt
            self.sigs = sigs
            sigst = []
            self.position = self.n_responses - 8 - self.n_groups + 1
            print 'postion', self.position
            for s in sigs:
                sigst.append(s[self.position])
            for s in range(0, self.n_neutrons):
                for g in range(s+1, self.n_neutrons):
                    sigst[s] += sigs[g][self.position+g-s]
            for s in range(self.position, self.n_neutrons):
                for g in range(0, self.position):
                    sigst[s] += sigs[s-g-1][self.position-g-1]
            self.sigst = sigst
            if len(self.xs) < 1:
                f.close()
        ##elif self.id < 8000:
        ##    responses = []
        ##    for r in range(0, self.n_responses):
        ##        responses.append(data[:self.n_groups])
        ##        data[:self.n_groups] = []
        ##    self.xs.append(responses)
        ##        
        ##else:
        ##    responses = []
        ##    for r in range(0, self.n_responses):
        ##        responses.append(data[:self.n_groups])
        ##        data[:self.n_groups] = []
        ##    self.xs.append(responses)
            
## =========================================    
        
## =========================================       
##        read in all cross sections
##            from a '.bcd' file
class multigroup_library:
    def __init__(self, file_name):
        lines = [line.replace('\r','').replace('\n','') for line in open(file_name, 'r').readlines()]
        comments = [i for i in range(0, len(lines)) if "'" in lines[i]][:-1:2]
        for comment in comments[::-1]:
            lines[comment] = lines[comment][1:] + ' ' + lines[comment+1][1:]
            lines.pop(comment+1)
            if 'ampx' in lines[comment+1]:
                lines[comment] = lines[comment][1:] + ' ' + lines[comment+1][1:]
                lines.pop(comment+1)
                
        start = 0
        self.nuclides = {}
        for l in range(1, len(lines)):
            if (len(lines[l]) < 80) or ('endf' in lines[l]) or ('p' in lines[l]):
                finish = l-1
                title = lines[start]
                if title.split() == ['7', '7', '7', '7']:
                    break
                nuclide = int(title.split()[-1])
                ## if nuclide < 7000 and 'mixed' not in title:
                ##     nuclide = int(title.split()[6])
                if nuclide not in self.nuclides:
                    print '=================================='
                    print 'adding nuclide', nuclide
                    self.nuclides[nuclide]    = isotope(lines[start:finish+1])
                else:
                    print '----------------------------------'
                    print 'next order', nuclide
                    self.nuclides[nuclide].read_data(lines[start:finish+1])
                start = l
                
                
    def get_mt(self, id, mts=[1], legendre=0):
        if not isinstance(mts, list):
            mts = [mts]
        sigmas = []
        for mt in mts:
            sigmas.append(self.nuclides[id].xs[legendre][mt])
        if len(sigmas) == 1:
            return sigmas
        else:
            return sigmas
            
    def sigt(self, id):
        return self.nuclides[id].sigst
            
        
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


        
        


