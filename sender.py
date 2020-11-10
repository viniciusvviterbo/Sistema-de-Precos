import socket
import argparse

parser = argparse.ArgumentParser(description = 'Simples implementação do jogo Batalha Naval.')
parser.add_argument('-i', action = 'store', dest = 'host', default = '127.0.1.1', required = False, help = 'Endereço IP do servidor.')
parser.add_argument('-p', action = 'store', dest = 'porta', default = 9999, required = False, help = 'Porta a ser usada pelo servidor.')

arguments = parser.parse_args()
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = arguments.host
porta = int(arguments.porta)
buffer_size = 1024
mensagem_envio = 'D&1&2&3&4&5' 
soc.sendto(str.encode(mensagem_envio), (host, porta))
mensagem_recebida = soc.recvfrom(buffer_size)
print('\n' + mensagem_recebida[0].decode())    