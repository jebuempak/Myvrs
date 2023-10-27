import multiprocessing
from handTracking import main as handTracking_main
from humanBGRemove import main as humanBGRemove_main

def run_handTracking():
	handTracking_main()

def run_humanBGRemove():
	humanBGRemove_main()

if __name__ == '__main__':
	# multiprocessing 프로세스 생성
	p1 = multiprocessing.Process(target=run_handTracking)
	p2 = multiprocessing.Process(target=run_humanBGRemove)

	# 프로세스를 daemon으로 설정
	p1.daemon = True
	p2.daemon = True

	# 프로세스 시작
	p1.start()
	p2.start()

	# 무한 루프를 사용하여 메인 스레드가 종료되지 않게 합니다.
	# 이렇게 하면 데몬 프로세스가 계속 실행될 수 있습니다.
	try:
		while True:
			pass
	except KeyboardInterrupt:
		print("Main process terminated. Daemon processes will also be terminated.")

