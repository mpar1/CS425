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
    pass

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
