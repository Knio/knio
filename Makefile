
mount.media:
	mkdir -p media
	sudo mount.cifs \\\\127.0.0.1\\MEDIA media -o "username=Tom Flanagan,uid=tom,gid=tom,file_mode=0750,dir_mode=0750,port=9001,soft"

mount.desktop:
	mkdir -p desktop
	sudo mount.cifs \\\\127.0.0.1\\\DOCS desktop -o "username=Tom Flanagan,uid=tom,gid=tom,file_mode=0750,dir_mode=0750,port=9001,soft"

mount.zenbook:
	mkdir -p zenbook
	sudo mount.cifs "\\\\127.0.0.1\\DOCS" zenbook -o "username=Tom Flanagan,uid=tom,gid=tom,file_mode=0750,dir_mode=0750,port=9002,soft"

mount.docs:
	veracrypt --mount /dev/nvme0n1 Docs --protect-hidden=no

unmount.docs:
	veracrypt --dismount Docs

