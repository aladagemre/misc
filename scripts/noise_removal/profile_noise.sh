# In order to profile the noise, give the sample video with noise and number of first seconds to process.
# Below will profile a noise for first 4 seconds in the noise_sample.mp4 file.
# sh profile_noise.sh noise_sample.mp4 4

ffmpeg -i "$1" -sameq -an tmpvid.mp4
ffmpeg -i "$1" -sameq tmpaud.wav 
ffmpeg -i "$1" -vn -ss 00:00:00 -t 00:00:"$2" noiseaud.wav
sox noiseaud.wav -n noiseprof noise.prof
rm -f tmpvid.mp4 tmpaud.wav noiseaud.wav

