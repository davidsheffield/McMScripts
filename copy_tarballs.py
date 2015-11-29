import os,sys
from subprocess import Popen, PIPE

exit_anyway_after_check = False
# exit_anyway_after_check = True

inputs_dir ='/afs/cern.ch/work/p/perrozzi/private/git/Hbb/McMScripts/gridpacks/'
  
# target_main = '/afs/cern.ch/user/p/perrozzi/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/'
target_main = '/afs/cern.ch/user/p/perrozzi/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.3.2.2/'

print 'target main folder',target_main
if not os.path.isdir('/afs/cern.ch/user/p/perrozzi/eos/cms/store/group/phys_generator/cvmfs/gridpacks/'):
  print 'mount eos first!'
  sys.exit(1)
else:
  print 'eos mounted'

version = "v1"
print 'version',version

print 'input dir',inputs_dir
inputs = filter(None,os.popen('ls '+inputs_dir).read().split('\n'))

existing_list = []
existing_list2 = []
trow_exception = False

for input in inputs:
  foldername = input.replace('_tarball','').replace('.tar.gz','').replace('.tar.xz','')
  fullpath = target_main+"/"+foldername
  fullpath_version = fullpath+"/"+version
  print "checking version folder",version,"for",foldername,", check if it is empty"
  if os.path.isdir(fullpath_version) and (len(os.listdir(fullpath_version))!=0):
    print "file already inside",fullpath_version,"please change version"
    existing_list.append(((fullpath_version+"/"+os.listdir(fullpath_version)[0]).replace('/afs/cern.ch/user/p/perrozzi/eos/cms','')).replace('//','/'))
    trow_exception = True

if(trow_exception):
  print 'same files already existed, please check'
  print existing_list
  sys.exit(1)

if exit_anyway_after_check: sys.exit(1)
  
for input in inputs:
  foldername = input.replace('_tarball','').replace('.tar.gz','').replace('.tar.xz','')
  fullpath = target_main+"/"+foldername
  fullpath_version = fullpath+"/"+version+"/"
  print 'foldername',foldername.replace('/afs/cern.ch/user/p/perrozzi/eos/cms','')
  print 'os.path.isdir('+fullpath.replace('/afs/cern.ch/user/p/perrozzi/eos/cms','')+')',os.path.isdir(fullpath)
  if not os.path.isdir(fullpath):
    os.makedirs(fullpath)
  print 'os.path.isdir('+fullpath_version.replace('/afs/cern.ch/user/p/perrozzi/eos/cms','')+')',os.path.isdir(fullpath_version)
  if not os.path.isdir(fullpath_version):
    os.makedirs(fullpath_version)
  
  print("cp "+inputs_dir+"/"+input+" "+fullpath_version.replace('/afs/cern.ch/user/p/perrozzi/eos/cms','')+'/')
  os.system("cp "+inputs_dir+"/"+input+" "+fullpath_version+'/')
  existing_list2.append(((fullpath_version+'/'+os.listdir(fullpath_version)[0]).replace('/afs/cern.ch/user/p/perrozzi/eos/cms/store/group/phys_generator/cvmfs','/cvmfs/cms.cern.ch/phys_generator')).replace('//','/'))

print 'list of copied files'
print existing_list2

