#!/scratch/bogdanm/miniconda3/envs/py37/bin/python
#PBS -l walltime=1:00:00
#PBS -l select=1:ncpus=28
#PBS -j oe
#PBS -o /scratch/bogdanm/output.txt
#PBS -m ae
#PBS -M bogdan.matviichuk@utas.edu.au
#PBS -N GipsyX_synth

import os as _os, sys as _sys

GIPSY_WRAP_PATH="/scratch/bogdanm/gipsyx/GipsyX_Wrapper"
if GIPSY_WRAP_PATH not in _sys.path:
    _sys.path.insert(0,GIPSY_WRAP_PATH)


'''Kunanyi'''
from mGNSS_class import mGNSS_class
import trees_options
stations_list=['CAMO'];years_list=[2010,2011,2012,2013];num_cores = 28


kinematic_project = mGNSS_class(project_name = 'penna',
                                stations_list=stations_list,
                                years_list=years_list,
                                tree_options = trees_options.rw_otl, 
                                num_cores=num_cores,
                                blq_file = '/scratch/bogdanm/Products/otl/ocnld_coeff/bigf_complete.blq',
                                rnx_dir='/scratch/bogdanm/GNSS_data/BIGF_data/daily30s',
                                tmp_dir='/scratch/bogdanm/tmp_GipsyX/bigf_tmpX/',
                                VMF1_dir = '/scratch/bogdanm/Products/VMF1_Products',
                                tropNom_input = 'trop+penna',
                                IGS_logs_dir = '/scratch/bogdanm/GNSS_data/station_log_files/',
                                IONEX_products = '/scratch/bogdanm/Products/IONEX_Products',
                                rate = 300,
                                gnss_products_dir = '/scratch/bogdanm/Products/IGS_GNSS_Products/init/es2_30h_init/',
                                ionex_type='igs', #No ionex dir required as ionex merged products will be put into tmp directory by ionex class
                                eterna_path='/scratch/bogdanm/Products/otl/eterna',
                                hardisp_path = '/scratch/bogdanm/Products/otl/hardisp/hardisp',
                                pos_s = 0.57, wetz_s=0.1,PPPtype='kinematic')
kinematic_project.gd2e()
