import socket

BUFFER_SIZE = 1024
def udp_connection(msg_query, ip , port):
    #opens the socket in kernal and use the ipv4 and upd proctocall here alterly we can ue the tcp socket.SOCK_STREAM , for ipv6 .AF_INET6
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip,port)
    #CONVERTS THE HEXT TO BYTES PASSING THE message with having the ip and port send to over n/w 
    client_socket.sendto(bytes.fromhex(msg_query), server_address)
    # will recive the date and convert back form byts to hex and close the sockt 
    response, server_address = client_socket.recvfrom(BUFFER_SIZE)
    response = response.hex()
    client_socket.close()
    return response