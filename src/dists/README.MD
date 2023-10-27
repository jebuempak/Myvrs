0. 사전 설치
	- brew install cmake
1. python 3.11.6 설치
	- brew install python@3.11.6
	- Install_NDI_SDK_v5_Apple.pkg 설치
	- git clone https://github.com/buresu/ndi-python
	
	

2. venv 설정
2.1 venv directory 생성( 위치는 상관 없음)
	- venv 설치할 폴더 생성 ex) /Users/사용자/venvs
 
 2.2 가상화 생성
	- python3.11 -m venv /Users/venvs/scale
	- source /Users/venvs/scale/bin/activate

3. pip install
	- 가상화 실행
	source /Users/venvs/scale/bin/activate
	- pip upgreade
	pip install --upgrade pip
	- 라이브러리 설치
	- pip install pybind11
	pip install -r requiment.txt
	cmake -DNDI_DIE=

4. 소스 파일
- handTracking.py
- 손의 위치와 사용자의 얼굴을 감지해서 입장 여부 화인
- osc 주소는 127.0.0.1 port 8000
- 변경 시 소스에서 수정 해야함
ex) python handTracking.py

- humanBGRemove.py
인물 오려내서 NDI로 전송
ex) python humanBGRemove.py