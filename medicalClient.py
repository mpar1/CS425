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



def get_action(user_in):
    action_switch = {
        "1" : schedule_appoint,
        "2" : view_records,
        "3" : doc_calandar,
        "4" : view_reports,
        "5" : quit_program
    }
    return action_switch.get(user_in, wrong_option)

def schedule_appoint(action):
    pass

def view_records(var):
    print("hello")

def doc_calandar(action):
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

def view_reports(action):
    pass

def quit_program(action):
    print("Quiting program")
    conn.close()

def wrong_option(action):
    print("Invalid option")


def main():
    print("Welcome to the medical clinic, please select any of the following options:")
    prompt =  "\n===============================\n" \
            + "1. Schedule an appointment\n" \
            + "2. View medical record\n" \
            + "3. View Doctor calendar\n" \
            + "4. View reports\n" \
            + "5. Quit\n" \
            + "===============================\n" \
            + "Enter in the number for the action:"

    action = ""

    while action != "5":
        action = input(prompt)
        get_action(action)(action)
        
        

main()
