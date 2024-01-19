import sqlite3
import PySimpleGUI as sg
import os 
import json
# import emoji

con = sqlite3.connect('project.db')
cur = con.cursor()

login_user_id = -1
login_user_name = -1
login_user_type = -1

def window_login(): # GENEL
    sg.theme('DarkBlack')  # Set the background color to light green

    layout = [
        [sg.Text('Welcome to MacFit. Please enter your MacFit ID and Password')],
        [sg.Text('ID: ', size=(15, 1)), sg.Input(size=(15, 1), key='user_id')],
        [sg.Text('Password: ', size=(15, 1)), sg.Input(size=(15, 1), key='password')],
        [sg.Button('Login'), sg.Exit()]
    ]
    return sg.Window('Login System', layout)

def window_admin(): # GENEL


    layout = [
        [sg.Text('Welcome ' + login_user_name)],
        [sg.Button('Create New Group Session')],
        [sg.Button('Browse Sessions')],
        [sg.Button('Browse PT Session')],
        [sg.Button('Logout')]
    ]
    return sg.Window('Admin System', layout)

def window_member(): # GENEL
    layout = [
        [sg.Text('Welcome ' + login_user_name)],
        [sg.Button('Browse Sessions')],
        [sg.Button('Browse PT Sessions')],
        [sg.Button('Edit Your Information')],
        [sg.Button('See Your Group Session')],
        [sg.Button('See Your PT Session')],
        [sg.Button('Logout')]
    ]
    return sg.Window('Member System', layout)

def window_trainer(): # GENEL
    layout = [
        [sg.Text('Welcome ' + login_user_name)],
        [sg.Button('See Your Group Sessions')],
        [sg.Button('See Your PT Sessions')],
        [sg.Button('Arrange PT Session')],
        [sg.Button('Logout')]
    ]
    return sg.Window('Trainer System', layout)

def window_create_group_session(): # SENARYO 1

    days_in_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    trainerID_list = []
    exercise_type = []
    studio_number = []

    for row in cur.execute(''' Select TrainerID, Name, Specialities 
                           From Trainer, User
                           Where Trainer.TrainerID = User.UserID'''):
        trainerID_list.append(row[0])
        exercise_type.append(row)
    for row2 in cur.execute('Select StudioNumber From Studio'):
        studio_number.append(row2[0])


    layout = [
        [sg.Text('Create New Group Session')],
        [sg.Text('Session Number:', size=(15, 1)), sg.Input(key='session_number')],
        [sg.Text('Day of the Week:', size=(15, 1)), sg.Combo(days_in_week, size = (43,7), key='day_of_week')],
        [sg.Text('Start Time:', size=(15, 1)), sg.Input(key='start_time')],
        [sg.Text('End Time:', size=(15, 1)), sg.Input(key='end_time')],
        [sg.Text('Exercise Type:', size=(15, 1)), sg.Combo(exercise_type, size = (43,7), key='exercise_type')],
        [sg.Text('Trainer ID:', size=(15, 1)), sg.Combo(trainerID_list, size = (43,7), key='trainer_id')],
        [sg.Text('Studio Number:', size=(15, 1)), sg.Combo(studio_number, size = (43,7), key = 'studio_number')],
        [sg.Button('Create Session'), sg.Button('Return To Main')]
    ]
    return sg.Window('Create Group Session', layout)

def window_create_pt_session(): # SENARYO 2

    days_in_week = ['Monday', 'Tuesday', "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    trainerID_list = []
    pt_session_list = cur.execute('SELECT PT_SessionNumber FROM PT_SESSION').fetchall()

    for row in cur.execute(''' Select TrainerID, Name, Specialities 
                           From Trainer, User
                           Where Trainer.TrainerID = User.UserID'''):
        trainerID_list.append(row[0])

    layout = [
        [sg.Text('Create New PT Session')],
        [sg.Text('PT Session Number:', size=(15, 1)), sg.Input(key='pt_session_number')],
        [sg.Text('Day of the Week:', size=(15, 1)), sg.Combo(days_in_week, size = (43,7), key='day_of_week_pt')],
        [sg.Text('Start Time:', size=(15, 1)), sg.Input(key='start_time_pt')],
        [sg.Text('End Time:', size=(15, 1)), sg.Input(key='end_time_pt')],
        [sg.Button('Create PT Session'), sg.Button('Delete Your PT Session'), sg.Button('Edit Your PT Session'),sg.Button('Return To Main')]
    ]
    return sg.Window('Arrange PT Session', layout)

def window_browse_sessions(): # SENARYO 1
    session_list = cur.execute('SELECT SessionNumber FROM Session').fetchall()
    layout = [
        [sg.Text('Please select a SESSION NUMBER to get information about it: ', size = (65,1))],
        [sg.Combo(values=session_list, size=(5, 1), key='session_list', enable_events=True)],
        [sg.Button('View Details'), sg.Button('Make Reservation'), sg.Button('Return To Main')]
    ]
    return sg.Window('Browse Sessions', layout)

def window_browse_pt_sessions(): # SENARYO 2
    pt_session_list = cur.execute('SELECT PT_SessionNumber FROM PT_SESSION').fetchall()

    layout = [
        [sg.Text('Please select a PT SESSION NUMBER to get information about it: ', size = (65,1))],
        [sg.Combo(values=pt_session_list, size=(5, 1), key='pt_session_list', enable_events=True)],
        [sg.Button('View Details'), sg.Button('Make Reservation'), sg.Button('Return To Main')]
    ]
    return sg.Window('Browse PT Sessions', layout)

def window_confirmation(payment_amount): # SENARYO 3

    layout = [
        [sg.Text(f'The total cost of this PT Session is {payment_amount}TL. If you are ready to pay, just click on confirm.', size = (80,1))],
        [sg.Button('Confirm'), sg.Button('Return To Main')]
    ]
    return sg.Window('Confirmation', layout)

def window_browse_pt_sessions_for_admin(): # SENARYO 2
    pt_session_list = cur.execute('SELECT PT_SessionNumber FROM PT_SESSION').fetchall()

    layout = [
        [sg.Text('Please select a PT SESSION NUMBER to get information about it: ', size = (65,1))],
        [sg.Combo(values=pt_session_list, size=(5, 1), key='pt_session_list', enable_events=True)],
        [sg.Button('View Details'), sg.Button('Return To Main')]
    ]
    return sg.Window('Browse PT Sessions', layout)

def window_browse_trainer_sessions(): # SENARYO 1 VE 2
    session_list = cur.execute('SELECT SessionNumber FROM Session S WHERE S.TrainerID = ?', (login_user_id,)).fetchall()
    layout = [
        [sg.Text('Please select a SESSION NUMBER to get information about it: ', size = (65,1))],
        [sg.Combo(values=session_list, size=(50, 10), key='session_list', enable_events=True)],
        [sg.Button('View Details'), sg.Button('Return To Main')]
    ]
    return sg.Window('Browse Sessions', layout)

def window_trainer_schedule(): # SENARYO 2

    pt_reservation_list = cur.execute('SELECT P.PT_SessionNumber From PT_SESSION P, Trainer T Where P.TrainerID = T.TrainerID AND P.TrainerID = ? ', (login_user_id,)).fetchall()
    
    layout = [

        [sg.Text('Your PT Sessions', size = (50,1))],
        [sg.Combo(values = pt_reservation_list, size = (50,10), key = 'pt_reservation_list', enable_events=True)],
        [sg.Text('Change Your Hourly Fee', size = (45,1))],
        [sg.Input(size = (52,10), key = 'hourly_fee', enable_events=True)],
        [sg.Button('View Details'), sg.Button('Update Your Hourly Fee'), sg.Button('Return To Main')]
    ]
    return sg.Window('See Your PT Sessions', layout)

def window_session_details(session): # SENARYO 1
    layout = [
        [sg.Text(f'Session Details: {session}')],
        [sg.Button('Return To Main')]
    ]
    return sg.Window('Session Details', layout)

def window_make_reservation(values): # SENARYO 1
    reservation_dates = cur.execute('SELECT SessionNumber, Reservation_Date FROM Reservation, Session WHERE Reservation.SessionNumber = Session.SessionNumber').fetchall()
    layout = [
        [sg.Text('Make Reservation')],
        [sg.Text('Reservation Date:', size=(30, 1)), [sg.Combo(values = reservation_dates, key='reservation_date', enable_events=True)]],
        [sg.Button('Make Reservation'), sg.Button('Cancel')]
    ]
    return sg.Window('Make Reservation', layout)

def window_make_pt_reservation(values): # SENARYO 2
    pt_reservation_dates = cur.execute('SELECT PT_SessionNumber, Reservation_Date FROM PT_RESERVATION R, PT_SESSION S WHERE R.PT_SessionNumber = S.SessionNumber').fetchall()
    layout = [
        [sg.Text('Make Reservation')],
        [sg.Text('Reservation Date:', size=(30, 1)), [sg.Combo(values = pt_reservation_dates, key='pt_reservation_date', enable_events=True)]],
        [sg.Button('Make Reservation'), sg.Button('Cancel')]
    ]
    return sg.Window('Make Reservation', layout)

def window_browse_member_info(): # SENARYO 3
    
    layout = [
        [sg.Text('Age:', size=(15, 1)), sg.Input(key='age')],
        [sg.Text('Height:', size=(15, 1)), sg.Input(key='height')],
        [sg.Text('Weight:', size=(15, 1)), sg.Input(key='weight')],
        [sg.Button('Edit Your Information'), sg.Button('Return To Main')]
    ]
    return sg.Window('Browse Sessions', layout)

def window_browse_member_session(): # SENARYO 3

    reservation_list = cur.execute('SELECT SessionNumber FROM Reservation Where MemberID = ?', (login_user_id,)).fetchall()

    layout = [
        [sg.Text('Please select a SESSION NUMBER to get information about it: ', size = (65,1))],
        [sg.Combo(values = reservation_list, size=(15, 1), key='reservation_list', enable_events=True)],
        [sg.Button('View Details'), sg.Button('Cancel Your Reservation'), sg.Button('Return To Main')]
    ]
    return sg.Window('Browse Sessions', layout)

def window_browse_member_pt_session(): # SENARYO 3

    pt_reservation_list = cur.execute('SELECT PT_SessionNumber FROM PT_RESERVATION Where MemberID = ?', (login_user_id,)).fetchall()

    layout = [
        [sg.Text('Please select a SESSION NUMBER to get information about it: ', size = (65,1))],
        [sg.Combo(values = pt_reservation_list, size=(15, 1), key='pt_reservation_list', enable_events=True)],
        [sg.Button('View Details'), sg.Button('Cancel Your PT Reservation'), sg.Button('Return To Main')]
    ]
    return sg.Window('Browse Sessions', layout)

"""
-------- Window End --------
-------- Button Start ------
"""

def button_login(values): # GENEL

    global login_user_id
    global login_user_name
    global login_user_type
    global window

    user_id = values['user_id']
    password = values['password']

    if user_id == '':
        sg.popup('Please enter ID')
    elif password == '':
        sg.popup('Please enter password')
    else:
        cur.execute('Select UserID, Name From User Where UserID = ? and Password = ?', (user_id, password))
        row = cur.fetchone()

        if row is None:
            sg.popup('ID or password is wrong!')
        else:
            login_user_id = row[0]
            login_user_name = row[1]

            cur.execute('Select AdminID From Admin Where AdminID = ?', (user_id,))
            row_admin = cur.fetchone()

            if row_admin is None:
                cur.execute('Select MemberID from Member Where MemberID = ?', (user_id,))
                row_member = cur.fetchone()
                if row_member is None:
                    cur.execute('Select TrainerID from Trainer Where TrainerID = ?', (user_id,))
                    row_trainer = cur.fetchone()
                    if row_trainer is None:
                        sg.popup('User type error! Please enter a valid ID.')
                    else:
                        login_user_type = 'Trainer'
                        sg.popup('Welcome, ' + login_user_name + ' (Trainer)')
                        window.close()
                        window = window_trainer()
                else:
                    login_user_type = 'Member'
                    sg.popup('Welcome, ' + login_user_name + ' (Member)')
                    window.close()
                    window = window_member()
            else:
                login_user_type = 'Admin'
                sg.popup('Welcome,' + login_user_name + ' (Admin)')
                window.close()
                window = window_admin()
    con.commit()

def button_create_pt_session(values): # SENARYO 2
    pt_session_number_str = values.get('pt_session_number', '')

    if pt_session_number_str == '':
        sg.popup('Please enter a valid PT session number.')
        return

    if not pt_session_number_str.isdigit():
        sg.popup('Invalid PT session number. Please enter a numeric value.')
        return

    day_of_week = values['day_of_week_pt']
    start_time = values['start_time_pt']
    end_time = values['end_time_pt']
    trainer_id_str = login_user_id

    new_pt_session_number = int(pt_session_number_str)
    cur.execute('SELECT MAX(PT_SessionNumber) FROM PT_SESSION')
    row = cur.fetchone()
    el = []
    for row2 in cur.execute('Select PT_SessionNumber From PT_SESSION'):
        el.append(int(row2[0]))
        
    if row is None:
        new_pt_session_number = 1
    elif new_pt_session_number < row[0] and new_pt_session_number not in el:
        new_pt_session_number = int(pt_session_number_str)
    else:
        sg.popup('PT Session number that you entered does not fit with the order of the system! Let it be corrected by the system.')
        new_pt_session_number = row[0] + 1
    '''
    if new_pt_session_number > int(pt_session_number_str):
        sg.popup('PT Session number that you entered does not fit with the order of the system! Let it be corrected by the system.')
        new_no = int(new_pt_session_number)

    elif new_pt_session_number < int(pt_session_number_str):
        sg.popup('PT Session number that you entered does not fit with the order of the system! Let it be corrected by the system.')
    else:
        new_no = int(new_pt_session_number)
    '''

    if trainer_id_str == '':
        sg.popup('Please enter valid numeric values for trainer ID.')
        return

    if not str(trainer_id_str).isdigit():
        sg.popup('Invalid trainer ID. Please enter numeric values.')
        return

    trainer_id = int(trainer_id_str)

    cur.execute(
        'SELECT * FROM Session WHERE TrainerID = ? AND DayOfWeek = ? AND ((StartTime <= ? AND EndTime >= ?) OR (StartTime <= ? AND EndTime >= ?))',
        (trainer_id, day_of_week, start_time, start_time, end_time, end_time))
    trainer_conflict = cur.fetchone()


    cur.execute('''
        SELECT *
        FROM PT_SESSION P
        WHERE TrainerID = ? AND P.DayOfWeek = ?
        AND ((StartTime <= ? AND EndTime >= ?) OR (StartTime <= ? AND EndTime >= ?))
    ''', (trainer_id, day_of_week, start_time, start_time, end_time, end_time))
    session_pt_conflict = cur.fetchone()

    if trainer_conflict:
        sg.popup(
            'Sorry! Trainer is not available during the specified time. Please add a PT session for an appropriate time.')
    elif session_pt_conflict:
        sg.popup(
            'Sorry! Trainer is not available during the specified time since the group session is assigned for him/her.')
    else:
        # No conflict, proceed with the insertion
        cur.execute(
            'INSERT INTO PT_Session (PT_SessionNumber, DayOfWeek, StartTime, EndTime, TrainerID) VALUES (?, ?, ?, ?, ?)',
            (new_pt_session_number, day_of_week, start_time, end_time, trainer_id))
        sg.popup('PT Session created successfully!')

    con.commit()

def button_create_session(values): # SENARYO 1
    session_number_str = values.get('session_number', '')

    if session_number_str == '':
        sg.popup('Please enter a valid session number.')
        return

    if not session_number_str.isdigit():
        sg.popup('Invalid session number. Please enter a numeric value.')
        return

    day_of_week = values['day_of_week']
    start_time = values['start_time']
    end_time = values['end_time']
    exercise_type = list(values['exercise_type'])
    trainer_id_str = values.get('trainer_id', '')
    studio_number_str = str(values.get('studio_number', ''))
    new_session_number = int(session_number_str)
    cur.execute('SELECT MAX(SessionNumber) FROM Session')
    row = cur.fetchone()
    if row is None:
        new_session_number = 1
    else:
        new_session_number = row[0] + 1

    if new_session_number > int(session_number_str):
        sg.popup('Session number that you entered does not fit with the order of the system! Let it be corrected by the system.')
        new_no = int(new_session_number)

    elif new_session_number < int(session_number_str):
        sg.popup('Session number that you entered does not fit with the order of the system! Let it be corrected by the system.')
        new_no = int(new_session_number)
    else:
        new_no = int(new_session_number)
        
    if trainer_id_str == '' or studio_number_str == '':
        sg.popup('Please enter valid numeric values for trainer ID and studio number.')
        return

    if not str(trainer_id_str).isdigit() or not studio_number_str.isdigit():
        sg.popup('Invalid trainer ID or studio number. Please enter numeric values.')
        return

    trainer_id = int(trainer_id_str)
    studio_number = int(studio_number_str)

    cur.execute(
        'SELECT * FROM Session WHERE StudioNumber = ? AND DayOfWeek = ? AND ((StartTime >= ? AND StartTime < ?) OR (EndTime > ? AND EndTime <= ?))',
        (studio_number, day_of_week, start_time, end_time, start_time, end_time))
    studio_conflict = cur.fetchone()

    cur.execute(
        'SELECT * FROM Session WHERE TrainerID = ? AND DayOfWeek = ? AND ((StartTime >= ? AND StartTime < ?) OR (EndTime > ? AND EndTime <= ?))',
        (trainer_id, day_of_week, start_time, end_time, start_time, end_time))
    trainer_conflict = cur.fetchone()

    if studio_conflict or trainer_conflict:
        sg.popup(
            'Sorry! Studio or Trainer is not available during the specified time. Please add a session for an appropriate time.')
    else:
        # No conflict, proceed with the insertion
        cur.execute(
            'INSERT INTO Session (SessionNumber, DayOfWeek, StartTime, EndTime, ExerciseType, TrainerID, StudioNumber) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (new_no, day_of_week, start_time, end_time, exercise_type[2], trainer_id, studio_number))

        sg.popup('Group Session created successfully!')

    con.commit()

def make_pt_reservation(session_number, login_user_id, reservation_date, payment_amount, day): # SENARYO 2
    if reservation_date == '':
        sg.popup('Please enter a reservation date')
    else:
        insert_query = """
        INSERT INTO PT_RESERVATION (PT_SessionNumber, MemberID, Reservation_Date, Payment_Amount)
        VALUES (?, ?, ?, ?)
        """
        check_session = '''
            SELECT S.StartTime, S.Endtime 
            FROM PT_RESERVATION P, RESERVATION R, Session S
            WHERE P.MemberID = R.MemberID AND P.MemberID = ? AND P.Reservation_Date = ? AND DayOfWeek = ?
                AND S.SessionNumber = R.SessionNumber AND ((StartTime <= ? AND EndTime >= ?))
        '''
        try:
            cur.execute(insert_query, (session_number, login_user_id, reservation_date, payment_amount))
            cur.execute(check_session, (login_user_id, reservation_date, day, reservation_date, reservation_date))
            conflict_row = cur.fetchall()
            con.commit()


            if not conflict_row:
                # No conflicts, continue with the reservation
                sg.popup(f'Reservation added successfully for PT Session {session_number} on {reservation_date} by MemberID {login_user_id} with total payment as {payment_amount}TL')
            elif reservation_date >= conflict_row[0][0] and reservation_date <= conflict_row[0][1]:
                # There is a conflict, delete the reservation
                cur.execute('DELETE FROM PT_RESERVATION WHERE PT_SessionNumber = ?', (session_number,))
                sg.popup('Sorry! You have a group session assigned for you in this time period!')

            
        except sqlite3.IntegrityError:
            sg.popup('Error: Unique constraint violated. This PT Session is already reserved!')

def make_reservation(session_number, login_user_id, reservation_date, day): # SENARYO 1

    if reservation_date == '':
        sg.popup('Please enter a reservation date')
    else:
        insert_query = """
        INSERT INTO Reservation (SessionNumber, MemberID, Reservation_Date)
        SELECT ?, ?, ?
        WHERE (
            SELECT COUNT(*) FROM Reservation R
            JOIN Session S ON R.SessionNumber = S.SessionNumber
            JOIN Studio ST ON S.StudioNumber = ST.StudioNumber
            WHERE R.SessionNumber = ?
        ) <
        (
            SELECT Capacity FROM Studio
            WHERE StudioNumber = (
                SELECT StudioNumber FROM Session
                WHERE SessionNumber = ?
            )
        );
        """


        check_pt_session = '''
            SELECT S.StartTime, S.Endtime 
            FROM PT_RESERVATION P, RESERVATION R, PT_SESSION S
            WHERE P.MemberID = R.MemberID AND R.MemberID = ? AND R.Reservation_Date = ? AND S.DayOfWeek = ?
                AND S.PT_SessionNumber = P.PT_SessionNumber AND ((S.StartTime <= ? AND S.EndTime >= ?))
        '''
        
        check_session = '''
            SELECT  *
FROM RESERVATION R, Session S
WHERE S.SessionNumber = R.SessionNumber AND R.MemberID = ?  AND S.SessionNumber != ? AND S.DayOfWeek = ?
AND (S.StartTime <= ? AND S.EndTime >= ?)

        '''

        
        all_reservations_list = []
        cur.execute('Select SessionNumber, MemberID from Reservation')
        all_reservations = cur.fetchall()
        all_reservations_list.append(all_reservations)
        all_reservations_list = list(all_reservations_list)
        
        cur.execute(insert_query, (session_number, login_user_id, str(reservation_date), session_number, session_number))
        con.commit()
        existing_reservation_list = []


        cur.execute('SELECT SessionNumber, MemberID FROM Reservation WHERE SessionNumber = ? AND MemberID = ? AND Reservation_Date = ?',
                    (session_number, login_user_id, reservation_date))
        existing_reservation = cur.fetchone()
        existing_reservation_list.append(existing_reservation)
        existing_reservation_list = list(existing_reservation_list)

        
        cur.execute(check_pt_session, (login_user_id, reservation_date, day, reservation_date, reservation_date))
        conflict_row = cur.fetchall()
        con.commit()
        cur.execute(check_session, (login_user_id, session_number, day, reservation_date, reservation_date))
        conflict_row_2 = cur.fetchall()

        if existing_reservation_list[0] in all_reservations_list[0]:
            sg.popup('You have already registered for this session!')
            cur.execute('DELETE FROM Reservation WHERE SessionNumber = ?', (session_number,))
            cur.execute(insert_query, (session_number, login_user_id, str(reservation_date), session_number, session_number))
            con.commit()
        
        elif conflict_row_2:
            cur.execute('DELETE FROM Reservation WHERE SessionNumber = ?', (session_number,))
            sg.popup('Sorry! You have a group session assigned for you in this time period!')
            con.commit()
            
        elif conflict_row:
            if reservation_date >= conflict_row[0][0] and reservation_date <= conflict_row[0][1]:
                cur.execute('DELETE FROM Reservation WHERE SessionNumber = ?', (session_number,))
                sg.popup('Sorry! You have a PT session assigned for you in this time period!')
                con.commit()
        else:
            sg.popup('Reservation Added!')
    con.commit()

def button_delete_pt_session(values): # SENARYO 2
    pt_session_number_str = values.get('pt_session_number', '')

    if pt_session_number_str == '':
        sg.popup('Please enter a valid PT session number.')
        return

    if not pt_session_number_str.isdigit():
        sg.popup('Invalid PT session number. Please enter a numeric value.')
        return

    new_pt_session_number = int(pt_session_number_str)
    cur.execute('SELECT MAX(PT_SessionNumber) FROM PT_SESSION')
    row = cur.fetchone()[0]  

    cur.execute('SELECT * FROM PT_SESSION')
    pt_sessions = cur.fetchall()

    for session in pt_sessions:
        if pt_sessions is None:
            sg.popup('There is no PT Session assigned!')
        elif new_pt_session_number == session[0]:
            cur.execute('DELETE FROM PT_SESSION WHERE PT_SessionNumber = ?', (new_pt_session_number,))
            sg.popup(f'{new_pt_session_number}th PT Session has been DELETED!')
        elif new_pt_session_number > row:
            new_pt_session_number = row
            cur.execute('DELETE FROM PT_SESSION WHERE PT_SessionNumber = ?', (new_pt_session_number,))
            sg.popup(f'{new_pt_session_number}th PT Session has been DELETED!')

    con.commit()

def button_edit_pt_session(values):
    pt_session_number_str = values.get('pt_session_number', '')

    if pt_session_number_str == '':
        sg.popup('Please enter a valid PT session number.')
        return

    if not pt_session_number_str.isdigit():
        sg.popup('Invalid PT session number. Please enter a numeric value.')
        return

    day_of_week = values['day_of_week_pt']
    start_time = values['start_time_pt']
    end_time = values['end_time_pt']
    trainer_id_str = login_user_id
    pt_session_no = int(pt_session_number_str)
    cur.execute('SELECT MAX(PT_SessionNumber) FROM PT_SESSION')
    row = cur.fetchone()
    if row is None:
        pt_session_no = 1

    elif pt_session_no <= 0:
        sg.popup('It cannot be negative or zero!')
        pt_session_no = row[0] + 1 
    elif pt_session_no > row[0]:
        sg.popup('PT Session number that you entered does not fit with the order of the system! Let it be corrected by the system.')
        pt_session_no = row[0] + 1

    if trainer_id_str == '':
        sg.popup('Please enter valid numeric values for trainer ID.')
        return

    if not str(trainer_id_str).isdigit():
        sg.popup('Invalid trainer ID. Please enter numeric values.')
        return

    trainer_id = int(trainer_id_str)

    cur.execute(
        'SELECT * FROM Session WHERE TrainerID = ? AND DayOfWeek = ? AND ((StartTime <= ? AND EndTime >= ?) OR (StartTime <= ? AND EndTime >= ?))',
        (trainer_id, day_of_week, start_time, start_time, end_time, end_time))
    trainer_conflict = cur.fetchone()

    cur.execute('''
        SELECT *
        FROM PT_SESSION P
        WHERE TrainerID = ? AND P.DayOfWeek = ?
        AND ((StartTime <= ? AND EndTime >= ?) OR (StartTime <= ? AND EndTime >= ?))
    ''', (trainer_id, day_of_week, start_time, start_time, end_time, end_time))
    session_pt_conflict = cur.fetchone()


    if trainer_conflict:
        sg.popup(
            'Sorry! Trainer is not available during the specified time. Please add a PT session for an appropriate time.')
    elif session_pt_conflict:
        sg.popup(
            'Sorry! Trainer is not available during the specified time since the group session is assigned for him/her.')
    else:
        cur.execute(
                    'UPDATE PT_Session SET DayOfWeek=?, StartTime=?, EndTime=?, TrainerID=? WHERE PT_SessionNumber=?',
                    (day_of_week, start_time, end_time, trainer_id, pt_session_no)
                )
        sg.popup('PT Session edited successfully!')
        con.commit()


def button_browse_sessions_handler():
    window_browse = window_browse_sessions()
    window_details = None  # Initialize window_details outside the if block

    while True:
        event, values = window_browse.read()

        if event == sg.WIN_CLOSED or event == 'Return To Main':
            window_browse.close()
            break
        elif event == 'View Details':
            if values['session_list']:
                selected_session_i = values['session_list'][0]
                selected_session_from_session_list = cur.execute('SELECT * FROM Session WHERE rowid = ?',
                                                  (selected_session_i,)).fetchone()
                selected_session_dict = dict(zip([desc[0] for desc in cur.description], selected_session_from_session_list))

                # Check capacity and conflicts before making a reservation
                studio_number = selected_session_dict['StudioNumber']
                selected_session_index = values['session_list'][0]
                selected_session = list(cur.execute('SELECT * FROM Session S, User U WHERE S.TrainerID = U.UserID AND S.SessionNumber = ?',
                                              (selected_session_index,)).fetchone())

                cur.execute('SELECT Capacity FROM Studio WHERE StudioNumber = ?', (studio_number,))
                capacity = cur.fetchone()[0]

                cur.execute('SELECT COUNT(*), R.SessionNumber FROM Reservation R, Session S WHERE R.SessionNumber = S.SessionNumber AND R.SessionNumber = ? GROUP BY R.SessionNumber', (selected_session_i,))
                reservations_count = cur.fetchone()

                day = selected_session[1]
                time_interval = selected_session[2] + ' - ' + selected_session[3]
                
                window_details = window_session_details(f'{day} {time_interval} trained by {selected_session[8]}. The number of registration is 0 out of {capacity}')

                if reservations_count is not None:
                    reservation_count = reservations_count[0]
                    shown = f'{day} {time_interval} trained by {selected_session[8]}. The number of registration is {reservation_count} out of {capacity}'
                    window_details = window_session_details(shown)

                select_query = """
SELECT U.Name, U.Surname
FROM RESERVATION R
JOIN SESSION S ON R.SessionNumber = S.SessionNumber
JOIN User U ON R.MemberID = U.UserID
WHERE R.SessionNumber = ?;
"""
                session_number = values['session_list'][0]
                print(session_number)

                selected_session = cur.execute(select_query,
                                              (session_number,)).fetchall()
                selected_session_new = []
                for row in selected_session:   
                    name = row[0]
                    surname = row[1]
                    nameandsurname = name + ' ' + surname
                    selected_session_new.append(nameandsurname)
                result_string = ', '.join(selected_session_new)

                if result_string == '':
                    sg.popup('This session is empty since no one is registered!')
                else:
                    sg.popup(result_string)
                while True:
                    event_details, _ = window_details.read()
                    if event_details == sg.WIN_CLOSED or event_details == 'Return To Main':
                        window_details.close()
                        break
                else:
                    sg.popup(f'{day} {time_interval} trained by {selected_session[8]}. The number of registration is 0 out of {capacity}')
        elif event == 'Make Reservation':
            if values['session_list']:
                selected_session_index = values['session_list'][0]
                selected_session_from_session_list = cur.execute('SELECT * FROM Session WHERE rowid = ?',
                                              (selected_session_index,)).fetchone()
                selected_session_dict = dict(zip([desc[0] for desc in cur.description], selected_session_from_session_list))

                studio_number = selected_session_dict['StudioNumber']
                session_number = selected_session_dict['SessionNumber']
                reservation_date = selected_session_dict['StartTime']
                day = selected_session_dict['DayOfWeek']

                cur.execute('SELECT Capacity FROM Studio WHERE StudioNumber = ?', (studio_number,))
                capacity = cur.fetchone()[0]

                cur.execute('SELECT COUNT(*) FROM Reservation R, Session S WHERE R.SessionNumber = S.SessionNumber AND R.SessionNumber = ? AND S.StudioNumber = ? GROUP BY S.SessionNumber', (session_number, studio_number,))
                reservations_count = cur.fetchone()

                if reservations_count is not None:
                    reservation_count = reservations_count[0]

                    if reservation_count >= capacity:
                        sg.popup('Sorry! The studio is full in that time interval. Please choose another.')
                    else:
                        button_make_reservation(session_number, login_user_id, reservation_date, day)
                        con.commit()
                else:
                    button_make_reservation(session_number, login_user_id, reservation_date, day)
                    con.commit()

    con.commit()

def button_browse_sessions_trainer_handler(): # SENARYO 1
    window_browse = window_browse_trainer_sessions()

    while True:
        event, values = window_browse.read()

        if event == sg.WIN_CLOSED or event == 'Return To Main':
            window_browse.close()
            break
        elif event == 'View Details':
            # Check if session_list is not empty before accessing its elements
            if values['session_list']:
                selected_session_index = values['session_list'][0]
                selected_s = list(cur.execute('SELECT * FROM Session S, User U WHERE S.TrainerID = U.UserID AND S.SessionNumber = ?',
                                              (selected_session_index,)).fetchone())
                day = selected_s[1]
                time_interval = selected_s[2] + ' - ' + selected_s[3]
                shown = f'{day} {time_interval} trained by {selected_s[8]}'
                window_details = window_session_details(shown)

                select_query = """
SELECT U.Name, U.Surname
FROM Reservation R
JOIN Session S ON R.SessionNumber = S.SessionNumber
JOIN User U ON R.MemberID = U.UserID
WHERE R.SessionNumber = ?;
"""

                session_number = selected_s[0]
                selected_session = cur.execute(select_query,
                                              (session_number,)).fetchall()
                selected_session_new = []
                for row in selected_session:   
                    name = row[0]
                    surname = row[1]
                    nameandsurname = name + ' ' + surname
                    selected_session_new.append(nameandsurname)
                result_string = ', '.join(selected_session_new)

                if result_string == '':
                    sg.popup('This session is empty since no one is registered!')
                else:
                    sg.popup(result_string)
                while True:
                    event_details, _ = window_details.read()
                    if event_details == sg.WIN_CLOSED or event_details == 'Return To Main':
                        window_details.close()
                        break
    
    con.commit()

def button_browse_pt_sessions(): # SENARYO 2

    window_browse = window_browse_pt_sessions()
    while True:
        event, values = window_browse.read()

        if event == sg.WIN_CLOSED or event == 'Return To Main':
            window_browse.close()
            break
        elif event == 'View Details':
            # Check if session_list is not empty before accessing its elements
            if values['pt_session_list']:
                selected_session_index = values['pt_session_list'][0]
                selected_session = list(cur.execute('SELECT * FROM PT_SESSION S, User U, Trainer T WHERE S.TrainerID = U.UserID AND T.TrainerID = S.TrainerID AND S.PT_SessionNumber = ?',
                                              (selected_session_index,)).fetchone())
                day = selected_session[1]
                time_interval = selected_session[2] + ' - ' + selected_session[3]
                gender = selected_session[8]
                hourlyfee = selected_session[12]
                shown = f'{day} {time_interval} trained by {selected_session[6]} ({gender}) in which the session cost is {hourlyfee}.'

                #selected_session_dict = dict(zip([desc[0] for desc in cur.description], shown))
                window_details = window_session_details(shown)
                while True:
                    event_details, _ = window_details.read()
                    if event_details == sg.WIN_CLOSED or event_details == 'Return To Main':
                        window_details.close()
                        break
        elif event == 'Make Reservation':
            # Check if session_list is not empty before accessing its elements

            if values['pt_session_list']:
                selected_pt_session_index = values['pt_session_list'][0] # User selects this sessions.

                selected_pt_session_from_session_list = list(cur.execute('SELECT * FROM PT_SESSION P, Trainer T WHERE P.TrainerID = T.TrainerID AND P.PT_SessionNumber = ?',
                                              (selected_pt_session_index,)).fetchone())
                session_number = selected_pt_session_index
                hourly_fee = selected_pt_session_from_session_list[6]
                reservation_date = selected_pt_session_from_session_list[2]
                hour_diff = int(selected_pt_session_from_session_list[3][:2]) - int(selected_pt_session_from_session_list[2][:2]) 
                hour_to_minute = hour_diff * 60
                minute_diff = int(selected_pt_session_from_session_list[3][3:5]) - int(selected_pt_session_from_session_list[2][3:5]) 
                payment_amount = int(((hour_to_minute + minute_diff) / 60) * hourly_fee)
                day = selected_pt_session_from_session_list[1]
                window_browse2 = window_confirmation(payment_amount)
                
                while True:
                    event, values = window_browse2.read()

                    if event == sg.WIN_CLOSED or event == 'Return To Main':
                        window_browse2.close()
                        break
                    elif event == 'Confirm':
                        window_browse2.close()
                        button_make_pt_reservation(session_number, login_user_id, reservation_date, payment_amount, day)
                        
                        break  # Make sure this break is inside the 'Confirm' branch
    

    con.commit()

def button_trainer_schedule(): # SENARYO 2
    window_browse = window_trainer_schedule()
    while True:
        event, values = window_browse.read()

        if event == sg.WIN_CLOSED or event == 'Return To Main':
            window_browse.close()
            break
        if event == 'Update Your Hourly Fee':
            if values['hourly_fee']:
                hourly_fee = values['hourly_fee']

                if hourly_fee == '':
                    sg.popup('Please Enter Hourly Fee To Update!')
                else:
                    cur.execute(
                        'UPDATE Trainer SET HourlyFee = ? WHERE TrainerID = ?',
                        (hourly_fee, login_user_id))
                    sg.popup(f'Your Hourly Fee has been updated to {hourly_fee}TL')
                    con.commit()
        elif event == 'View Details':
            if values['pt_reservation_list']:
                selected_s = list(cur.execute('SELECT * FROM PT_SESSION S, User U , Trainer T WHERE S.TrainerID = U.UserID AND S.TrainerID = T.TrainerID AND S.TrainerID = ?',
                                              (login_user_id,)).fetchall())
                print(selected_s)
                day = selected_s[0][1]
                time_interval = selected_s[0][2] + ' - ' + selected_s[0][3]
                gender = selected_s[0][8]
                hourlyfee = selected_s[0][12]
                shown = f'{day} {time_interval} trained by {selected_s[0][6]} ({gender}) in which the session cost is {hourlyfee}.'
                window_details = window_session_details(shown)

                select_query = """
SELECT U.Name, U.Surname
FROM PT_RESERVATION R
JOIN PT_SESSION S ON R.PT_SessionNumber = S.PT_SessionNumber
JOIN User U ON R.MemberID = U.UserID
WHERE R.PT_SessionNumber = ?;
"""
                session_number = values['pt_reservation_list'][0]
                print(session_number)

                selected_session = cur.execute(select_query, (session_number,)).fetchall()
                selected_session_new = []
                for row in selected_session:
                    name = row[0]
                    surname = row[1]
                    nameandsurname = name + ' ' + surname
                    selected_session_new.append(nameandsurname)
                result_string = ', '.join(selected_session_new)

                if result_string == '':
                    sg.popup('This session is empty since no one is registered!')
                else:
                    sg.popup(result_string)
                while True:
                    event_details, _ = window_details.read()
                    if event_details == sg.WIN_CLOSED or event_details == 'Return To Main':
                        window_details.close()
                        break
    con.commit()

def check_capacity(studio_number): # BU NE AMK BUNU NE ARA YAZDIM CHECK ET BIR DAHA
    cur.execute('SELECT Capacity FROM Studio WHERE StudioNumber = ?', (studio_number,))
    capacity = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM Reservation R, Session S WHERE R.SessionNumber = S.SessionNumber AND S.StudioNumber = ? GROUP BY R.SessionNumber',
                (studio_number,))
    reservations_count = cur.fetchone()[0]
    return reservations_count < capacity 

    con.commit()

def button_make_reservation(session_number, login_user_id, reservation_date, day):  # SENARYO 1

    make_reservation(session_number, login_user_id, reservation_date, day)
    '''
    existing_reservation_list = []
    cur.execute('SELECT * FROM Reservation WHERE SessionNumber = ? AND MemberID = ? AND Reservation_Date = ?',
                (session_number, login_user_id, reservation_date))
    existing_reservation = cur.fetchone()
    existing_reservation_list.append(existing_reservation)

    
    if existing_reservation:
        sg.popup('You have already made a reservation for this session on the selected date.')
    '''

    con.commit()

def button_make_pt_reservation(session_number, login_user_id, reservation_date, payment_amount, day): # SENARYO 2

    existing_reservation_list = []
    cur.execute('SELECT * FROM PT_RESERVATION WHERE PT_SessionNumber = ? AND MemberID = ? AND Reservation_Date = ?',
                (session_number, login_user_id, reservation_date))
    existing_reservation = cur.fetchone()
    existing_reservation_list.append(existing_reservation)


    if existing_reservation:
        sg.popup('You have already made a reservation for this session on the selected date.')
    else:
        # Attempt to make a reservation
        make_pt_reservation(session_number, login_user_id, reservation_date, payment_amount, day)


    con.commit()

def button_edit_your_info(): # SENARYO 3

    window_browse = window_browse_member_info()
    while True:
        event, values = window_browse.read()

        if event == sg.WIN_CLOSED or event == 'Return To Main':
            window_browse.close()
            break
        elif event == 'Edit Your Information':
            age = values['age']
            height = values['height']
            weight = values['weight']
            
            if age == '' or height == '' or weight == '':
                sg.popup('All Physical Attributes must be filled.')
            else:
                cur.execute(
                        'UPDATE Member SET Age = ?, Height = ?, Weight = ? WHERE MemberID = ?',
                        (age, height, weight, login_user_id))
                con.commit()
                sg.popup('Your changes is approved!')

def button_browse_sessions_member_handler(): # SENARYO 3

    window_browse = window_browse_member_session()
    while True:
        event, values = window_browse.read()

        if event == sg.WIN_CLOSED or event == 'Return To Main':
            window_browse.close()
            break
        elif event == 'View Details':

            if values['reservation_list']:
                selected_session_number_index = values['reservation_list'][0]
                selected_session = list(cur.execute('SELECT * FROM Session S, Reservation R WHERE S.SessionNumber = R.SessionNumber AND S.SessionNumber = ?',
                                              (selected_session_number_index,)).fetchone())

                day = selected_session[1]
                time_interval = selected_session[2] + ' - ' + selected_session[3]
                shown = f'Your Group Session will be on {day} between {time_interval}'
                window_details = window_session_details(shown)
                while True:
                    event_details, _ = window_details.read()
                    if event_details == sg.WIN_CLOSED or event_details == 'Return To Main':
                        window_details.close()
                        break
        elif event == 'Cancel Your Reservation':
            session_number_str = values['reservation_list'][0]

            cur.execute('SELECT * FROM Reservation Where SessionNumber = ? AND MemberID = ?', (session_number_str, login_user_id))
            pt_sessions = cur.fetchall()

            if pt_sessions is None:
                sg.popup('There is no Reservation assigned!')
            elif bool(pt_sessions) == False:
                sg.popup('Sorry! There is no such session!')
                break
            elif session_number_str == pt_sessions[0][0]:
                cur.execute('DELETE FROM Reservation WHERE SessionNumber = ? AND MemberID = ?', (session_number_str, login_user_id))
                sg.popup(f'{session_number_str}th PT Session has been DELETED!')


        con.commit()

def button_browse_pt_session_member_handler(): # SENARYO 3

    window_browse = window_browse_member_pt_session()
    while True:
        event, values = window_browse.read()

        if event == sg.WIN_CLOSED or event == 'Return To Main':
            window_browse.close()
            break
        elif event == 'View Details':

            if values['pt_reservation_list']:
                selected_session_number_index = values['pt_reservation_list'][0]
                selected_session = list(cur.execute('SELECT * FROM PT_SESSION S, PT_RESERVATION R WHERE S.PT_SessionNumber = R.PT_SessionNumber AND S.PT_SessionNumber = ?',
                                              (selected_session_number_index,)).fetchone())

                day = selected_session[1]
                time_interval = selected_session[2] + ' - ' + selected_session[3]
                shown = f'Your PT Session will be on {day} between {time_interval}'
                window_details = window_session_details(shown)
                while True:
                    event_details, _ = window_details.read()
                    if event_details == sg.WIN_CLOSED or event_details == 'Return To Main':
                        window_details.close()
                        break
        elif event == 'Cancel Your PT Reservation':
            session_number_str = values['pt_reservation_list'][0]

            cur.execute('SELECT * FROM PT_RESERVATION Where PT_SessionNumber = ? AND MemberID = ?', (session_number_str, login_user_id))
            pt_sessions = cur.fetchall()

            if pt_sessions is None:
                sg.popup('There is no Reservation assigned!')
            elif bool(pt_sessions) == False:
                sg.popup('Sorry! There is no such session!')
                break
            elif session_number_str == pt_sessions[0][0]:
                cur.execute('DELETE FROM PT_RESERVATION WHERE PT_SessionNumber = ?', (session_number_str, ))
                sg.popup(f'{session_number_str}th PT Session has been DELETED!')
                sg.popup(f'Re-payment will be done in 2-3 days.\nThanks for your patience') #{emoji.emojize(":smiling_face_with_smiling_eyes:")}
                con.commit()

def button_browse_pt_sessions_for_admin(): # GENEL
    window_browse = window_browse_pt_sessions_for_admin()
    while True:
        event, values = window_browse.read()

        if event == sg.WIN_CLOSED or event == 'Return To Main':
            window_browse.close()
            break
        elif event == 'View Details':
            # Check if session_list is not empty before accessing its elements
            if values['pt_session_list']:
                selected_session_index = values['pt_session_list'][0]
                selected_session = list(cur.execute('SELECT * FROM PT_SESSION S, User U, Trainer T WHERE S.TrainerID = U.UserID AND T.TrainerID = S.TrainerID AND S.PT_SessionNumber = ?',
                                              (selected_session_index,)).fetchone())
                day = selected_session[1]
                time_interval = selected_session[2] + ' - ' + selected_session[3]
                gender = selected_session[8]
                hourlyfee = selected_session[12]
                shown = f'{day} {time_interval} trained by {selected_session[6]} ({gender}) in which the session cost is {hourlyfee}.'

                window_details = window_session_details(shown)
                while True:
                    event_details, _ = window_details.read()
                    if event_details == sg.WIN_CLOSED or event_details == 'Return To Main':
                        window_details.close()
                        break
                select_query = """
SELECT U.Name, U.Surname
FROM PT_RESERVATION R
JOIN PT_SESSION S ON R.PT_SessionNumber = S.PT_SessionNumber
JOIN User U ON R.MemberID = U.UserID
WHERE R.PT_SessionNumber = ?;
"""
                session_number = values['pt_session_list'][0]
                print(session_number)

                selected_session = cur.execute(select_query,
                                              (session_number,)).fetchall()
                selected_session_new = []
                for row in selected_session:   
                    name = row[0]
                    surname = row[1]
                    nameandsurname = name + ' ' + surname
                    selected_session_new.append(nameandsurname)
                result_string = ', '.join(selected_session_new)

                if result_string == '':
                    sg.popup('This session is empty since no one is registered!')
                else:
                    sg.popup(result_string)
                while True:
                    event_details, _ = window_details.read()
                    if event_details == sg.WIN_CLOSED or event_details == 'Return To Main':
                        window_details.close()
                        break

window = window_login()

while True:

    event, values = window.read()

    if event == 'Login':
        button_login(values)
    elif event == 'Create New Group Session':
        window.close()
        window = window_create_group_session()
    elif event == 'Create Session':
        if True:
            button_create_session(values)
    elif event == 'Browse Sessions':
        button_browse_sessions_handler()
    elif event == 'See Your Group Sessions':
        button_browse_sessions_trainer_handler()
    elif event == 'See Your Group Session':
        button_browse_sessions_member_handler()
    elif event == 'Browse PT Sessions':
        button_browse_pt_sessions()
    elif event == 'Edit Your Information':
        button_edit_your_info()
    elif event == 'Browse PT Session':
        button_browse_pt_sessions_for_admin()
    elif event == 'Update Your Hourly Fee':
        button_edit_your_info()
    elif event == 'See Your PT Session':
        button_browse_pt_session_member_handler()
    elif event == 'See Your PT Sessions':
        button_trainer_schedule()
    elif event == 'Arrange PT Session':
        window.close()
        window = window_create_pt_session()
    elif event == 'Create PT Session':
        if True:
            button_create_pt_session(values)
    elif event == 'Delete Your PT Session':
        if True:
            button_delete_pt_session(values)
    elif event == 'Edit Your PT Session':
        if True:
            button_edit_pt_session(values)
    elif event == 'Return To Main':
        window.close()
        if login_user_type == 'Admin':
            window = window_admin()
        elif login_user_type == 'Member':
            window = window_member()
        elif login_user_type == 'Trainer':
            window = window_trainer()
    elif event == 'Logout':
        window.close()
        window = window_login()
    elif event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'reservation_date':
        # Handle the event for reservation date
        pass

window.close()
con.commit()
con.close()

