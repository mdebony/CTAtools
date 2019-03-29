"""Central place for config file handling"""
import sys
import logging
from os.path import join
from astropy.io import fits
from configobj import ConfigObj

def getConfig(infile):
    """Parse config file"""
    config = ConfigObj(infile, file_error=True)

    return config


def queryConfig():
    import os
    """Make a new config object, asking the user for required options"""
    config = ConfigObj(indent_type='\t')
    print('Please provide the following required options [default] :')
    config['out'] = os.getcwd()
    out = input('Output directory ['+config['out']+'] : ')
    if not(out=='') :
        config['out'] = out
        config['submit'] = 'False'
    config['analysisPipeline'] = 'ctools'

#    Informations about the source
    config['target'] = {}
    config['target']['name'] = input('Target Name : ')
    config['target']['ra'] = input('Right Ascension: ')
    config['target']['dec'] = input('Declination: ')

    config['target']['redshift'] = '0'
    redshift = input('redshift, no effect if null [0] : ')
    if not(redshift=='') :
        config['target']['redshift'] = redshift
        config['target']['ebl_model'] = input('ebl model to used\n'
                                                   '0=Kneiske, 1=Primack05, 2=Kneiske_HighUV, 3=Stecker05, '
                                                   '4=Franceschini, 5=Finke, 6=Gilmore : ')

#    informations about the input files
    config['file'] = {}
    config['file']['inobs'] = 'events.fits'
    config['file']['selectedevent'] = 'selectedevent.fits'
    config['file']['cntcube'] = 'cntcube.fits'
    config['file']['expcube'] = 'expcube.fits'
    config['file']['psfcube'] = 'psfcube.fits'
    config['file']['bkgcube'] = 'bkgcube.fits'
    config['file']['edispcube'] = 'edispcube.fits'
    config['file']['outmap'] = 'skymap.fits'
    config['file']['model'] = 'model.fits'
    config['file']['inmodel'] = 'model.xml'
    config['file']['tag'] = ''

#    information about the binning
    config['binning'] = {}
    config['binning']['usepnt'] = 'False'
    config['binning']['expr'] = ''
    config['binning']['ebins_per_dec'] = '8'
    config['binning']['enumbins'] = '60'
    config['binning']['ebinalg'] = 'LOG'
    config['binning']['eunit'] = 'TeV'
    config['binning']['binsz'] = '0.05'
    config['binning']['nxpix'] = '200'
    config['binning']['nypix'] = '200'

#    informations about the time
    config['time'] = {}
    tmin = input('Start time [-1=START] : ')
    if not(tmin=='') and float(tmin)>=0 :
        config['time']['tmin'] = tmin
    else :
        config['time']['tmin'] = '0'
    tmax = input('End time [-1=END] : ')
    if not(tmax=='') and float(tmax)>=0 :
        config['time']['tmax'] = tmax
    else :
        config['time']['tmax'] = '1e20'

#    informations about the energy
    config['energy'] = {}
    emin = input('Emin [0.2] : ')
    if not(emin=='') :
        config['energy']['emin'] = emin
    else :
        config['energy']['emin'] = '0.2'
    emax = input('Emax [300] : ')
    if not(emax=='') :
        config['energy']['emax'] = emax
    else :
        config['energy']['emax'] = '300'
    config['energy']['enumbins_per_decade'] = '5'

#   information about the analysis
    config['analysis']={}
    config['analysis']['likehood']='unbinned'
    config['analysis']['stat'] ='POISSON'
    config['analysis']['fix_spat_for_ts'] = 'False'
    config['analysis']['edisp'] = 'True'

#   information about the skymap
    config['SkyMap'] = {}
    config['SkyMap']['bkgsubtract'] = 'NONE'
    config['SkyMap']['roiradius'] = '0.1'
    config['SkyMap']['inradius'] = '0.6'
    config['SkyMap']['outradius'] = '0.8'
    config['SkyMap']['inexclusion'] = 'NONE'

#   information about the irfs
    config['irfs']={}
    config['irfs']['irf'] = 'South_0.5h'
    config['irfs']['caldb'] = 'prod2'

#   information about the space
    config['space']={}
    config['space']['rad'] = '15.'
    config['space']['xref'] = '0.'
    config['space']['yref'] = '0.'
    config['space']['coordsys'] = 'CEL'
    config['space']['proj'] = 'CAR'

    return getConfig(config)
