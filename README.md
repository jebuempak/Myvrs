- 파일 복사
cp com.galaxy.handTracking.plist ~/Library/LaunchAgents/com.galaxy.handTracking.plist

- 데몬 실행
launchctl load -w ~/Library/LaunchAgents/com.galaxy.handTracking.plist

-데몬 중지
launchctl unload -w ~/Library/LaunchAgents/com.galaxy.handTracking.plist# Myvrs
