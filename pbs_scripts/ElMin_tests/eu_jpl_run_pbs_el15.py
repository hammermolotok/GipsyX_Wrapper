import subprocess
import sys as _sys, os as _os

import numpy as _np

GIPSY_WRAP_PATH="/scratch/bogdanm/gipsyx/GipsyX_Wrapper"
if GIPSY_WRAP_PATH not in _sys.path:
    _sys.path.insert(0,GIPSY_WRAP_PATH)

import trees_options
from gxlib.gx_aux import _project_name_construct, gen_staDb, prepare_dir_struct_dr, prepare_dir_struct_gathers
from gxlib.gx_pbs import gen_code, qsub_python_code
from gxlib.gx_trees import gen_trees

#parameters to change-----------------------------------------------------------------------------------------------

project_name = 'eu_jpl_cm'
ionex_type='jpl' #igs ionex map igsg2260.15i is missing data
gnss_products_dir = '/scratch/bogdanm/Products/JPL_GPS_Products_IGb08/source/Final' #we should use COD MGEX, ESA and GFZ later


'''Execution part here''' 
stations_list= ['LERI','PADT', 'PMTH', 'PRAE', 'APPL', 'EXMO',
                'TAUT', 'PBIL', 'POOL','SANO','CHIO','CARI', 'SWAS',
                'ANLX','HERT','LOFT','WEAR','CAMO','BRAE','BRST','ZIM2']
#'SCTB' station removed as it is in Anatarctica and almost no OTL
years_list=[2010,2011,2012,2013];num_cores = 28
num_nodes = 10
if num_nodes > len(stations_list): num_nodes = len(stations_list) #in case staions num is less than num_nodes => num_nodes = stations num
#-------------------------------------------------------------------------------------------------------------------

#We need to generate unique staDb with all the stations
tmp_dir='/scratch/bogdanm/tmp_GipsyX/bigf_tmpX/'
rnx_dir='/scratch/bogdanm/GNSS_data/BIGF_data/daily30s'
cddis=False
IGS_logs_dir = '/scratch/bogdanm/GNSS_data/station_log_files/bigf_igs_logs'
hatanaka=True
tree_options = trees_options.rw_otl
blq_file = '/scratch/bogdanm/Products/otl/ocnld_coeff/FES2004_GBe.blq'
ElMin = 15
pos_s = 3.2
wetz_s=0.1
PPPtype='kinematic'
VMF1_dir = '/scratch/bogdanm/Products/VMF1_Products'
static_clk = False
ambres = False
cache_path = '/dev/shm'#'/scratch/bogdanm/cache' 
tropNom_input = 'trop'
IONEX_products = '/scratch/bogdanm/Products/IONEX_Products'
rate = 300
eterna_path='/scratch/bogdanm/Products/otl/eterna'
hardisp_path = '/scratch/bogdanm/Products/otl/hardisp/hardisp'
tree_options_code = 'trees_options.rw_otl'
tqdm=False
ElDepWeight = 'SqrtSin'

pbs_base = _os.path.join('/scratch/bogdanm/pbs',project_name) #break down by project folders as gets slow on hpc with multiple files
prepare_dir_struct_dr(begin_year=_np.min(years_list), end_year = _np.max(years_list),tmp_dir=tmp_dir) #prepare dir struct for dr files
project_name_construct = _project_name_construct(project_name=project_name,PPPtype=PPPtype,pos_s=pos_s,wetz_s=wetz_s,tropNom_input=tropNom_input,ElMin=ElMin,ambres=ambres)
prepare_dir_struct_gathers(tmp_dir=tmp_dir,project_name=project_name_construct)

#generating tree files that won't be overwritten as crc32 will be the same
gen_trees(  ionex_type=ionex_type,tmp_dir=tmp_dir,tree_options=tree_options,blq_file=blq_file,mode = 'GPS+GLONASS',ElDepWeight=ElDepWeight,
            ElMin = ElMin,pos_s = pos_s,wetz_s = wetz_s,PPPtype = PPPtype,years_list=years_list,cache_path = cache_path,
            VMF1_dir = VMF1_dir,project_name = project_name_construct,static_clk = static_clk,ambres = ambres)#the GNSS_class single project name

staDb_path = gen_staDb(tmp_dir = tmp_dir, project_name = project_name, stations_list = stations_list, IGS_logs_dir = IGS_logs_dir)
stations_list_arrays = _np.array_split(stations_list,num_nodes)
for i in range(len(stations_list_arrays)):
    code = gen_code(stations_list = list(stations_list_arrays[i]), cache_path = cache_path,tropNom_input=tropNom_input, ambres = ambres,ElMin=ElMin,ElDepWeight=ElDepWeight,
                    staDb_path = staDb_path,years_list=years_list,num_cores=num_cores,tmp_dir=tmp_dir,project_name=project_name,IGS_logs_dir=IGS_logs_dir,blq_file=blq_file,
                    VMF1_dir = VMF1_dir,pos_s = pos_s,wetz_s = wetz_s,PPPtype = PPPtype,ionex_type=ionex_type,IONEX_products = IONEX_products,rate = rate,cddis=cddis,
                    gnss_products_dir = gnss_products_dir,eterna_path=eterna_path,hardisp_path = hardisp_path,rnx_dir=rnx_dir,hatanaka=hatanaka,tree_options = tree_options_code,tqdm=False,
                    command='gps.gd2e();kinematic_project.gps.envs(dump=True)')
    qsub_python_code(code,name='{}{}{}{}'.format(project_name,str(i),'AR' if ambres else '',ElMin if ElMin!=7 else ''),email='bogdan.matviichuk@utas.edu.au',cleanup=False,pbs_base = pbs_base,walltime='06:00:00')
