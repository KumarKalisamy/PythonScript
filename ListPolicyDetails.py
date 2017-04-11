#!/usr/bin/python
 
import re
import subprocess
import datetime
import time
import os
import json
from pprint import pprint


CredStatus = os.path.isfile(os.path.expanduser('~/.aws/credentials'))
if not (CredStatus):
	print "Credentail file is NOT there..." 
	exit(1)

def timecheck ():
        filemod = int(os.path.getmtime(os.path.expanduser("~/.aws/credentials")))
        now = int(time.time())

        modtime = int(now - filemod)/60
        print "Credential file has been updated ", modtime, "minutes before." 

        if now - filemod > 3600:
                print "You need to update the Credentials file to run this script....."
	        exit (2)


timecheck ()




UDL="UserDetailList"
UN="UserName"
RDL="RoleDetailList"
RN="RoleName"
GDL="GroupDetailList"
GN="GroupName"
AMP="AttachedManagedPolicies"
PN="PolicyName"

def la (a, RDL, RN, AMP, PN):
        for i in range(0, len(a[RDL])):
                print "\n", RN,": ", a[RDL][i][RN] #, PrintPN(UDL, AMP, PN)
                dot = len(a[RDL][i][RN]) + 12
                print '*' * dot
                for j in range(0, len(a[RDL][i][AMP])):
                        print a[RDL][i][AMP][j][PN]

with open("/home/awsuser/.aws/credentials") as cred:
	for i in cred.readlines():
		if re.findall(r'\[\d+\]|\[\d+_HPE_Account_Admin\]', i):
			found = re.findall(r'\d+\w+', i)

			AID=str(found).strip('[]')
			AccID=AID.strip('[]').strip("'")
			DOT=len(AccID) + 25
			print "\n""\t\t\t\t","*" * DOT  
			print "\t\t\t\t    ACCOUNT NAME: ", AccID
			print "\t\t\t\t", "*" * DOT

			with open(AccID, "w") as wfile:
			        try:
                			subprocess.call(["aws", "--profile",  AccID, "iam",  "get-account-authorization-details", "--output",  "json"], stdout=wfile)
					
					with open(AccID) as file:
		                                a = json.load(file)
				
						la(a, UDL, UN, AMP, PN); la(a, GDL, GN, AMP, PN); la(a, RDL, RN, AMP, PN)
			        except :
			                print "\t\t\t......Not Able To Get The Account(", AccID ,")Details....."
			os.remove(AccID)
