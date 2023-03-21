import os

def openFolder(folder):
    lines = 0
    item_list = os.listdir(folder)
    for item in item_list:
        if item == '__pycache__': continue
        newDir = folder + '/' + item
        if '.' not in item:
            #folder
            lines += openFolder(newDir)
        else:
            #file
            if '.js' in item or '.py' in item or '.html' in item or '.css' in item:
                numLines = len(open(newDir, 'r').readlines())
                lines += numLines
                print(newDir, lines)
    return lines

print('total lines:', openFolder('App/'))