# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nothing to do!')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.commit()


while True:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Add task")
    print("0) Exit")
    i = int(input('> '))
    print()
    today = datetime.today()
    rows = session.query(Table).order_by(Table.deadline).all()
    if i == 1:
        print('Today:', today.day, today.strftime('%b'))

        j = 1
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for row in rows:
                if row.deadline == today:
                    print(str(j) + '. ' + row.task)
                    j = j + 1
    elif i == 2:
        weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        the_day = today.weekday()
        printing = True
        day_printing = today.date()
        if the_day == 0:
            stop_day = 6
        else:
            stop_day = the_day - 1
        while printing:
            if day_printing.weekday() == stop_day:
                printing = False
            print(weekdays[day_printing.weekday()], day_printing.day, today.strftime('%b'))
            j = 1
            if len(rows) == 0:
                print('Nothing to do!')
            else:
                for row in rows:
                    if row.deadline == day_printing:
                        print(str(j) + '. ' + row.task)
                        j = j + 1
            day_printing = day_printing + timedelta(days=1)
            print()

    elif i == 3:
        j = 1
        print("All tasks:")
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for row in rows:
                print(str(j) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + row.deadline.strftime('%b'))
                j = j + 1
                
    elif i == 4:
        print('Enter task')
        tk = input('>')
        print("Enter deadline")
        ddl = input(">")
        new_row = Table(task=tk, deadline=datetime.strptime(ddl, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print('The task has been added!')
    elif i == 0:
        print('Bye!')
        break
    print()
