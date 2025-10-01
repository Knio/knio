


stream:
	sudo $(MTXDIR)/mediamtx mediamtx.yml


run:
	python3 birbs.py


install:
	python3 -m pip install -r requirements.txt


MTXDIR=/home/tom/bin/mediamtx
mediamtx-install:
	mkdir -p $(MTXDIR)
	cd $(MTXDIR); wget https://github.com/bluenviron/mediamtx/releases/download/v1.15.0/mediamtx_v1.15.0_linux_amd64.tar.gz
	cd $(MTXDIR); tar xvf mediamtx*.tar.gz


CAM1=rtsp://10.87.1.29:8554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp



# IN_USB=-f video4linux2 -i /dev/video0
IN_IP=-i 'rtsp://10.87.1.29:8554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp'
# OUT1=[f=segment:segment_atclocktime=1:segment_time=60:reset_timestamps=1:strftime=1]/home/tom/mnt/desktop/media/Temp/birbs/birbs_%Y%m%d-%H%M.mp4
OUT2=[f=rtsp:rtsp_transport=tcp]rtsp://10.87.7.1:8554/birbs

# FFMPEG=~/bin/ffmpeg/ffmpeg
# FFMPEG=ffmpeg
FFMPEG=/home/tom/bin/ffmpeg/ffmpeg
FFMPEG=/home/tom/bin/ffmpeg-prebuilt/ffmpeg

old-stream:
		$(FFMPEG) \
		$(IN_IP) \
		-an \
		-codec:v copy \
		-f segment -segment_atclocktime 1 -segment_time 60 -reset_timestamps 1 -strftime 1 \
				"/mnt/zp/tom/temp/birbs/%Y-%m-%d/birbs_%Y%m%d-%H%M.mp4" \
		-vf "scale=-1:720" -pix_fmt yuv420p \
		-c:v libx264 -profile:v baseline -preset fast \
		-crf 22 -maxrate:v 4M -bufsize:v 5M \
		-f tee -map 0:v -an \
		-f tee "$(OUT2)"

alley-day:
	curl 'http://10.87.1.128/setIRCutManual_DayNight' \
  -b 'DHLangCookie30=English; ipc_10.87.1.128_webLanguage=en_us; ipc_10.87.1.128_KeepScale=0; ipc_10.87.1.128_username=admin; ipc_10.87.1.128_password=E10ADC3949BA59ABBE56E057F20F883E' \
  --data-raw '<?xml version="1.0"?><soap:Envelope xmlns:soap="http://www.w3.org/2001/12/soap-envelope"><soap:Header>\u0009<userid>52851dbd7918bbae</userid>\u0009<passwd>a17faccd02661e4c</passwd></soap:Header><soap:Body>DayMode</soap:Body></soap:Envelope>' \
  --insecure

alley-night:
	curl 'http://10.87.1.128/setIRCutManual_DayNight' \
  -b 'DHLangCookie30=English; ipc_10.87.1.128_webLanguage=en_us; ipc_10.87.1.128_KeepScale=0; ipc_10.87.1.128_username=admin; ipc_10.87.1.128_password=E10ADC3949BA59ABBE56E057F20F883E' \
  --data-raw '<?xml version="1.0"?><soap:Envelope xmlns:soap="http://www.w3.org/2001/12/soap-envelope"><soap:Header>\u0009<userid>52851dbd7918bbae</userid>\u0009<passwd>a17faccd02661e4c</passwd></soap:Header><soap:Body>NightMode</soap:Body></soap:Envelope>' \
  --insecure
