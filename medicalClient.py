import psycopg2 as db
import urllib.parse as up
import os

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
			"4" : access_reporting,
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
			"2" : view_bills
			"3" : quit_program
		}
		
	elif priv == "scheduler":
	
		action_switch = {
			"1" : view_orders,
			"2" : view_bills
			"3" : access_calendar,
			"4" : quit_program
		}
		
    action_switch.get(action, wrong_option)


def schedule_appoint(action):
    pass
	

def view_records(var):
    print("hello")

def doc_calandar(action):
    pass

def view_reports(action):
    pass

def quit_program(action):
    print("Quiting program")
    conn.close()

def wrong_option(action):
    print("Invalid option")
	
''' Pulls whole login table from database and attempts a login.
	If successful, returns login details as a list [userID, password, patient, employee, privilege, LoginTime, LogoutTime]
'''
def try_login(u,p):

	cursor.execute("SELECT * from 'login'")
	
	logins = cursor.fetchall()
	logindetails = []
	
	while True:
		if u == "q"
			quit_program()
		for row in logins:
			if row[0] == u:
				while True:
					if row[1] == p:
						for x in row:
							logindetails.append(x)
						print("Login Successful!")
						return logindetails
					elif p == "q": '''Doesn't work if password is q'''
						quit_program()
					else:
						print("Wrong password. Please try again, or input q to close. \n")
						print("Password: ")
						p = input(prompt)
		print("Username not found. Please try again, or input q to close. \n")
		print("Username: ")
		u = input(prompt)
					
		


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
	
    print(action_switch.get(user_in, "Invalid Option"))
	
	print(endcl)


def main():
    print("Welcome to the medical clinic, please log in:")
    '''prompt =  "\n===============================\n" \
            + "1. Schedule an appointment\n" \
            + "2. View medical record\n" \
            + "3. View Doctor calendar\n" \
            + "4. View reports\n" \
            + "5. Quit\n" \
            + "===============================\n" \
            + "Enter in the number for the action:"
	'''
	print("Username: ")
	u = input(prompt)
	print("Password: ")
	p = input(prompt)
	
	'''[userID, password, priv, LoginTime, LogoutTime]'''
	loginDetails = try_login(u,p)
	priv = login_details[4]

	print("Welcome, " + u + "! Please select any of the following: ")
	
	menu(priv)

    while action != "5":
        action = input(prompt)
        do_action(action, priv)
        
        

main()
