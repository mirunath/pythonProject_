import sqlite3
from datetime import datetime, timedelta
import questionary


# create database and tables
def get_db(name='main.db'):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
                      name TEXT NOT NULL,
                      description TEXT,
                      periodicity TEXT NOT NULL,
                      completion DATETIME,
                      due DATETIME NOT NULL,
                      streak INTEGER
                      )""")

    db.commit()


# create predefined habits for the user to try the program starting on 2023-02-01
def predefined(db):
    cur = db.cursor()
    predefined_list = [('Swim', 'Daily', 'health', '2023-02-01', '2023-02-02', 0),
                       ('Walk', 'Daily', 'health', '2023-02-01', '2023-02-02', 0),
                       ('Yoga', 'Weekly', 'mindfulness', '2023-02-01', '2023-02-08', 0),
                       ('Code', 'Daily', 'become better', '2023-02-01', '2023-02-02', 0),
                       ('Meditate', 'Weekly', 'mindfulness', '2023-02-01', '2023-02-08', 0)]
    cur.executemany("INSERT OR REPLACE INTO habit ('name', 'description', 'periodicity', 'completion', 'due', 'streak')"
                    "VALUES (?,?,?,?,?,?)", predefined_list)
    db.commit()


# the user can add in the db daily or weekly habits
def add_habit_daily(db):
    cur = db.cursor()
    name = questionary.text("What is the name of the habit?").ask()
    description = questionary.text("What is the description?").ask()
    completion = datetime.today().date()
    periodicity = "Daily"
    due = completion - timedelta(days=1)
    streak = 1
    cur.execute("INSERT INTO habit VALUES(?, ?, ?, ?, ?, ?)",
                (name, description, periodicity, completion, due, streak))
    db.commit()


def add_habit_weekly(db):
    cur = db.cursor()
    name = questionary.text("What is the name of the habit?").ask()
    description = questionary.text("What is the description?").ask()
    completion = datetime.today().date()
    periodicity = "Weekly"
    due = completion - timedelta(days=7)
    streak = 1
    cur.execute("INSERT INTO habit VALUES(?, ?, ?, ?, ?, ?)",
                (name, description, periodicity, completion, due, streak))
    db.commit()


def get_habit_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM habit WHERE name=?", (name,))
    return cur.fetchall()


# deletes the habit that the user wants
def delete_habit(db):
    cur = db.cursor()
    name = questionary.text("What habit do you want to delete? ").ask()
    existing_habit = get_habit_data(db, name)
    if existing_habit:
        cur.execute(f"DELETE FROM habit WHERE name = '{name}';")
        cur.fetchall()
        db.commit()
    else:
        print("\nNo such habit in database!\n")


# the user can check off the habit that he did
def check(db):
    cur = db.cursor()
    name = questionary.text("What is the name of the habit?").ask()
    twoday = datetime.today().date()
    tmdelta = timedelta(days=-1)
    yestday = twoday + tmdelta
    twomorrow = twoday + timedelta(days=1)
    cur.execute(
        'UPDATE habit SET streak = streak+? WHERE completion <=? AND name = ? AND due > ?',
        (1, twoday, name, yestday))

    cur.execute('UPDATE habit SET (completion)=(due) WHERE name = ? AND completion<? AND due > ?',
                (name, twomorrow, yestday))

    newstartdate = datetime.today().date()

    # for daily habits
    time_delta_d = timedelta(days=2)
    newduedate_d = newstartdate + time_delta_d
    cur.execute(
        'UPDATE habit SET due = ? WHERE due=due AND periodicity=="Daily" AND name = ? AND due > ?',
        (newduedate_d, name, yestday))

    # for weekly habits
    time_delta_w = timedelta(days=14)
    newduedate_w = newstartdate + time_delta_w
    cur.execute(
        'UPDATE habit SET due = ? WHERE due=due AND periodicity=="Weekly" AND name = ? AND due > ?',
        (newduedate_w, name, yestday))
    db.commit()


# the function that auto-resets the habits
def reset(db):
    cur = db.cursor()
    tmdelta = timedelta(days=-1)
    yestday = datetime.today().date() + tmdelta

    newstartdate = datetime.today().date()

    time_delta_daily = timedelta(days=1)
    newduedateday = newstartdate + time_delta_daily

    time_delta_week = timedelta(days=7)
    newduedateweek = newstartdate + time_delta_week

    # reset the streak to 0 if the user missed to do
    cur.execute('UPDATE habit SET streak=? WHERE streak=(streak) AND due <= ?', (0, yestday))

    # replace completion with today newstartdate (for daily or weekly habits)
    cur.execute('UPDATE habit SET completion=? WHERE completion=(completion) AND due <= ?',
                (newstartdate, yestday))
    # replace daily habits due date with newduedateday
    cur.execute('UPDATE habit SET due=? WHERE due=(due) AND periodicity=("Daily") AND due <= ?',
                (newduedateday, yestday))
    # replace weekly habits due date with newduedateweek
    cur.execute('UPDATE habit SET due=? WHERE due=(due) AND periodicity=("Weekly") AND due <= ?',
                (newduedateweek, yestday))

    db.commit()


# the user can see the habits from the db (all, only weekly or only daily habits):
def show_all(db):
    cur = db.cursor()
    cur.execute("SELECT * FROM habit")
    items = cur.fetchall()
    habits = []
    for item in items:
        habits.append(item[0])
    print(habits)
    return habits


def show_weekly_habits(db):
    cur = db.cursor()
    cur.execute(f"SELECT name FROM habit WHERE periodicity = 'Weekly'")
    items = cur.fetchall()
    habits = []
    for item in items:
        habits.append(item[0])
    print(habits)
    return habits


def show_daily_habits(db):
    cur = db.cursor()
    cur.execute(f"SELECT name FROM habit WHERE periodicity = 'Daily'")
    items = cur.fetchall()
    habits = []
    for item in items:
        habits.append(item[0])
    print(habits)
    return habits


# the user can see the due date until the next check for a specific habit
def habit_progress(db, name):
    cur = db.cursor()
    cur.execute("SELECT due FROM habit WHERE name=?", (name, ))
    progress = cur.fetchall()
    print(progress)
    return progress


# the user can see the streaks of habits
def maximum_given(db, name):
    cur = db.cursor()
    cur.execute("SELECT MAX(streak) FROM habit WHERE name=?", (name,))
    maxim = cur.fetchall()
    print(maxim)
    return maxim


# the user can see the maximum streak of all the daily habits
def maximum_daily(db):
    cur = db.cursor()
    cur.execute("SELECT MAX(streak) FROM habit WHERE periodicity='Daily'")
    maxim = cur.fetchall()
    print(maxim)
    return maxim


# the user can see the maximum streak of all the weekly habits
def maximum_weekly(db):
    cur = db.cursor()
    cur.execute("SELECT MAX(streak) FROM habit WHERE periodicity='Weekly'")
    maxim = cur.fetchall()
    print(maxim)
    return maxim
