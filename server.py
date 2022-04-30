import socket, pickle

# Socket
host, ip = "localhost", 5556
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, ip))
serversocket.listen(4)

# Socket data schema
data = {
    "points": {"player1": 0, "player2": 0, "player3": 0, "player4": 0},
    "paddle1_rect_y": 225,
    "paddle2_rect_y": 225,
    "paddle3_rect_x": 340,
    "paddle4_rect_x": 340,
    "winner_text": "",
    "game_over": False,
}
connection = []


def waiting_for_connections():
    while len(connection) < 4:
        conn, addr = serversocket.accept()
        connection.append(conn)


def receive_information():
    player_1_info = pickle.loads(connection[0].recv(1024))
    player_2_info = pickle.loads(connection[1].recv(1024))
    player_3_info = pickle.loads(connection[2].recv(1024))
    player_4_info = pickle.loads(connection[3].recv(1024))

    return player_1_info, player_2_info, player_3_info, player_4_info


while True:
    waiting_for_connections()

    data_arr = pickle.dumps(data)
    connection[0].send(data_arr)
    connection[1].send(data_arr)
    connection[2].send(data_arr)
    connection[3].send(data_arr)

    player1, player2, player3, player4 = receive_information()

    data = {**player1, **player2, **player3, **player4}
