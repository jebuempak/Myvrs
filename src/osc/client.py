from pythonosc import udp_client

if __name__ == "__main__":
    # OSC 클라이언트를 설정합니다.
    client = udp_client.SimpleUDPClient("127.0.0.1", 8000)
    client.send_message("/greeting", "Hello OSC!",)
    client.send_message("/numbers", [1, 2, 3])
