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

def load_game_board():
    def generate_board():
        body = '    <div id="center">emails</div>\n'
        for j in range(4):
            body += f'    <!--Row {j}-->\n'
            body += f'    <div class="row" id="row-{j}">\n'
            for i in range(10):
                id = j * 10 + i
                body += f'        <div class="tile">\n'
                if i > 0:
                    body += f'            <div class="tile-color"></div>\n'
                    body += f'            <div class="tile-name">Tile {id}</div>\n'
                    body += f'            <div class="tile-price">Price {id}</div>\n'
                else:
                    body += f'            <div class="tile-name">Tile {id}</div>\n'
                body += f'            <div class="player" id="tile{id}"></div>\n'
                body += f'        </div>\n'
            body += '    </div>\n\n'
        return body

    body = ""
    with open('App/templates/game_room.html') as file:
        generating = False
        for line in file:
            if not generating:
                body += line
            if line == '<div id="board">\n':
                generating = True
            elif line == '</div><!--END-->\n':
                generating = False
                body += generate_board() + '</div><!--END-->\n'
    
    with open('App/templates/game_room.html', 'w') as file:
        file.write(body)