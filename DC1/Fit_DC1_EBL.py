# ------ Imports --------------- #
from ebltable.tau_from_model import OptDepth as OD
import os,sys
from os.path import join
import ctools
from ctoolsAnalysis.config import get_config,get_default_config
from ctoolsAnalysis.LikeFit import CTA_ctools_analyser
from Script.Common_Functions import *
import  ctoolsAnalysis.xml_generator as xml
# ------------------------------ #
try:
    get_ipython().magic(u'pylab')
except :
    pass


try:  #conf file provided
    config = get_config(sys.argv[-1])
except :
    print "usage : python "+sys.argv[0]+" config_file"
    exit()

#------ Source Id
data = numpy.genfromtxt("AGN_Monitoring_list.dat",dtype=str,unpack=True)
for i in xrange(len(data[0])):
    srcname = data[0][i]+data[1][i]
    if srcname == config["target"]["name"]:
        redshift = data[-1][i]

srcname = config["target"]["name"]
ra = config["target"]["ra"]
dec = config["target"]["dec"]
        
#------------------ Value of the EBL normalisation and redshift
Alpha = numpy.arange(.1,1.5001,.1)
ETeV = numpy.logspace(-2,2.5,200)
tau = OD.readmodel(model = 'dominguez')
Tau_values = tau.opt_depth(redshift,ETeV)


#----------------- make the first DC1 selection 
import csobsselect
selection = csobsselect.csobsselect()
selection["inobs"] = "$CTADATA/obs/obs_agn_baseline.xml"
selection["outobs"] = config["file"]["inobs"]

selection["pntselect"] = "CIRCLE"
selection["coordsys"] = "CEL"
selection["ra"] = ra
selection["dec"] = dec
selection["rad"] = 3.0
selection.execute()
print selection

#------------------- Select the files
Analyse = CTA_ctools_analyser.fromConfig(config)
Analyse.ctselect(log = True)

loglike_res = open(srcname+"_AlphaScan_DC1.txt","w")

for ii in xrange(len(Alpha)):
    filename = "tau_"+str(redshift)+"_"+str(Alpha[ii])+".txt"
    filefun = open(filename,"w")
    for j in xrange(len(ETeV)):
        filefun.write(str(ETeV[j]*1e6)+" "+str(max(1e-10,numpy.exp(-Alpha[ii] * Tau_values)[j]))+"\n")
    #------------------ Make the XML model
    #SOURCE SPECTRUM
    lib,doc = xml.CreateLib()
    spec = xml.MultiplicativeModel(lib,srcname,filename)
    spatial = xml.AddPointLike(doc,ra,dec)
    spec.appendChild(spatial)
    lib.appendChild(spec)

    #CTA BACKGROUND
    bkg = xml.addCTAIrfBackground(lib)
    lib.appendChild(bkg)

    open(srcname+'.xml', 'w').write(doc.toprettyxml('  '))

    #------------------- fit the data
    Analyse.create_fit(log = True,debug = False)
    Analyse.fit()
#    Analyse.PrintResults()
    print "LogLike value for Alpha = ",Alpha[ii]," ",Analyse.like.opt().value()
    loglike_res.write(str(Alpha[ii])+" "+str(Analyse.like.opt().value())+"\n")
    
loglike_res.close()

