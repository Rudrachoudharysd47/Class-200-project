import socket 
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = "127.0.0.1"
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
answer = []
print("Server has Started....")

def get_random_question_answer(conn):
    random_index = random.randint(0, len(questions) -1)
    random_question = questions[random_index]
    random_answer = answer[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answer.pop(index)


def clientthread(conn, addr):
    conn.send("Welcome to this quiz game".encode('utf-8'))
    conn.send("you will recive a question. you have to write oneline answer about that".encode('utf-8'))
    conn.send("Good Luck/n/n".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo ! Your Score is {score}/n/n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue


questions = [
    "1.Which of the following countries has a record of high participation of women in the political sphere of the society?",
    "2.On an average an Indian woman works…………..more than an average man every day.",
    "3.………………… provides that equal wages should be paid to equal work.",
    "4.In local self-government institutions, at least one third of all positions are reserved for?",
    "5.What portion of deposits is essential for the banks to maintain in liquid cash for their day to day transaction?",
    "6.The exchange of goods for goods is a process of ………………",
    "7.Which is not a modern form of money?",
    "8.Why do banks keep a small proportion of the deposits as cash with themselves?"
    "--WRITE SHORT/ONELINE ANSWER--"
]


def brodcast(message , connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)



while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print (addr[0] + " connected")
    new_thread = Thread(target= clientthread,args=(conn,addr))
    new_thread.start()

