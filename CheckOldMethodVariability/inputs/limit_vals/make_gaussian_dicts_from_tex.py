import ROOT

outdict = {}

# Unit conversion if need be
# High mass dijet limits need to be scaled down.
scaleBy = 1/1000.

def hasNumbers(inputString):
  return any(char.isdigit() for char in inputString)

dijet_widths = ["res","0p03","0p05","0p07","0p10","0p15"]

with open('HighMassDijet_gaussians_preformat.txt', 'r') as f:
  lines = f.readlines()
  for line in lines :

    tokens = line.split()
    if len(tokens) < 1 : continue

    index = -1
    mass = 0    
    for token in tokens :
      if not hasNumbers(token) and not "-" in token :
        continue
      index = index+1

      # If no solution, continue now. But wanted to increment number.
      if "-" in token :
        continue

      token = token.replace("[","").replace("'","").replace('"','')
      number = eval(token)

      # It's the mass
      if index == 0 :
        mass = number        
        if not number in outdict.keys() :
          outdict[number] = {}

      # It's a width
      else :
        width = dijet_widths[index-1]
        outdict[mass][width] = number*scaleBy

f = open("HighMassDijet_gaussians.txt","w")
f.write( str(outdict) )
f.close() 
