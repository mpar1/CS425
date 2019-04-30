import psycopg2 as db
import urllib.parse as up
import os
import sys

up.uses_netloc.append("postgres")
url = up.urlparse("postgres://fcbeygin:nPzIeoASpjJTLArcn4BCdZB_SzchCX78@isilo.db.elephantsql.com:5432/fcbeygin")
conn = db.connect(database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)

cursor = conn.cursor()

def do_action(action,priv):

	if priv == "admin":
	
		action_switch = {
			"1" : schedule_appoint,
			"2" : create_patient,
			"3" : create_account,
			"4" : access_reports,
			"5" : quit_program
		}
		
	elif priv == "medicalStaff":
	
		action_switch = {
			"1" : access_records,
			"2" : create_order,
			"3" : access_calendar,
			"4" : quit_program
		}
	
	elif priv == "patient":
	
		action_switch = {
			"1" : view_orders,
			"2" : view_bills,
			"3" : quit_program
		}
		
	elif priv == "scheduler":
	
		action_switch = {
			"1" : view_orders,
			"2" : view_bills,
			"3" : access_calendar,
			"4" : quit_program
		}
		
		action_switch.get(action, wrong_option)


def schedule_appoint(action):
    pass
	
def access_records(var):
    pass

def access_calendar(action):
	pass

def access_reports(action):
    pass

def create_patient():
	pass

def create_account():
	print("New Username: ")
	user = input()
	print("New Password: ")
	pw = input()
	print("Privilege (patient, medicalStaff, scheduler, admin): ")
	while (true):
		priv = input()
		if priv == "patient":
			cursor.execute("SELECT * FROM patient")
			patients = cursor.fetchall()
			print("\n===============================\n")
			for row in patients:
				print("ID: " + row[3] + " | Name: " + row[0] + " " + row[1] + " | Address: " + row[2] + "\n")
			print("\n===============================\n")
			break
		elif priv == "medicalStaff" or priv == "scheduler" or priv == "admin":
			cursor.execute("SELECT * FROM employee")
			employees = cursor.fetchall()
			print("\n===============================\n")
			for row in employees:
				print("ID: " + row[2] + " | Name: " + row[0] + " " + row[1] + " | Job Type: " + row[3] + "\n")
			print("\n===============================\n")
			break
		else: 
			print("Please input a valid privilege \n (patient, medicalStaff, scheduler, admin)")
	print("Please input the ID of the person you wish to connect this account to: ")
	id = input()
	loginDet = [user, pw]
	if priv == "patient":
		loginDet.append(str(id))
		loginDet.append(None)
	else:
		loginDet.append(None)
		loginDet.appent(str(id))
	loginDet.append(priv)
	
	command = "INSERT INTO login VALUES (" + row[0] + ", " + row[1] + ", " + row[2] + ", " + row[3] + ", " + row[4] + ")"
	
	print("Login created!")
	
def view_orders():
	pass

def view_bills():
	pass

def quit_program():
	print("Quiting program")
	conn.close()
	sys.exit(0)

def wrong_option(action):
    print("Invalid option")
	
''' Pulls whole login table from database and attempts a login.
	If successful, returns login details as a list [userID, password, patient, employee, privilege, LoginTime, LogoutTime]
'''
def try_login(u,p):

	cursor.execute("SELECT * FROM login")
	
	logins = cursor.fetchall()
	logindetails = []
	
	while True:
		if u == "q":
			quit_program()
		for row in logins:
			if row[0] == u:
				while True:
					if row[1] == p:
						for x in row:
							logindetails.append(x)
						print("Login Successful!")
						return logindetails
					elif p == "q": #Doesn't work if password is q
						quit_program()
					else:
						print("Wrong password. Please try again, or input q to close. \n")
						print("Password: ")
						p = input()
		print("Username not found. Please try again, or input q to close. \n")
		print("Username: ")
		u = input()
					


def menu(priv):

	print("\n===============================\n")

	adminPrompt =  "1. Schedule an appointment\n" \
            + "2. Create new patient\n" \
            + "3. Create new user account\n" \
            + "4. View reports\n" 
	
	staffPrompt =  "1. View and update patient record\n" \
            + "2. Create a order\n" \
            + "3. View calendar and schedule appointment\n"
	
	patientPrompt =  "1. View orders\n" \
            + "2. View bills\n" \
		
	schedulerPrompt =  "1. Schedule an appointment\n" \
            + "2. Create new patient\n" \
            + "3. Create new user account\n" \
            + "4. View reports\n" 
	
	endcl = "5. Quit\n" \
            + "===============================\n" \
            + "Enter in the number for the action:"
			
	action_switch = {
        "admin" : adminPrompt,
        "medicalStaff" : staffPrompt,
        "patient" : patientPrompt,
        "scheduler" : schedulerPrompt,
    }
	
	print(action_switch.get(priv, "Invalid Option"))
	
	print(endcl)


def main():
	print("Welcome to the medical clinic, please log in:")
	'''
	prompt =  "\n===============================\n" \
            + "1. Schedule an appointment\n" \
            + "2. View medical record\n" \
            + "3. View Doctor calendar\n" \
            + "4. View reports\n" \
            + "5. Quit\n" \
            + "===============================\n" \
            + "Enter in the number for the action:"
	'''

	print("Username: ")
	u = input()
	print("Password: ")
	p = input()
	
	#[userID, password, patient, employee, privilege, LoginTime, LogoutTime]
	loginDetails = try_login(u,p)
	priv = loginDetails[4]

	print("Welcome, " + u + "! Please select any of the following: ")
	
	menu(priv)

	while True:
		action = input(prompt)
		do_action(action, priv)
        
        

main()
