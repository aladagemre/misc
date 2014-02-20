# Following script will remove noise from first parameter and write the video without noise into the second parameter.
# will use noise.prof in the same folder for eliminating the noise.
# sh clear_noise.sh noisy_full_video.mp4 noiseless_full_video.mp4

ffmpeg -i "$1" -sameq -an tmpvid.mp4
ffmpeg -i "$1" -sameq tmpaud.wav
sox tmpaud.wav tmpaud-clean.wav noisered noise.prof 0.21
ffmpeg -i tmpaud-clean.wav -i tmpvid.mp4 -sameq "$2"
rm -f tmpvid.mp4 tmpaud.wav tmpaud-clean.wav
