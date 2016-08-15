import requests
import re
import os
from lxml import html

# LoginURL: http://www.spoj.com/login
# SubmissionsURL: http://www.spoj.com/status/'+[Username]+'/signedlist/'
# CodeURL: http://www.spoj.com/files/src/[SubmissionID]/

Loginurl = 'http://www.spoj.com/login'
login_details = dict(login_user='username',password='password')	# Change these values to your login details

session = requests.session()				# Creates a session object
session.post(Loginurl, data=login_details)	# Logs into the SPOJ site

# SPOJ provides a plain text view of all our submissions.
# The following code extracts the information on what problems are solved from that link.
SubmissionsURL = 'http://www.spoj.com/status/'+login_details['login_user']+'/signedlist/'
submissions = session.get(SubmissionsURL)

# submissions.content contains the data parsed from that page
# print submissions.content

lines = []
line = ""
length = len(submissions.content)

# Storing all the data in that page into lines list
i = 0
while i < length:
	j = i
	while j < length:
		if submissions.content[j] != '\n':
			line += submissions.content[j]
		else:
			lines.append(line)
			line = ""
			i = j
			break
		j += 1
	i+=1

# Creating a new directory in current directory to store all the correct solutions
if not os.path.isdir('spoj_solutions'):
	os.makedirs('spoj_solutions',0777)

# The extensions are added only for 4 languages for now.
# The code is written such that all other languages are stored in .txt format.
# Can add more file type extensions if needed
# Look into the language code on SPOJ for the one you want to add.(ex: for python, its 'PYT')
extenstions = {'C':'c', 'C++':'cpp', 'PYT':'py', 'JAV':'java'}

flag = 0	# Flag is 2 when the for loop is executing on line which contains details of a submission

for line in lines:

	# Extracting required information from line using regex
	words = re.findall('\s+([+a-zA-Z0-9]+)\s+',line)
	if flag >= 1 and len(words) == 0:
		flag += 1
	
	elif flag == 2:

		# Parsing only those solutions that are accepted
		if words[2] == "AC":
			filename = words[1]+'.'+extenstions.get(words[4],'txt')

			# If a problem is solved in same language multiple times, the latest correct submission is saved
			# Edit the statement below if you want to save all the correct submissions
			if not os.path.isfile('spoj_solutions/'+filename):
				with open('spoj_solutions/'+filename,"w+") as sourceFile:
					CodeURL = 'http://www.spoj.com/files/src/'+words[0]+'/'
					HTMLcode = session.get(CodeURL)
					HTMLcode = html.fromstring(HTMLcode.content)

					# Parses all data in <li> that are inside <ol>
					res = HTMLcode.xpath('//ol/li')
					for a in res:
						sourceFile.write("".join([t for t in a.itertext()]).encode("utf-8"))
						sourceFile.write("\n")
					
	elif len(words) >= 1:
		if words[0] == "ID":
			flag = 1
