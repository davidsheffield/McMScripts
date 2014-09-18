import sys
import pprint
import csv
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM

mcm = restful( dev=False ) # Get mcmc connection

# Check for CSV file
if len(sys.argv) != 2:
    print "usage: python clone.py csvfile.csv"
    sys.exit(1)

req = mcm.getA('requests','EXO-Fall13-00199') # Get request to clone

csvfile = open(sys.argv[1],'r') # Open CSV file

# Initialize lists
DataSetName=[] # Sample names
MCDBID=[]      # LHE file
CS=[]          # Cross section [pb]
Evts=[]        # Number of events
Cards=[]       # Fragment name
Time=[]        # Time per event [s]
Size=[]        # Size per event [kB]
Eff=[]         # Efficiency
Tag=[]         # Fragment tag
Gen=[]         # Generators

# Read CSV into lists
for row in csv.reader(csvfile):
    DataSetName.append(row[0])
    MCDBID.append(row[1])
    CS.append(row[2])
    Evts.append(row[3])
    #Cards.append("Configuration/GenProduction/python/EightTeV/"+row[4])
    Cards.append("Configuration/GenProduction/python/ThirteenTeV/"+row[4])
    Time.append(row[5])
    Size.append(row[6])
    #Size.append(1.0)
    #Eff.append(row[7])
    Eff.append(1.0)
    Tag.append(row[7])
    Gen.append(row[8])

num_to_clone = len(Cards)
list_of_modifications = [] # List of dictionaries for each clone request
for i in range(num_to_clone):
    req['dataset_name'] = DataSetName[i]
    req['mcdb_id'] = MCDBID[i]
    req['name_of_fragment'] = Cards[i]
    req['size_event'] = Size[i]
    req['time_event'] = Time[i]
    req['total_events'] = Evts[i]
    req['fragment_tag'] = Tag[i]
    req['generators'] = [Gen[i]]
    #req['generators'] = ["madgraph","pythia6"]
    
    list_of_modifications.append(req.copy()) # Append dictionary

# Clone requests
for i in range(num_to_clone):
    answer = mcm.clone('EXO-Fall13-00199',list_of_modifications[i]) # Clone
    if answer['results']:
        newid = answer['prepid'] # Get new PrepId
        a_clone = mcm.getA('requests',newid) # Get dictionary for new PrepId
        # Add generator parameters
        a_clone['generator_parameters'][0]['cross_section'] = float(CS[i])
        a_clone['generator_parameters'][0]['filter_efficiency'] = Eff[i]
        a_clone['generator_parameters'][0]['filter_efficiency_error'] = 0.0
        a_clone['generator_parameters'][0]['match_efficiency'] = 1.0
        a_clone['generator_parameters'][0]['match_efficiency_error'] = 0.0
        update_answer = mcm.updateA('requests',a_clone) # Update request with generator parameters
        if update_answer['results']:
            print newid, list_of_modifications[i]['dataset_name'] # Print new PrepId and sample name
        else:
            print newid, "cloned but not updated with generator parameters"
    else:
        print list_of_modifications[i]['dataset_name'], "not cloned"
