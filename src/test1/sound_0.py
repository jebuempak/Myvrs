from pydub import AudioSegment
from pydub.generators import Sine

# 배경 소리 로드 (이 예에서는 dummy 데이터)
water_sound = AudioSegment.silent(duration=10000)  # 대신 실제 물소리 샘플로 대체 가능
bird_sound = AudioSegment.silent(duration=10000)   # 대신 실제 새소리 샘플로 대체 가능
wind_sound = AudioSegment.silent(duration=10000)   # 대신 실제 바람소리 샘플로 대체 가능

background = water_sound.overlay(bird_sound).overlay(wind_sound)

# 간단한 음악 코드 생성
base_freqs = {
    'C': 261.63,
    'G': 392.00,
    'Am': 440.00,  # A note as a representation
    'F': 349.23
}

chord_duration = 2000  # 2 seconds for each chord

chords = ['C', 'G', 'Am', 'F']

song = AudioSegment.empty()

for chord in chords:
    sine_wave = Sine(base_freqs[chord])
    chord_sound = sine_wave.to_audio_segment(duration=chord_duration)
    song += chord_sound

# 배경 소리와 음악 코드를 합침
final_track = background.overlay(song)

# 결과 재생 (이 부분은 OS와 환경에 따라 다를 수 있음)
final_track.export("final_output.mp3", format="mp3")
