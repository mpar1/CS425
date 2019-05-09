import psycopg2 as db
import urllib.parse as up
import os
import sys
from datetime import datetime

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
					"group by customerID, category")
	records = cursor.fetchall()
	print("Here are all the patient records")
	for record in records:
		print(f"Patient: {record[0]}\nList of all treatments: {record[1]}\n")


def access_calendar(): #view appointments for a specific doctor
	cursor.execute("select fname, lname, staffID\n"
					+ "from employee\n"
					+ "where jobtype='Medical Staff'")
	doc_lst = cursor.fetchall()

	print("The doctors are:")
	for num, doc in enumerate(doc_lst):
		print(f"{num+1}: {doc[0]} {doc[1]}")

	while True:
		try:
			doc_idx = int(input("Select which doctor you would like to see the calandar for\n" \
							  + "(Please enter the number corresponding with the doctor): "))-1
			doc = doc_lst[doc_idx]
			break
		except:
			print("Please enter a valid number")

	doc_id = doc[2]
	cursor.execute("select appointdate, patient\n"
				   "from appointments\n"
				  f"where meeting='{doc_id}'")
	schedule = cursor.fetchall()

	print("The apointments for {0} are:".format(doc[1]))
	for appoint in schedule:
		print("Patient: {1}\nDate: {0}\n".format(appoint[0], appoint[1]))

def view_orders():
	cursor.execute("select * from orders")
	orders = cursor.fetchall()
	print("Here is the log of all orders:")
	for order in orders:
		print(order)

def access_reports():
	cursor.execute("SELECT * FROM orders as o JOIN diagnostic as d ON o.diagnosticID=d.ID")
	orders = cursor.fetchall() #[orderID,customerID,staffID,diagnosticID,results,price,category]
	costsum = 0
	t_counts = {"Lab":0, "MRI":0, "Xray":0, "Office Visit":0}
	visitrev = 0
	for row in orders:
		costsum += row[6]
		row_type = row[7]
		t_counts[row_type] += 1
		if row_type == "Office Visit":
			visitrev += row[6]

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

def show_patients(verbose=False):
	cursor.execute("SELECT * FROM patient")
	patients = cursor.fetchall()
	print("Here is a list of all of the patients: ")
	print("\n===============================\n")
	for row in patients:
		info = f"ID: {row[3]}  | Name: {row[0]} {row[1]}"
		if verbose:
			info += f" | Address: {row[2]}"

		print(info)
	print("\n===============================\n")


def show_employees(verbose=False): #no grouping between doc and others
	cursor.execute("SELECT * FROM employee")
	employees = cursor.fetchall()
	print("Here is a list of all of the employees: ")
	print("\n===============================\n")
	for row in employees:
		info = f"ID: {row[2]} | Name: {row[0]} {row[1]}"
		if verbose:
			info += f" | Job Type: {row[3]}"

		print(info)
	print("\n===============================\n")

def view_prompt(prompt, lst_name, show_func): #gives option to print vals in database
	u_in = ""
	while (not u_in.isalnum() and u_in != "v") or u_in == "v":
		if u_in == "v":
			show_func()
		else:
			print(f"View the list of {lst_name} by typing \"v\"")
		u_in = input(prompt)
	return u_in

def schedule_appoint():
	date= input("Enter in the date(yyyy-mm-dd) of the appointment: " )
	while True:
		try:
			pID_in = view_prompt("Enter in the ID of the patient: ", "patients", show_patients)
			sID_in = view_prompt("Enter in the ID of staff meeting the patient: ", "employees", show_employees)
			pID = int(pID_in)
			sID = int(sID_in)
			break
		except:
			print("One of the ids entered was invalid, please try again")

	PGsql = f"insert into appointments(appointDate, patient, meeting) values('{date}', '{pID:03d}', '{sID:02d}');"

	cursor.execute(PGsql, (date, pID, sID))
	conn.commit()
	print("Your Appointment has been created. Returing back to the main menu. ")

def create_order():
	cID = view_prompt("Enter in the ID for the customer: ", "customers", show_patients)
	stID = view_prompt("Enter in the ID for the staff: ", "employees", show_employees)

	dID = input("Enter in the ID for the diagnostic: ")
	res = input("Enter in the results: ")
	cursor.execute("select max(patientID) from patient")
	oID = int(cursor.fetchone()[0])+1
	pgsql = """insert into orders(orderID, customerID, staffID, diagnosticID, results)
				values('ord%s', %s, %s, %s, %s)"""
	cursor.execute(pgsql, (oID, cID, stID, dID, res))
	#cursor.fetchall()
	conn.commit()
	count=cursor.rowcount
	print(count, "Your order has been succesfully created. Returning back to main menu")

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
		command = f"insert into patient values ('{attrs[0]}', '{attrs[1]}', '{attrs[2]}', '{id:03d}')"
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
			show_patients(True)
			break
		elif priv == "medicalStaff" or priv == "scheduler" or priv == "admin":
			show_employees(True)
			break
		else:
			print("Please input a valid privilege \n (patient, medicalStaff, scheduler, admin)")

	id_str = input("Please input the ID of the person you wish to connect this account to: ")
	id = int(id_str)
	log = [user, pw]
	if priv == "patient":
		log.append(id)
		log.append('NULL')
	else:
		log.append('NULL')
		log.append(id)

	t = str(datetime.now().time())
	t = t[:8]
	log.append(t)
	log.append(priv)

	command = f"INSERT INTO login VALUES ('{log[0]}', '{log[1]}', '{log[5]}', '{log[4]}', '{log[4]}', {log[2]}, {log[3]})"
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
			t = str(datetime.now().time())
			t = t[:8]
			command = f"UPDATE login SET logintime = '{t}' WHERE userid = '{user_info[0]}'"
			cursor.execute(command)
			command2 = f"SELECT logintime FROM login WHERE userid='{user_info[0]}'"
			cursor.execute(command2)
			logintime = cursor.fetchall()
			for t2 in logintime:
				print("Login time recorded:", t2)
			return [val for val in user_info] #convert user info to array
		elif p_word == "q": #Doesn't work if password is q
			quit_program()
		else:
			print("Wrong password. Please try again, or input q to close. \n")


def welcome_login(): #wrapper
	print("Welcome to the medical clinic, please log in:")
	return try_login()

def logout():
	print("Logging out\n")
	return welcome_login()

def menu(priv):
	start_line = ("\n===============================\n")
	adminPrompt =  "1. Schedule an appointment\n" \
					+ "2. Create new patient\n" \
					+ "3. Create new user account\n" \
					+ "4. View reports\n" \
					+ "5. Logout\n"

	staffPrompt =  "1. View patient records\n" \
					+ "2. Create an order\n" \
					+ "3. View calendar\n" \
					+ "4. Schedule appointment\n" \
					+ "5. Logout\n"

	patientPrompt =  "1. View orders\n" \
					+ "2. Logout\n"

	schedulerPrompt =  "1. View orders\n" \
						+ "2. Schedule an appointment\n" \
						+ "3. View calandar\n" \
						+ "4. Logout\n"

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
		"4" : schedule_appoint,
		"5" : logout
	}
	patient = {
		"1" : view_orders,
		"2" : logout
	}
	scheduler = {
		"1" : view_orders,
		"2" : schedule_appoint,
		"3" : access_calendar,
		"4" : logout
	}

	action_switch = {
		"admin" : admin,
		"medicalStaff" : med_staff,
		"patient" : patient,
		"scheduler" : scheduler
	}

	return action_switch.get(priv).get(action, wrong_option)

def main():
	# [userID, password, patient, employee, privilege, LoginTime, LogoutTime]
	login_details = welcome_login()
	priv = login_details[2]
	#priv = "scheduler"
	print(f"Welcome, {login_details[0]}! Please select any of the following: ")

	while True:
		action = input(menu(priv))
		login_details = do_action(priv, action)() #update on relogin
		if login_details:
			priv = login_details[2]



main()
