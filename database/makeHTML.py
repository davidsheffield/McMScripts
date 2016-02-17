#!/usr/bin/env python

################################
#
# check.py
#
#  Script to check status of requests and save in database
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sqlite3
import argparse
#from __future__ import print_function


def makeAnalyzerHTML():
    fout = open('analyzer.html', 'w')
    status_name = [["LHE_New", "LHE_Validating", "LHE_Validated", "LHE_Defined",
                    "LHE_Approved", "LHE_Submitted", "LHE_Done"],
                   ["GS_New", "GS_Validating", "GS_Validated", "GS_Defined",
                    "GS_Approved", "GS_Submitted", "GS_Done"],
                   ["DR_New", "DR_Validating", "DR_Validated", "DR_Defined",
                    "DR_Approved", "DR_Submitted", "DR_Done"],
                   ["MiniAOD_New", "MiniAOD_Validating", "MiniAOD_Validated",
                    "MiniAOD_Defined", "MiniAOD_Approved", "MiniAOD_Submitted",
                    "MiniAOD_Done"],
                   ["MiniAODv2_New", "MiniAODv2_Validating",
                    "MiniAODv2_Validated", "MiniAODv2_Defined",
                    "MiniAODv2_Approved", "MiniAODv2_Submitted",
                    "MiniAODv2_Done"]]
    campaigns = ["RunIIWinter15*LHE", "RunIISummer15GS", "RunIIFall15DR76",
                 "RunIIFall15MiniAODv1", "RunIIFall15MiniAODv2"]

    fout.write("""\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
    <title>Exotica MC Status for Analyzers</title>

    <link rel="stylesheet" type="text/css" href="global.css">

    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
</head>

<body>

<table>
<tr class="table_header">
    <th>Process</th>
    <th>LHE</th>
    <th>GS</th>
    <th>DR</th>
    <th>MiniAOD</th>
    <th>MiniAODv2</th>
</tr>
""")

    conn = sqlite3.connect('EXO_MC_Requests.db')
    c = conn.cursor()
    c.execute('SELECT * FROM RequestSets;')
    out = c.fetchall()

    print "Filling:"
    for request in out:
        print request[4]
        fout.write("""\
<tr>
    <td>{0}</td>
""".format(request[1]))
        for i in range(len(status_name)):
            fout.write("    <td><a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={0}&member_of_campaign={1}&page=-1&shown=137438955551\">".format(
                    request[4], campaigns[i]))
            for j in range(len(status_name[0])):
                fout.write("{0} ".format(request[10 + j + 7*i]))
            fout.write("</a></td>\n")
        fout.write("</tr>\n")
    conn.close()

    fout.write("""\
</table>
</body>
</html>
""")
    fout.close()

    return

def main():
    makeAnalyzerHTML()

    return


if __name__ == '__main__':
    main()
