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

	admin = {
		"1" : schedule_appoint,
		"2" : create_patient,
		"3" : create_account,
		"4" : access_reports,
		"5" : quit_program
	}
	med_staff = {
		"1" : access_records,
		"2" : create_order,
		"3" : access_calendar,
		"4" : quit_program
	}
	patient = {
		"1" : view_orders,
		"2" : quit_program
	}
	scheduler = {
		"1" : view_orders,
		"2" : access_calendar,
		"3" : quit_program
	}

	action_switch = {
		"admin" : admin,
		"medical staff" : med_staff,
		"patient" : patient,
		"scheduler" : scheduler
	}
		
	action_switch.get(action, wrong_option)


def schedule_appoint(action):
    pass
	
def access_records(var):
	pass

def access_calendar(action): #view appointments for a specific doctor
    cursor.execute("select fname, lname, staffID\n"
                 + "from employee\n"
                 + "where jobtype=\"Medical Staff\";")
    doc_lst = cursor.fetchall()
    
    print("The doctors are:")
    for num, doc in enumerate(doc_lst):
        print(f"{num+1}: {doc[0]} {doc[1]}")
    
    while True:
        try:
            doc_idx = int(input("Select which doctor you would like to see calandar for\n \
                                (Please enter the number corresponding with the doctor):"))-1
            break
        except:
            print("Please enter a valid number")

    doc = doc_lst[doc_idx]
    doc_id = doc[2]
    cursor.execute("select date, patient\n"
                   "from appointments\n"
                  f"where meeting=\"{doc_id}\"")
    schedule = cursor.fetchall()

    print("The apointments for {0} are:", doc[1])
    for appoint in schedule:
        print("Patient: {0}\nDate: {1}\n", appoint[0], appoint[1])

def access_reports():
	cursor.execute("SELECT * FROM orders JOIN diagnostic ON orders.diagnosticID=diagnostic.ID")
	orders = cursor.fetchall() #[orderID,customerID,staffID,diagnosticID,results,price,category]
	costsum = 0
	labs = 0
	mris = 0
	xrays = 0
	visits = 0
	for row in orders:
		costsum += row[5]
		if row[6] == "Lab":
			labs += 1
		elif row[6] == "MRI":
			mris += 1
		elif row[6] == "Xray":
			xrays += 1
		elif row[6] == "Office Visit":
			visits += 1
	
	print("\n=====================\n")
	print("Overall order summary: \n")
	print(f"Total number of orders: {str(len(orders))} \n")
	print(f"Total cost of all orders: {str(costsum)}")
	
	
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
	
	command = f"INSERT INTO login VALUES ({row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]})"
	
	print("Login created!")
	
def view_orders():
	currsor.execute("select * from orders")
	orders = currsor.fetchall()
	for order in orders:
		print(order)

def quit_program():
	print("Quiting program")
	conn.close()
	sys.exit(0)

def wrong_option(action):
    print("Invalid option")
	
# Pulls whole login table from database and attempts a login.
# If successful, returns login details as a list [userID, password, patient, employee, privilege, LoginTime, LogoutTime]

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
