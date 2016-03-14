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
import sys
import math
import time
sys.path.append('../')
import mcmscripts_config


def display_number(n):
    if n == 0:
        return "0"
    else:
        prefix = ['', 'k', 'M']
        n = float(n)
        prefix_id = max(0, min(2, int(math.floor(math.log10(abs(n))/3.0))))
        return "{0:.5g}{1}".format(n/10**(3*prefix_id), prefix[prefix_id]);


def makeAnalyzerHTML():
    fout = open('{0}analyzer.html'.format(mcmscripts_config.html_location), 'w')
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
    campaign_classes = ["lhe", "gs", "dr", "miniaod", "miniaodv2"]

    fout.write("""\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
    <title>Exotica MC Status for Analyzers</title>

    <link rel="stylesheet" type="text/css" href="global.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">

    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
</head>

<body>

<div class="wrapper">
<h1>Exotica MC</h1>

<h2 class="campaign">7_6_X Campaign</h2>
<p>(RunIIWinter15wmLHE/RunIIWinter15pLHE &rarr;) RunIISummer15GS &rarr; RunIIFall15DR &rarr; RunIIFall15MiniAODv1 &rarr; RunIIFall15MiniAODv2</p>
<table>
<tr class="table_header">
    <th class="process">Process</th>
    <th class="requester">Requester</th>
    <th class="lhe">LHE</th>
    <th class="gs">GS</th>
    <th class="dr">DR</th>
    <th class="miniaod">MiniAODv1</th>
    <th class="miniaodv2">MiniAODv2</th>
</tr>
""")

    conn = sqlite3.connect(mcmscripts_config.database_location)

    c = conn.cursor()
    c.execute('SELECT Process, Tag, RequestMultiplicity, LHE_Done, GS_Done, DR_Done, MiniAOD_Done, MiniAODv2_Done, RequesterID FROM RequestSets;')
    out = c.fetchall()

    for request in out:
        c.execute('SELECT Name, Email FROM Requesters WHERE RequesterID = {0};'.format(
                request[8]))
        requester = c.fetchall()
        fout.write("""\
<tr>
    <td class="process">{0}</td>
    <td class="requester"><a href="mailto:{1}">{2}</a></td>
""".format(request[0], requester[0][1], requester[0][0]))
        for i in range(len(status_name)):
            fout.write("    <td class=\"{0}\"><a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={1}&member_of_campaign={2}&page=-1\" class=\"status\">{3}/{4} done</a></td>\n".format(
                    campaign_classes[i], request[1], campaigns[i], request[3 + i], request[2]))
        fout.write("</tr>\n")
    conn.close()

    fout.write("""\
</table>
<p class="update-time">Updated {0}</p>
</div>

</body>
</html>
""".format(time.asctime()))
    fout.close()

    print "Generated analyzer page"

    return


def makeContactHTML():
    fout = open('{0}contact.html'.format(mcmscripts_config.html_location), 'w')
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
    campaign_classes = ["lhe", "gs", "dr", "miniaod", "miniaodv2"]

    fout.write("""\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
    <title>Exotica MC Status for Contacts</title>

    <link rel="stylesheet" type="text/css" href="global.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">

    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
</head>

<body>

<div class="wrapper">
<h1>Exotica MC</h1>

<h2 class="campaign">7_6_X Campaign</h2>
<p>(RunIIWinter15wmLHE/RunIIWinter15pLHE &rarr;) RunIISummer15GS &rarr; RunIIFall15DR &rarr; RunIIFall15MiniAODv1 &rarr; RunIIFall15MiniAODv2</p>
<table style="margin:1em;border:1px black solid;"><tbody><tr style="background-color:#ffffff"><td>Key:</td><td class="gs" style="width:3em">1<br>2<br>3<br>4<br>5<br>6<br>7/28</td><td class="gs">new<br>validating<br>validated<br>defined<br>approved<br>submitted<br>done/total</td></tr></tbody></table>
<table>
<tr class="table_header">
    <th class="process">Process</th>
    <th class="tag">Tag</th>
    <th class="requester">Requester</th>
    <th class="contact">Contact</th>
    <th class="events">Events</th>
    <th class="lhe">LHE</th>
    <th class="gs">GS</th>
    <th class="dr">DR</th>
    <th class="miniaod">MiniAODv1</th>
    <th class="miniaodv2">MiniAODv2</th>
    <th class="spreadsheet">Spreadsheet</th>
    <th class="notes">Notes</th>
</tr>
""")

    conn = sqlite3.connect(mcmscripts_config.database_location)

    c = conn.cursor()
    c.execute("""SELECT Process, RequesterID, ContactID, Tag, Events, Notes, Spreadsheet, RequestMultiplicity,
                 LHE_New, LHE_Validating, LHE_Validated, LHE_Defined, LHE_Approved, LHE_Submitted, LHE_Done,
                 GS_New, GS_Validating, GS_Validated, GS_Defined, GS_Approved, GS_Submitted, GS_Done,
                 DR_New, DR_Validating, DR_Validated, DR_Defined, DR_Approved, DR_Submitted, DR_Done,
                 MiniAOD_New, MiniAOD_Validating, MiniAOD_Validated, MiniAOD_Defined, MiniAOD_Approved, MiniAOD_Submitted, MiniAOD_Done,
                 MiniAODv2_New, MiniAODv2_Validating, MiniAODv2_Validated, MiniAODv2_Defined, MiniAODv2_Approved, MiniAODv2_Submitted, MiniAODv2_Done
                 FROM RequestSets;""")
    out = c.fetchall()

    for request in out:
        c.execute('SELECT Name, Email FROM Requesters WHERE RequesterID = {0};'.format(
                request[1]))
        requester = c.fetchall()
        c.execute('SELECT DisplayName, Email FROM Contacts WHERE ContactID = {0};'.format(
                request[2]))
        contact = c.fetchall()
        fout.write("""\
<tr>
    <td class="process">{0}</td>
    <td class="tag">{1}</td>
    <td class="requester"><a href="mailto:{2}">{3}</a></td>
    <td class="contact">{4}</td>
    <td class="events">{5}</td>
""".format(request[0], request[3], requester[0][1], requester[0][0], contact[0][0],
           display_number(request[4])))
        for i in range(len(status_name)):
            fout.write("    <td class=\"{0}\"><a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={1}&member_of_campaign={2}&page=-1\" class=\"status\">{3}<br>{4}<br>{5}<br>{6}<br>{7}<br>{8}<br>{9}/{10}</a></td>\n".format(
                    campaign_classes[i], request[3], campaigns[i],
                    request[8 + i*7], request[9 + i*7], request[10 + i*7],
                    request[11 + i*7], request[12 + i*7], request[13 + i*7],
                    request[14 + i*7], request[7]))
        if request[6] == "":
            fout.write("    <td class=\"spreadsheet empty\">&nbsp;</td>\n")
        else:
            fout.write("    <td class=\"spreadsheet\"><a href=\"{0}\">X</a></td>".format(
                    request[6]))
        fout.write("""\
    <td class="notes">{0}</td>
</tr>\n""".format(request[5]))
    conn.close()

    fout.write("""\
</table>
<p class="update-time">Updated {0}</p>
</div>

</body>
</html>
""".format(time.asctime()))
    fout.close()

    print "Generated contact page"

    return


def main():
    makeAnalyzerHTML()
    makeContactHTML()

    return


if __name__ == '__main__':
    main()
