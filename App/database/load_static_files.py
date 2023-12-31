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
        index += 1
        current_line = lines[index]

        #Utilites
        while current_line != '\n':
            details = current_line.split(';')
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
        index += 1
        current_line = lines[index]   
        
        #Bus stop     
        while current_line != '\n':
            details = current_line.split(';')
            db.session.add(Bus_stop(
                name=details[0],
                photo=details[1],
                position=int(details[2]),
                buy_price=int(details[3]),
                morgage_value=int(details[4][0:len(details[4]) - 1])
                ))
            index += 1
            current_line = lines[index]
        index += 1
        current_line = lines[index]
        
        #Student union
        while current_line != '\n':
            details = current_line.split(';')
            db.session.add(Student_union(
                text=details[0],
                amount=int(details[1]),
                go_to=int(details[2][0:len(details[2]) - 1])
                ))
            index += 1
            current_line = lines[index]
        index += 1
        current_line = lines[index] 

        #Email       
        while current_line != '\n':
            details = current_line.split(';')
            db.session.add(Email(
                text=details[0],
                amount=int(details[1]),
                go_to=int(details[2][0:len(details[2]) - 1])
                ))
            try:
                index += 1
                current_line = lines[index]
            except:
                current_line = '\n'
    db.session.commit()

def load_game_board():
    def get_database():
        data = {}
        with open('App/database/db_static_files.txt') as file:
            lines = file.readlines()
            breaks = 0
            for i in range(len(lines)):
                if lines[i] == '\n':
                    breaks += 1
                    continue
                if breaks == 3:
                    break
                line = lines[i].split(';')
                if breaks == 0:
                    #property
                    data[int(line[3])] = {'name': line[0], 'price': line[4], 'colour': line[1]}
                elif breaks == 1:
                    #utility
                    data[int(line[3])] = {'name': line[0], 'price': line[4], 'colour': None}
                else:
                    #bus stop
                    data[int(line[2])] = {'name': line[0], 'price': line[3], 'colour': None}
        return data

    def generate_board():
        data = get_database()
        corners = {0: 'Go', 1: 'Jail', 2: 'Free Parking', 3: 'Go to Jail'}
        body = '    <div id="center"></div>\n'
        for j in range(4):
            body += f'    <!--Row {j}-->\n'
            body += f'    <div class="row" id="row-{j}">\n'
            for i in range(10):
                id = j * 10 + i
                body += f'        <div class="tile">\n'
                if i == 0: 
                    #corner
                    body += f'            <div class="tile-name">{corners[j]}</div>\n'
                elif i == 5: 
                    #bus stop
                    o = 'h' if j % 2 == 0 else 'v'
                    body += f'            <div class="tile-name">{data[id]["name"]}</div>\n'
                    body += f'            <div class="bus-stop-image {o}-image"></div>\n'
                    body += f'            <div class="tile-price">{data[id]["price"]}</div>\n'
                elif id in [2, 12, 22, 33]: 
                    #su
                    body += f'            <div class="tile-name">SU</div>\n'
                elif id in [7, 17, 28, 36]:
                    #email
                    body += f'            <div class="tile-name">Email</div>\n'
                else: 
                    #property/utility
                    col = data[id]["colour"]
                    if col != None:
                        #property
                        body += f'            <div class="tile-color {col}"></div>\n'
                        body += f'            <div class="tile-name">{data[id]["name"]}</div>\n'
                    else:
                        #utility
                        body += f'            <div class="tile-name">{data[id]["name"]}</div>\n'
                        if id == 4:
                            pass
                        else:
                            body += f'            <div class="wine-bottle-image v-image"></div>\n'
                    body += f'            <div class="tile-price">{data[id]["price"]}</div>\n'
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