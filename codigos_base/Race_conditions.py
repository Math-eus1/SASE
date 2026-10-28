#BLOCO 1 -> REGIÃO CRÍTICA E EXCLUSÃO MÚTUA
  # Soluciona com o Lock e põe Threads em espera
  # Evita que 2 TSs entrem em conflito

import queue # -: Módulo de filas que permite trocar dados e tarefas entre diferentes Threads de forma segura;
import threading  # -> Cria e gerencia Threads; Chamadas de I/O - Bounds
import socket

# Importações que criam e gerenciam programação concorrente

#Filas de senhas - Criação
normal_queue = queue.Queue()
priority_queue = queue.Queue()

counter_n = 1 # Contador da fila normal
counter_p = 1 # Contador da fila preferencial

HOST = '127.0.0.1'
PORT = 5000

lock_counters = threading.Lock() # A função Lock do módulo threading aplica o Lock nos contadores;

def generate_ticket(type_ticket):
    global counter_n
    global counter_p
    # Resgata as informações globais das variáveis counter enquanto variáveis locais

    with lock_counters: # O comando with serve para o fechamento da instrução de Lock 
        if type_ticket == 'N':
            ticket = f"N{counter_n}" #Aqui é pra ficar N1, N2, N3 ...
            counter_n += 1
            normal_queue.put(ticket) #Aqui adiciona na fila referente
        elif type_ticket == 'P':
            ticket = f"P{counter_p}" #P1, P2, P3 ...
            counter_p += 1
            priority_queue.put(ticket) #Aqui adiciona na fila referente
        else:
            return None
    return ticket #Destranca o Lock do comando with

def treat_client(connection, address):
    print(f"Client connected: {address}")

    try:
        while True: #pra deixar a conversa ativa enquanto tiver dados
            dados = connection.recv(1024) #recv vem de receive. Os 1024 referenciam a quantidade de bytes máximos de dados
            if not dados:
                break

            message = dados.decode("utf-8").strip() #Aqui  é pra decodificar a mensagem dos bytes em texto

            if message == 'Generate_N':
                ticket_generated = generate_ticket('N')
                answer = f"OK:{ticket_generated}" #Aqui ficaria OK:N1 por exemplo
            elif message == 'Generate_P':
                ticket_generated = generate_ticket('P') 
                answer = f"OK:{ticket_generated}" #Aqui ficaria OK:P1 por exemplo
            else:
                answer = f"Wrong command!"

            connection.sendall(answer.decode('utf-8')) #a conexão envia a mensagem oara o cliente em espera
    except ConnectionResetError:
        print(f"The client {address} closed the connection suddenly.")
    finally:
        connection.close()


