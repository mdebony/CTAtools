import os,numpy
import Script.Common_Functions as CF
from ctoolsAnalysis.config import get_config,get_default_config

data = numpy.genfromtxt("AGN_Monitoring_list.dat",dtype=str,unpack=True)

for i in xrange(len(data[0])):
    srcname = data[0][i]+data[1][i]
    cwd = os.getcwd()+"/"+srcname
    os.system("mkdir -p "+cwd)
    ra = data[2][i]
    dec = data[3][i]
    z = data[4][i]
    print srcname," ",ra," ",dec, " ", z
    
    config = get_config('Template.conf')
    config = CF.MakeconfigFromFile(cwd,srcname,ra,dec,'Template.conf')

    config['out'] = cwd
    config['file']['inobs'] = cwd+"/outobs_"+srcname+".xml"
    config['file']['selectedevent'] = cwd+"/outobs_"+srcname+"_selected.xml"
    config['file']['inmodel'] = cwd+"/"+srcname+".xml"
    config["file"]["tag"] = srcname+"_DC1"
    config["file"]["outmap"] = cwd+"/"+srcname+"_DC1_skymap.fits"
    
    config["space"]["xref"] = ra
    config["space"]["yref"] = dec
    config["space"]["rad"] = 3

    config["irfs"]["irf"] = "South_z20_50h"
    config["irfs"]["caldb"] = "1dc"
    
    config["SkyMap"]["nxpix"] = 500
    config["SkyMap"]["nypix"] = 500
    config["SkyMap"]["binsz"] = 0.02
    
    config["simulation"]["pivot_sim"] = 2000
    config["simulation"]["prefactor_sim"] = 1.465
    config["simulation"]["prefactor_max_sim"] = 1.665
    config["simulation"]["prefactor_min_sim"] = 1.275
    config["simulation"]["prefactor_scale_sim"] = 1e-10
    config["simulation"]["index_value_sim"] = -2.184
    config["simulation"]["index_min_sim"] = -2.3334
    config["simulation"]["index_maz_sim"] = -2.0346
    config["simulation"]["emin_sim"] = 0.03 #TeV
    config["simulation"]["emax_sim"] = 8    #TeV


    from ebltable.tau_from_model import OptDepth as OD
    tau = OD.readmodel(model = 'franceschini')
    # array with energies in TeV
    ETeV = numpy.logspace(-1,1,50)
    Tau_franceschini = tau.opt_depth(z,ETeV)

    Etau = numpy.interp([1.],Tau_franceschini,ETeV)
    Etau_max = numpy.interp([3.],Tau_franceschini,ETeV)
    #config['energy']['emin'] = Etau[0] #energy corresponding to tau=1
    config['energy']['emin'] = 0.05
    config['energy']['emax'] = 50.0
    #config['energy']['emax'] = Etau_max[0] #energy corresponding to tau=3
    

    config.write(open(cwd+"/"+srcname+"_DC1.conf", 'w'))
