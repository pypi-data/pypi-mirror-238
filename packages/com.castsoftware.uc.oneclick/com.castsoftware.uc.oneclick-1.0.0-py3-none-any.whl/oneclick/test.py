from cast_common.util import run_process,track_process,check_process,format_table,create_folder
from os import listdir,remove,rename
from os.path import exists,abspath
from time import sleep
from cast_common.logger import Logger,INFO
from json import load
from pandas import json_normalize,ExcelWriter
from cast_common.util import format_table


log = Logger("test",level=INFO)


profiler_path=r'E:\work\CAST-Profiler\CAST-Profiler.exe'
project = 'test'
app_name = 'ZIP-test'
profiler_output=f'D:\CAST\CODE\REPORT\{project}\{app_name}'
work_folder=f'D:\CAST\CODE\STAGED\AIP\{project}\{app_name}\Operator Rounds'
args = [profiler_path,
        work_folder,
        '--generate-report', profiler_output,
        '--name',app_name,
        '--output',profiler_output,
        '--offline','--details','--no-upload','--no-browser','--complete-insight'
    ]
log.info(' '.join(args))

files = [f for f in listdir(profiler_output) if f.startswith(app_name) and f.endswith('result.json')]
for f in files:
    remove (f'{profiler_output}/{f}')

# proc = run_process(args,wait=False)
# track_process(proc)

files = [f for f in listdir(profiler_output) if f.startswith(app_name) and f.endswith('result.json')]
new_name = abspath(f'{profiler_output}/{app_name}.json')
if len(files) > 0:
    old_name = abspath(f'{profiler_output}/{files[0]}')
    if exists(new_name):
        remove(new_name)
    rename(old_name,new_name)

with open(new_name) as f:
    prflr = load(f)

alerts = json_normalize(prflr['alerts'],max_level=1)
composition = json_normalize(prflr['composition'],max_level=1)
dependencies = json_normalize(prflr['dependencies'])
frameworks = json_normalize(prflr['frameworks'])
ext_list = json_normalize(prflr['extensions_list'],max_level=1).transpose()
ext_list.reset_index(inplace=True)
ext_list = ext_list.rename(columns={'index':'Name',0:'Count'})
files = json_normalize(prflr['files'],max_level=1)	

file_name = f'{profiler_output}/Profiler-rslts.xlsx'
print (file_name)
writer = ExcelWriter(file_name, engine='xlsxwriter')
if not composition.empty: format_table(writer,composition,'composition',total_line=True)
if not dependencies.empty: format_table(writer,dependencies,'dependencies',total_line=True)
if not ext_list.empty: format_table(writer,ext_list,'ext_list',total_line=True)
if not files.empty: format_table(writer,files,'files',total_line=True)
if not frameworks.empty: format_table(writer,files,'frameworks',total_line=True)
if not alerts.empty: format_table(writer,alerts,'alerts',total_line=True)
writer.close()
pass
