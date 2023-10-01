

laptop:
	mkdir -p laptop
desktop:
	mkdir -p desktop
lab-rpizw:
	mkdir -p lab-rpizw
lab-sp6:
	mkdir -p lab-sp6


MOUNTOPS = "username=Tom,uid=tom,gid=0,file_mode=0750,dir_mode=0750,soft"

mount.desktop: desktop
	mkdir -p desktop/k
	mkdir -p desktop/f
	sudo mount.cifs \\\\10.87.0.10\\\docs desktop/k -o $(MOUNTOPS)
	sudo mount.cifs \\\\10.87.0.10\\\media desktop/f -o $(MOUNTOPS)


rpizw.mount.desktop: desktop
	mkdir -p desktop/k
	mkdir -p desktop/f
	sudo mount.cifs '\\10.87.1.10\docs' k -o $(MOUNTOPS)
	sudo mount.cifs '\\10.87.1.10\media' f -o $(MOUNTOPS)


.PHONY: laptop desktop lab-rpizw lab-sp6 rpizw.mount.desktop

