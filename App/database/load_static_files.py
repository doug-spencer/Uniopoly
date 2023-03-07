from App.database.tables import Property, Utilities, Bus_stop, Email, Student_union
from App.main import db

def load_static_files():
    with open('App/database/db_static_files.txt') as file:
        lines = [i for i in file.readlines()]
        index = 0
        current_line = lines[index]

        #Properties
        while current_line != '\n':
            details = current_line.split(';')
            print(details)
            db.session.add(Property(
                name=details[0],
                colour=details[1],
                photo=details[2],
                position=int(details[3]),
                buy_price=int(details[4]),
                morgage_value=int(details[5]),
                rents=details[6][0:len(details[6]) - 1]
                ))
            index += 1
            current_line = lines[index]
            print(index,current_line)
        index += 1
        current_line = lines[index]

        #Utilites
        while current_line != '\n':
            details = current_line.split(';')
            print(details)
            db.session.add(Utilities(
                name=details[0],
                text=details[1],
                photo=details[2],
                position=int(details[3]),
                buy_price=int(details[4]),
                morgage_value=int(details[5][0:len(details[5]) - 1])
                ))
            index += 1
            current_line = lines[index]
            print(index,current_line)
        index += 1
        current_line = lines[index]   
        
        #Bus stop     
        while current_line != '\n':
            details = current_line.split(';')
            print(details)
            db.session.add(Bus_stop(
                name=details[0],
                photo=details[1],
                position=int(details[2]),
                buy_price=int(details[3]),
                morgage_value=int(details[4][0:len(details[4]) - 1])
                ))
            index += 1
            current_line = lines[index]
            print(index,current_line)
        index += 1
        current_line = lines[index]
        
        #Student union
        while current_line != '\n':
            details = current_line.split(';')
            print(details)
            db.session.add(Student_union(
                text=details[0],
                amount=int(details[1]),
                save_for_later=bool(details[2][0:len(details[2]) - 1])
                ))
            index += 1
            current_line = lines[index]
            print(index,current_line)
        index += 1
        current_line = lines[index] 

        #Email       
        while current_line != '\n':
            details = current_line.split(';')
            print(details)
            db.session.add(Email(
                text=details[0],
                amount=int(details[1]),
                save_for_later=bool(details[2][0:len(details[2]) - 1])
                ))
            try:
                index += 1
                current_line = lines[index]
            except:
                current_line = '\n'
            print(index,current_line)
    db.session.commit()
