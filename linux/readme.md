# 🚀 Linux Command Essentials for DevOps 🚀

This document provides a categorized list of 100 commonly used Linux commands, organized by functionality and difficulty level. It is designed as a quick reference for DevOps professionals.

## 🔧 File Management 🔧

### Simple
- `ls` - List files and directories.
- `cd directory_name` - Change directory.
- `touch filename` - Create a file.
- `mkdir directory_name` - Create a directory.
- `rm filename` - Remove a file.
- `rm -r directory_name` - Remove a directory.
- `cp source destination` - Copy files.
- `mv source destination` - Move or rename files.
- `cat filename` - Display file content.
- `cat file1 file2 > combined_file` - Concatenate files.

### Intermediate
- `less filename` - View file content with pagination.
- `head -n N filename` - Display the first N lines of a file.
- `tail -n N filename` - Display the last N lines of a file.
- `ln -s target link_name` - Create a symbolic link.
- `chmod permissions filename` - Change file permissions.
- `chown user:group filename` - Change file owner and group.
- `find /path -name filename` - Search for files by name.
- `grep 'pattern' filename` - Search for a pattern in a file.
- `du -h` - Display disk usage in human-readable format.
- `df -h` - Display file system disk space usage.

### Advanced
- `rsync -av source destination` - Synchronize files and directories.
- `tar -cvf archive.tar directory` - Archive a directory.
- `tar -xvf archive.tar` - Extract an archive.
- `scp user@host:/path/to/file /local/path` - Secure copy a file from a remote host.
- `scp /local/path user@host:/path/to/destination` - Secure copy a file to a remote host.
- `sftp user@host` - Securely transfer files over SSH.
- `zip -r archive.zip directory` - Create a compressed archive.
- `unzip archive.zip` - Extract a compressed archive.
- `sed 's/old/new/g' filename` - Replace text in a file.
- `awk '{print $1}' filename` - Extract the first column from a file.

## 🛠️ System and Process Management 🛠️

### Simple
- `ps` - Display currently running processes.
- `top` - Display real-time system statistics.
- `kill PID` - Terminate a process by PID.
- `uname -a` - Display system information.
- `whoami` - Display the current user.
- `uptime` - Show system uptime.
- `date` - Display the current date and time.
- `hostname` - Display or set the system hostname.
- `shutdown -h now` - Shut down the system immediately.
- `reboot` - Reboot the system.

### Intermediate
- `htop` - Interactive process viewer.
- `nice -n 10 command` - Start a process with a specified priority.
- `renice -n 10 -p PID` - Change the priority of a running process.
- `df -i` - Show inode usage.
- `du -sh directory` - Show the total size of a directory.
- `free -h` - Display memory usage in human-readable format.
- `lsof -i :port` - List open files and the processes using them on a specific port.
- `netstat -tuln` - Display listening ports and services.
- `systemctl status service` - Show the status of a systemd service.
- `systemctl restart service` - Restart a systemd service.

### Advanced
- `strace -p PID` - Trace system calls and signals.
- `lsof | grep filename` - List open files and the processes using them.
- `vmstat` - Report virtual memory statistics.
- `iostat` - Display I/O statistics.
- `tcpdump -i interface` - Capture network traffic.
- `iptables -L` - List firewall rules.
- `ufw status` - Show the status of the Uncomplicated Firewall.
- `service service_name start/stop/restart` - Start, stop, or restart a service.
- `journalctl -xe` - View the systemd journal logs.
- `crontab -e` - Edit the crontab for scheduling tasks.

## 💾 Disk and Storage Management 💾

### Simple
- `mount /dev/device /mnt/point` - Mount a file system.
- `umount /mnt/point` - Unmount a file system.
- `lsblk` - List information about block devices.
- `fdisk -l` - Display disk partition information.
- `blkid` - Display block device attributes.
- `mkfs -t ext4 /dev/device` - Create an ext4 file system on a device.
- `df -Th` - Show disk space usage by file system type.
- `sync` - Flush file system buffers.
- `eject /dev/cdrom` - Eject removable media.
- `file filename` - Determine the file type.

### Intermediate
- `parted /dev/device` - Partition a disk.
- `tune2fs -l /dev/device` - List the attributes of an ext4 file system.
- `e2fsck /dev/device` - Check and repair an ext4 file system.
- `resize2fs /dev/device` - Resize an ext4 file system.
- `mount -o loop image.iso /mnt/point` - Mount an ISO image.
- `xfs_info /mnt/point` - Display XFS file system information.
- `xfs_growfs /mnt/point` - Grow an XFS file system.
- `cryptsetup luksFormat /dev/device` - Set up LUKS encryption.
- `cryptsetup luksOpen /dev/device name` - Open a LUKS-encrypted device.
- `lvdisplay` - Display LVM logical volumes.

### Advanced
- `vgcreate volume_group /dev/device` - Create a volume group.
- `lvcreate -L 10G -n logical_volume volume_group` - Create a logical volume.
- `lvextend -L +5G /dev/volume_group/logical_volume` - Extend a logical volume.
- `lvreduce -L -5G /dev/volume_group/logical_volume` - Reduce a logical volume.
- `vgreduce volume_group /dev/device` - Remove a physical volume from a volume group.
- `mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sd[b-c]` - Create a RAID 1 array.
- `mdadm --detail /dev/md0` - Display RAID array details.
- `lvm2` - Use Logical Volume Manager 2.
- `btrfs filesystem show` - Show Btrfs file systems.
- `zfs list` - List ZFS file systems.

## 🔍 Search and Find 🔍

### Simple
- `find /path -name filename` - Find files by name.
- `locate filename` - Quickly find file paths.
- `grep 'pattern' filename` - Search for a pattern in a file.
- `grep -r 'pattern' directory` - Recursively search for a pattern in a directory.
- `grep -i 'pattern' filename` - Case-insensitive search.
- `grep -v 'pattern' filename` - Invert match (exclude pattern).
- `grep -l 'pattern' directory/*` - List files containing the pattern.
- `grep -c 'pattern' filename` - Count occurrences of a pattern in a file.
- `grep -n 'pattern' filename` - Show line numbers for matching lines.
- `find /path -type f -size +100M` - Find files larger than 100MB.

### Intermediate
- `awk '{print $1}' filename` - Print the first column.
- `awk -F: '{print $1}' /etc/passwd` - Print the first field using ':' as delimiter.
- `awk '/pattern/ {print $0}' filename` - Print lines matching a pattern.
- `sed 's/old/new/g' filename` - Replace text in a file.
- `sed -n '5,10p' filename` - Print lines 5 to 10.
- `cut -d: -f1 /etc/passwd` - Extract the first field from /etc/passwd.
- `cut -c1-5 filename` - Extract characters 1 to 5.
- `sort filename` - Sort file contents.
- `uniq filename` - Remove duplicate lines.
- `wc -l filename` - Count lines in a file.

### Advanced
- `xargs` - Build and execute command lines from input.
- `find /path -exec command {} \;` - Execute a command on found files.
- `find /path -mtime -1` - Find files modified in the last 24 hours.
- `grep -E 'pattern1|pattern2' filename` - Search for multiple patterns.
- `grep -A 3 'pattern' filename` - Show 3 lines after matches.
- `grep -B 3 'pattern' filename` - Show 3 lines before matches.
- `awk '{print $1, $2}' filename` - Print multiple columns.
- `awk 'NR%2==0' filename` - Print every second line.
- `sed '/pattern/d' filename` - Delete lines matching a pattern.
-
