import jenkins
import datetime
import sqlite3

#DataInput:
database = raw_input("Please insert database name: ").replace(" ", "")
table = raw_input("Please insert table name: ").replace(" ", "")
username = raw_input("Please insert username: ").replace(" ", "")
password = raw_input("Please insert password: ").replace(" ", "")
# **********************************************************************

conn = sqlite3.connect(database + '.db')
c = conn.cursor()

c.execute("CREATE TABLE " + table + "(Name text, Status text, lastCheck  DATETIME)")

server = jenkins.Jenkins('http://localhost:8080', username = username, password = password)

jobs = server.get_jobs()

for job in jobs:
	color = job['color']
	name = job['fullname']

	if(color == 'blue'):
		lastBuildNumber = server.get_job_info(job['fullname'])['lastBuild']['number']
		lastbuild = server.get_build_info(job['fullname'], lastBuildNumber)
		lastbuild_time = datetime.datetime.fromtimestamp(int(lastbuild['timestamp']*0.001)).strftime('%Y-%m-%d %H:%M:%S')
		status = "Success"

	elif(color == 'notbuilt'):
		status = "Not built"
		lastbuild_time = ""

	else:
		status = "Failed"
		lastbuild_time = ""

	c.execute("INSERT INTO " + table +  " VALUES (?, ?, ?)",(name, status, lastbuild_time))

	conn.commit()

c.execute("SELECT * FROM " + table)
print c.fetchall()
