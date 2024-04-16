set -euo pipefail

FFMPEG=/mnt/c/ffmpeg-3.2.4-win64-static/bin/ffmpeg.exe

ls \
  -cr1 *F.MP4 | sort -V \
  | awk '{print "file \047" $1 "\047"}' > tmp-list.txt




$FFMPEG \
  -f concat \
  -i tmp-list.txt \
  -an \
  -c copy \
  -r 3 \
  tmp-1.mp4

$FFMPEG \
  -f concat \
  -i tmp-list.txt \
  -an -filter:v \
    "setpts=0.001*PTS , fps=30, crop=3840:1646:0:0 , scale=w=3440:h=1440" \
  out.mp4

