
VC = veracrypt

mount-truecrypt-docs:
	mkdir -p ~/mnt/Docs
	sudo $(VC) --mount ~/Docs.tc ~/mnt/Docs --protect-hidden=no

unmount-truecrypt-docs:
	sudo $(VC) --dismount ~/mnt/Docs


MOUNTOPS = "username=Tom,uid=tom,gid=0,file_mode=0750,dir_mode=0750,soft,dirsync,sync"

mount-laptop-lan:
	mkdir -p laptop/data
	-sudo umount -lf laptop/data
	sudo mount.cifs -vvvv '\\10.87.0.12\data'  laptop/data -o $(MOUNTOPS)

mount-laptop-wan:
	mkdir -p laptop/data
	-sudo umount -lf laptop/data
	sudo mount.cifs -vvvv '\\10.87.1.12\data'  laptop/data -o $(MOUNTOPS)


mount-truenas-lan:
	# home dir over NFS so that symlinks work
	mkdir -p truenas/tom_home
	-sudo umount -lf truenas/tom_home
	sudo mount.nfs -vvvv '10.87.1.5:/mnt/zp/tom/home' truenas/tom_home -o "nfsvers=4,soft,softreval,timeo=10,nconnect=5"

	# everything else over cifs because it can see recursive child zfs's
	mkdir -p truenas/tom
	-sudo umount -lf truenas/tom
	sudo mount.cifs -vvvv '\\10.87.1.5\tom' truenas/tom -o "username=tom,uid=tom,gid=0,file_mode=0750,dir_mode=0750,soft,dirsync,sync"

