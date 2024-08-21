

run:
	python birbs.py


install:
	python -m pip install -r requirements.txt






IN_USB=-f video4linux2 -i /dev/video0
IN_IP=-i 'rtsp://10.87.1.29:8554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp'
OUT1=[f=segment:segment_atclocktime=1:segment_time=60:reset_timestamps=1:strftime=1]/home/tom/mnt/desktop/media/Temp/birbs/birbs_%Y%m%d-%H%M.mp4
OUT2=[f=rtsp:rtsp_transport=tcp]rtsp://10.87.0.2:8554/birbs

stream:

	ffmpeg \
		$(IN_IP) \
		-an \
		-codec:v copy \
		-f segment -segment_atclocktime 1 -segment_time 60 -reset_timestamps 1 -strftime 1 \
				"/home/tom/mnt/desktop/media/Temp/birbs/%Y-%m-%d/birbs_%Y%m%d-%H%M.mp4" \
		-vf "scale=-1:720" -pix_fmt yuv420p \
		-c:v libx264 -profile:v baseline -preset veryfast \
		-crf 25 -maxrate:v 4M -bufsize:v 5M \
		-f tee -map 0:v -an \
		-f tee "$(OUT2)"

		# -b:v 1M -minrate:v 10k -maxrate:v 4M -bufsize:v 5M -bt:v 2000k \


.PHONY: stream


# .\FFmpeg\ffmpeg-7.0.1-full_build\bin\ffmpeg.exe -i 'rtsp://10.87.1.29:8554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp' -vf 'scale=-1:720' -pix_fmt yuv420p -c:v libx264 -profile:v baseline -preset veryfast  -an -f rtsp  'rtsp://10.87.0.2:8554/birbs2'







.PHONY: install birbs
