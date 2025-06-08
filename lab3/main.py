from subprocess import Popen
from sys import executable
from time import sleep

print("Тест начат")

server = Popen([executable, 'server.py'])
print("Сервер запущен", end='\n\n')

lab = Popen([executable, 'lab3.py'])
sleep(3)

server.kill()
lab.kill()
print("Тест завершен")