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
	
def access_records():
	cursor.execute("select customerID, category\n"
				   "from orders join diagnostic\n"
				   "on orders.diagnosticID=diagnostic.ID\n"
				   "group by customerID")
	records = cursor.fetchall()
	print("Here are all the patient records")
	for record in records:
		print(f"Patient: {record[0]}\nList of all treatments: {record[1]}\n")


def access_calendar(): #view appointments for a specific doctor
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

def view_orders():
	cursor.execute("select * from orders")
	orders = cursor.fetchall()
	print("Here is the log of all orders:")
	for order in orders:
		print(order)

def access_reports():
	cursor.execute("SELECT * FROM orders JOIN diagnostic ON orders.diagnosticID=diagnostic.ID")
	orders = cursor.fetchall() #[orderID,customerID,staffID,diagnosticID,results,price,category]
	costsum = 0
	t_counts = {"Lab":0, "MRI":0, "Xray":0, "Office Visit":0}
	visitrev = 0
	for row in orders:
		costsum += row[5]
		row_type = row[6]
		t_counts[row_type] += 1
		if row_type == "Office Visit":
			visitrev += row[5]
	
	mris, xrays, labs, visits = t_counts["MRI"], t_counts["Xray"], t_counts["Lab"], t_counts["Office Visit"]
	print("\n=====================\n")
	print("Overall order summary: \n"
		 f"Total number of orders: {len(orders)} \n"
		 f"Total revenue from all diagnostics: {costsum} \n"
		 f"Total revenue from all doctor visits: {visitrev} \n"
		 f"Total MRIs: {mris} \n"
		 f"Total XRays: {xrays} \n"
		 f"Total Labs: {labs} \n"
		 f"Total Office Visits: {visits} \n"
		  "\n====End of Report====\n")


def schedule_appoint():
    pass

def create_order():
    pass

def create_patient():
    attrs = ["", "", ""]
    while True:
        attrs[0] = input("Enter in the first name of the new patient: ")
        attrs[1] = input("Enter in the last name of the patient: ")
        if attrs[0].isalpha() and attrs[1].isalpha(): #check valid names 
            break
        else:
            print("Invalid name")
    while True:
        attrs[2] = input("Enter in the new patient's address: ")
        if attrs[2][0].isdigit():
            break
        else:
            print("Invalid address")
    try:
        cursor.execute("select max(patientID) from patient")
        id = int(cursor.fetchone()[0])+1
        command = f"insert into patient values ({attrs[0]}, {attrs[1]}, {attrs[2]}, {id})"
        cursor.execute(command)
        conn.commit()
        print("Successfully added patient")
    except:
        print("Error while trying to add new patient")

def create_account():
    user = input("New Username: ")
    pw = input("New Password: ")
    while True:
        priv = input("Privilege (patient, medicalStaff, scheduler, admin): ")
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

    id = input("Please input the ID of the person you wish to connect this account to: ")
    log = [user, pw]
    if priv == "patient":
        log.append(id)
        log.append(None)
    else:
        log.append(None)
        log.append(id)
    log.append(priv)

    command = f"INSERT INTO login VALUES ({log[0]}, {log[1]}, {log[2]}, {log[3]}, {log[4]})"
    cursor.execute(command)
    conn.commit()	
    print("Login created!")

def quit_program():
	print("Quiting program")
	conn.close()
	sys.exit(0)

def wrong_option():
    print("Invalid option")
	
	
# Pulls whole login table from database and attempts a login.
# If successful, returns login details as a list [userID, password, patient, employee, privilege, LoginTime, LogoutTime]

def try_login():
	cursor.execute("SELECT * FROM login")
	logins = cursor.fetchall()
	user_info = None
	valid_user = False
	
	while valid_user == False:
		u_name = input("Username: ")	
		if u_name == 'q':
			quit_program()
		for row in logins:
			if row[0] == u_name:
				user_info = row
				valid_user = True
				break
		else:
			print("Username not found. Please try again, or input q to close. \n")

	while True:
		p_word = input("Password: ")
		if user_info[1] == p_word:
			print("Login Successful!")
			return [val for val in user_info] #convert user info to array
		elif p_word == "q": #Doesn't work if password is q
			quit_program()
		else:
			print("Wrong password. Please try again, or input q to close. \n")


def welcome_login(): #wrapper
	print("Welcome to the medical clinic, please log in:")
	try_login()

def logout():
	print("Logging out\n")
	welcome_login()

def menu(priv):
	start_line = ("\n===============================\n")
	adminPrompt =  "1. Schedule an appointment\n" \
                 + "2. Create new patient\n" \
                 + "3. Create new user account\n" \
                 + "4. View reports\n" \
				 + "5. Logout\n"
	
	staffPrompt =  "1. View patient records\n" \
                 + "2. Create an order\n" \
                 + "3. View calendar and schedule appointment\n" \
				 + "4. Logout\n"
	
	patientPrompt =  "1. View orders\n" \
				   + "2. Logout\n"
		
	schedulerPrompt =  "1. Schedule an appointment\n" \
                     + "2. Create new patient\n" \
                     + "3. Create new user account\n" \
                     + "4. View reports\n" \
					 + "5. Logout\n"
	
	endcl = "===============================\n" \
          + "Enter in the number for the action: "
			
	action_switch = {
        "admin" : adminPrompt,
        "medicalStaff" : staffPrompt,
        "patient" : patientPrompt,
        "scheduler" : schedulerPrompt,
	}
	return start_line + action_switch.get(priv, "Invalid Option") + endcl


def do_action(priv, action):
	admin = {
		"1" : schedule_appoint,
		"2" : create_patient,
		"3" : create_account,
		"4" : access_reports,
		"5" : logout
	}
	med_staff = {
		"1" : access_records,
		"2" : create_order,
		"3" : access_calendar,
		"4" : logout
	}
	patient = {
		"1" : view_orders,
		"2" : logout
	}
	scheduler = {
		"1" : view_orders,
		"2" : access_calendar,
		"3" : logout
	}

	action_switch = {
		"admin" : admin,
		"medical staff" : med_staff,
		"patient" : patient,
		"scheduler" : scheduler
	}

	return action_switch.get(priv).get(action, wrong_option)

def main():
	# [userID, password, patient, employee, privilege, LoginTime, LogoutTime]
	#login_details = welcome_login()
	#priv = login_details[4]
	priv = "admin"
	#print(f"Welcome, {login_details[0]}! Please select any of the following: ")
	while True:
		action = input(menu(priv))
		do_action(priv, action)()

        
main()
