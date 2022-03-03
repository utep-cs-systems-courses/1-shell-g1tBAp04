import os, sys, re


def param(str):
#Takes orders, makes strings
    commandl = []
    for item in str.split():
        commandl.append(item)

    return commandl

def ch_dir(folder):

    try:
        os.chdir(folder)
    except FileNotFoundError:
        os.write(1,(f'file{folder}not found\n').encode())

def ffail():
    os.write((1,f'fork failed {os.getpid()}\n'.encode()))
    sys.exit(1)

def runtask(commandl): #process to run command
    for dir in re.split(':', os.environ['PATH']):
        program = f'{dir}/{commandl[0]}'
        try:
            os.execve(program,commandl,os.environ)
        except OSError:
            pass

def execomm(commandl): #Forks, making child do command
    spt = os.fork()

    if spt < 0:
        ffail()
    elif spt == 0:
        runtask(commandl)
    else:
        os.wait()

def reroute(commandl):
    #redirect stdout to files

    spt = os.fork() #make child

    if spt < 0:
        os.write(2,("fork fail,resetting %d\n" % spt).encode())
        sys.exit(1)

    elif spt == 0:

        args = [commandl[0], commandl[1]]

        os.close(1)  # redirect child's stdout
        os.open(commandl[3], os.O_CREAT | os.O_WRONLY);
        os.set_inheritable(1, True)

        runtask(args)

    else: #parent
        os.wait()




def main():

    while (True):
        primr = f'{os.getcwd()}$'
        str = input(primr)

        if (str == ''):
            main()
        elif (str == 'exit'):
            sys.exit(0)
        elif((str[0:2] == 'cd') and (len(str) > 2)):
            ch_dir(str[3:])
        elif ((len(str) == 2) and (str[0:2] == 'cd')):
            os.chdir(os.environ['HOME'])
        else:
            commandl = param(str)
            if (len(commandl) > 3 and commandl[2] == '>'):
                reroute(commandl)
            else:
                execomm(commandl)


main()