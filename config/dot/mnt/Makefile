
VC = ~/bin/VeraCrypt/src/Main/veracrypt

mount.docs:
	mkdir -p ~/mnt/Docs
	sudo $(VC) --mount /dev/nvme1n1 ~/mnt/Docs --protect-hidden=no

unmount.docs:
	sudo $(VC) --dismount ~/mnt/Docs

MOUNTOPS = "username=Tom,uid=tom,gid=0,file_mode=0750,dir_mode=0750,soft,dirsync,sync"

mount.desktop:
	mkdir -p desktop
	mkdir -p desktop/docs
	mkdir -p desktop/media
	-sudo umount -lf desktop/docs
	-sudo umount -lf desktop/media
	sudo mount.cifs \\\\10.87.0.10\\\docs  desktop/docs  -o $(MOUNTOPS)
	sudo mount.cifs \\\\10.87.0.10\\\media desktop/media -o $(MOUNTOPS)

mount.desktop.local:
	mkdir -p desktop/docs
	mkdir -p desktop/media
	-sudo umount -lf desktop/docs
	-sudo umount -lf desktop/media
	sudo mount.cifs '\\10.87.1.10\docs'  desktop/docs  -o $(MOUNTOPS)
	sudo mount.cifs '\\10.87.1.10\media' desktop/media -o $(MOUNTOPS)


.PHONY: \
		mount.docs \
		unmount.docs \
		mount.desktop \
		rpizw.mount.desktop
