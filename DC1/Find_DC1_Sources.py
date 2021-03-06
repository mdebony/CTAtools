
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


#------------------ Make the XML model
lib,doc = xml.CreateLib()


srcname = config["target"]["name"]
#SOURCE SPECTRUM
spec = xml.addPowerLaw1(lib,srcname,"PointSource",flux_value=1e-14,flux_max=1000.0, flux_min=1e-5)
ra = config["target"]["ra"]
dec = config["target"]["dec"]
spatial = xml.AddPointLike(doc,ra,dec)
spec.appendChild(spatial)
lib.appendChild(spec)


#CTA BACKGROUND
bkg = xml.addCTAIrfBackground(lib)
lib.appendChild(bkg)

#----------------- make the first DC1 selection 
from ctoolsAnalysis.cscriptClass import CTA_ctools_script 
Script = CTA_ctools_script.fromConfig(config)
Script.csobsselect(obsXml = "$CTADATA/obs/obs_agn_baseline.xml", log = True,debug = False)


#------------------- Select the files
Analyse = CTA_ctools_analyser.fromConfig(config)
Analyse.ctselect(log = True)

#------------------- make a skymap
Analyse.ctskymap(log = True)

#-------------------detect new sources
Script.cssrcdetect(10, log = True,debug = False)

