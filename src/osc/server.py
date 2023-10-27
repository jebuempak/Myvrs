from pythonosc import dispatcher
from pythonosc import osc_server

def default_handler(address, *args):
	print(f"Received message {address}: {args}")

if __name__ == "__main__":
	# 메시지를 처리할 함수를 등록합니다.
	disp = dispatcher.Dispatcher()
	disp.set_default_handler(default_handler)
	

	# OSC 서버를 시작합니다.
	server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 8000), disp)
	print("Serving on {}".format(server.server_address))
	server.serve_forever()
