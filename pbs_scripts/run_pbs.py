import subprocess

import numpy as np

TEMPLATE_SERIAL = """
#!/scratch/bogdanm/miniconda3/envs/py37/bin/python
#PBS -l walltime=48:00:00
#PBS -l select=1:ncpus=28
#PBS -j oe
#PBS -N {name}
#PBS -o {logfile_path}
#PBS -m ae
#PBS -M {email}
{code}
"""

import os as _os, sys as _sys
GIPSY_WRAP_PATH="/scratch/bogdanm/gipsyx/GipsyX_Wrapper"
if GIPSY_WRAP_PATH not in _sys.path:
    _sys.path.insert(0,GIPSY_WRAP_PATH)
import trees_options


def qsub_python_code(code,name,email='bogdan.metviichuk@utas.edu.au',cleanup=False,pbs_base = '/scratch/bogdanm/pbs'):
    '''name should have number in it'''
    if not _os.path.exists(pbs_base):
        _os.makedirs(pbs_base)
    logfile_path = '{}/{}.log'.format(pbs_base,name)
    pbs_script_path = '{}/{}.qsub'.format(pbs_base,name)
    with open(pbs_script_path,'w') as pbs_script:
        pbs_script.write(TEMPLATE_SERIAL.format(name=name, logfile_path = logfile_path, email=email, code=code))

    # try:
    #     subprocess.call('qsub',pbs_script_path,shell=True)
    # finally:
    #     if cleanup:
    #         os.remove(pbs_script_path)

TEMPLATE_MGNSS = '''import os as _os, sys as _sys
GIPSY_WRAP_PATH="/scratch/bogdanm/gipsyx/GipsyX_Wrapper"
if GIPSY_WRAP_PATH not in _sys.path:
    _sys.path.insert(0,GIPSY_WRAP_PATH)

from mGNSS_class import mGNSS_class; import trees_options


kinematic_project = mGNSS_class(project_name = '{project_name}',
                                tmp_dir = '{tmp_dir}',
                                rnx_dir = '{rnx_dir}',
                                stations_list = {stations_list},
                                years_list = {years_list},
                                tree_options = {tree_options},
                                num_cores = {num_cores},
                                blq_file = '{blq_file}',
                                VMF1_dir = '{VMF1_dir}',
                                tropNom_input = '{tropNom_input}',
                                IGS_logs_dir = '{IGS_logs_dir}',
                                IONEX_products = '{IONEX_products}',
                                rate = {rate},
                                gnss_products_dir = '{gnss_products_dir}',
                                ionex_type = '{ionex_type}',
                                eterna_path = '{eterna_path}',
                                hardisp_path = '{hardisp_path}',
                                pos_s = {pos_s},
                                wetz_s = {wetz_s},
                                PPPtype = '{PPPtype}',
                                tqdm = {tqdm})
kinematic_project.{command}'''
                            
stations_list= ['ANAU', 'AUCK', 'BLUF', 'CHTI', 'CORM', 'DNVK', 'DUND', 'DUNT', 'FRTN',
                'GISB', 'GLDB', 'HAAS', 'HAMT', 'HAST', 'HIKB', 'HOKI', 'KAIK', 'KTIA',
                'LEXA', 'LEYL', 'LKTA', 'MAHO', 'MAKO', 'MAVL', 'METH', 'MKNO', 'MNHR',
                'MQZG', 'MTJO', 'NLSN', 'NPLY', 'NRSW', 'OROA', 'PKNO', 'RAHI', 'RAKW',
                'RAUM', 'RGHL', 'RGKW', 'RGMT', 'SCTB', 'TAUP', 'TAUW', 'TGRI', 'TRNG',
                'TRWH', 'VGMT', 'WAIM', 'WANG', 'WARK', 'WEST', 'WGTN', 'WHKT', 'WHNG',
                'WITH']

years_list=[2014,2015,2016,2017,2018];num_cores = 28

def gen_code(   stations_list,
                years_list,
                num_cores,
                command,
                project_name = 'nz_cod_ce',
                tmp_dir='/scratch/bogdanm/tmp_GipsyX/nz_tmpX/',
                rnx_dir='/scratch/bogdanm/GNSS_data/geonet_nz',
                tree_options = 'trees_options.rw_otl',
                blq_file = '/scratch/bogdanm/Products/otl/ocnld_coeff/FES2004_GBe.blq',
                VMF1_dir = '/scratch/bogdanm/Products/VMF1_Products',
                tropNom_input = 'trop',
                IGS_logs_dir = '/scratch/bogdanm/GNSS_data/station_log_files/',
                IONEX_products = '/scratch/bogdanm/Products/IONEX_Products',
                rate = 300,
                gnss_products_dir = '/scratch/bogdanm/Products/IGS_GNSS_Products/init/cod/', #we should use esa unreprocessed products
                ionex_type='igs', #No ionex dir required as ionex merged products will be put into tmp directory by ionex class
                eterna_path='/scratch/bogdanm/Products/otl/eterna',
                hardisp_path = '/scratch/bogdanm/Products/otl/hardisp/hardisp',
                pos_s = 3.2, wetz_s=0.1,PPPtype='kinematic',tqdm=False):
    return TEMPLATE_MGNSS.format(project_name = project_name,tmp_dir=tmp_dir,rnx_dir=rnx_dir,stations_list=stations_list,years_list=years_list,tree_options = tree_options,num_cores=num_cores,
                            blq_file = blq_file,VMF1_dir = VMF1_dir,tropNom_input = tropNom_input,IGS_logs_dir = IGS_logs_dir,IONEX_products = IONEX_products,rate = rate,
                            gnss_products_dir = gnss_products_dir,ionex_type=ionex_type,eterna_path=eterna_path,hardisp_path = hardisp_path,pos_s = pos_s, wetz_s=wetz_s,PPPtype=PPPtype,tqdm=tqdm,command=command)



stations_list_arrays = np.array_split(stations_list,10)
for i in range(len(stations_list_arrays)):
    code = gen_code(stations_list_arrays[i],years_list,num_cores,command='drMerge()')
    qsub_python_code(code,name='nz_cod_ce{}'.format(str(i)) ,email='bogdan.metviichuk@utas.edu.au',cleanup=False,pbs_base = '/scratch/bogdanm/pbs')