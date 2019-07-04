import ROOT

# Do for each width
dict_0p3 = {}
dict_0p6 = {}

for cut in ["03","06"] :

  infile = ROOT.TFile.Open("TLA_gaussians_y{0}.root".format(cut),"READ")
  tree_name = "Table 3" if "03" in cut else "Table 5"
  alist = infile.GetListOfKeys()
  akey = alist.FindObject(tree_name)
  dir = akey.ReadObj()
  res_width = dir.Get("Graph1D_y1")
  five_width = dir.Get("Graph1D_y2")
  seven_width = dir.Get("Graph1D_y3")
  ten_width = dir.Get("Graph1D_y4")

  for graph,width in zip([res_width,five_width,seven_width,ten_width],["res","0p05","0p07","0p10"]) :

    if "06" in cut and "0p10" in width : continue

    for index in range(graph.GetN()) :
      x = ROOT.Double(0)
      y = ROOT.Double(0)
      graph.GetPoint(index,x,y)

      usedict = dict_0p3 if x < 700.0 else dict_0p6

      if not x in usedict.keys() :
        usedict[x] = {}

      usedict[x][width] = y

for usedict,cut in zip([dict_0p3,dict_0p6],["03","06"]) :
  f = open("TLA_gaussians_y{0}.txt".format(cut),"w")
  f.write( str(usedict) )
  f.close()
