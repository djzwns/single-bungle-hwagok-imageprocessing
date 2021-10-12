file = open("c:/windows/win.ini", "r")
copyfile = open("copy.txt", "w")

while True:
    read = file.readline()
    if read == '':
        break

    copyfile.write(read)

copyfile.close()
file.close()
