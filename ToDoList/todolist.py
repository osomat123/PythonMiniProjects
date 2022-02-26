from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
         7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

weekday = ['Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def today_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()

    if len(rows) == 0:
        print("Nothing to do!")
    else:
        print(f"Today {today.day} {month[today.month]}:")
        for i, row in enumerate(rows, 1):
            print(i, '. ', row, sep='')

def week_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline < (today.date() + timedelta(days=7))).order_by(
        Table.deadline).all()

    tasks = {}
    # Creating task dict from the rows received
    # Format tasks = {date1 : [t1, t2...], date2 : [t1,t2....]}
    for row in rows:
        if tasks.get(row.deadline) is None:
            tasks[row.deadline] = [row]
        else:
            tasks[row.deadline].append(row)

    # Printing tasks date wise
    cur_date = today
    while cur_date < (today + timedelta(days=7)):
        print(f"{weekday[cur_date.weekday()]} {cur_date.day} {month[cur_date.month]}:")

        if tasks.get(cur_date.date()) is None:
            print("Nothing to do!")
        else:
            for i, task in enumerate(tasks[cur_date.date()], 1):
                print(i, '. ', task, sep='')

        cur_date += timedelta(days=1)
        print()

def get_all_tasks():
    today = datetime.today()
    rows = session.query(Table).order_by(Table.deadline).all()
    return rows

def print_all_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline >= today.date()).order_by(Table.deadline).all()

    print("All tasks:")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row}. {row.deadline.day} {month[row.deadline.month]}")

def add_task():
    print("Enter task")
    new_task = input()
    print("Enter Deadline")
    task_deadline = datetime.strptime(input(), '%Y-%m-%d')
    new_row = Table(task=new_task, deadline=task_deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!")

def missed_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()

    if len(rows) == 0:
        print("Nothing is missed!")
        return

    print("Missed tasks:")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row}. {row.deadline.day} {month[row.deadline.month]}")

def delete_task():
    rows = get_all_tasks()

    if len(rows) == 0:
        print("Nothing to delete")
        return

    print("Choose the number of the task you want to delete:")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row}. {row.deadline.day} {month[row.deadline.month]}")

    to_delete = rows[int(input()) - 1] # getting the task to be deleted
    session.query(Table).filter(Table.id == to_delete.id).delete()
    session.commit()
    print("The task has been deleted!")

def first_page():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")

    choice = int(input())
    print()

    if choice == 1:
        today_tasks()
        print()

    elif choice == 2:
        week_tasks()

    elif choice == 3:
        print_all_tasks()
        print()

    elif choice == 4:
        missed_tasks()
        print()

    elif choice == 5:
        add_task()
        print()

    elif choice == 6:
        delete_task()
        print()

    else:
        print("Bye!")
        return 0

    return 1

page = 1
while True:
    if page == 1:
        page = first_page()

    if page == 0:
        break
