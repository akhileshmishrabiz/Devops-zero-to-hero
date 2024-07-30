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

  ## 🌐 Network Management 🌐

### Simple
- `ping hostname` - Check connectivity to a host.
- `curl http://example.com` - Make a web request.
- `wget http://example.com/file` - Download a file.
- `hostname` - Display or set the system hostname.
- `ifconfig` - Display network interface information.
- `ip a` - Display IP addresses and interfaces.
- `ip link set dev interface up/down` - Bring a network interface up or down.
- `netstat -rn` - Display routing table.
- `traceroute hostname` - Trace the route to a host.
- `nslookup hostname` - Query DNS records for a domain.

### Intermediate
- `dig domain` - Query DNS records.
- `arp -a` - Display the ARP table.
- `ss -tuln` - List listening ports and services.
- `ip route` - Show routing table.
- `ip addr add ip_address dev interface` - Add an IP address to an interface.
- `iptables -A INPUT -p tcp --dport 22 -j ACCEPT` - Allow SSH traffic.
- `iptables -L -v -n` - List detailed firewall rules.
- `ifup interface` - Bring an interface up.
- `ifdown interface` - Bring an interface down.
- `iwconfig` - Configure wireless interfaces.

### Advanced
- `tcpdump -i interface -w file.pcap` - Capture network traffic to a file.
- `tcpdump -nn -i interface 'port 80'` - Capture HTTP traffic.
- `nmap -sP 192.168.1.0/24` - Scan for live hosts on a network.
- `nmap -sV -p 1-65535 hostname` - Scan all ports and detect service versions.
- `ssh user@hostname` - Connect to a remote host via SSH.
- `scp user@host:/path/file /local/path` - Securely copy a file from a remote host.
- `scp /local/path/file user@host:/path` - Securely copy a file to a remote host.
- `rsync -avz source destination` - Synchronize files and directories.
- `ipset create setname hash:ip` - Create an IP set for firewall rules.
- `ipset add setname ip_address` - Add an IP to an IP set.

## 🔄 Process and System Management 🔄

### Simple
- `ps aux` - Display all running processes.
- `killall process_name` - Terminate all processes with the specified name.
- `bg` - Resume a suspended job in the background.
- `fg` - Bring a job to the foreground.
- `jobs` - List background jobs.
- `nohup command &` - Run a command immune to hangups.
- `who` - Show who is logged on.
- `last` - Show the last logins on the system.
- `w` - Show who is logged on and what they are doing.
- `su - user` - Switch to another user.

### Intermediate
- `kill -9 PID` - Forcefully terminate a process.
- `pkill process_name` - Send a signal to processes by name.
- `top` - Display real-time system stats.
- `htop` - Interactive process viewer.
- `free -m` - Display memory usage in megabytes.
- `df -h` - Show disk usage in human-readable format.
- `du -sh directory` - Show directory size.
- `uptime` - Show system uptime.
- `uname -r` - Display the kernel version.
- `vmstat` - Report virtual memory statistics.

### Advanced
- `dmesg | less` - View kernel ring buffer messages.
- `sysctl -a` - List all kernel parameters.
- `sysctl -w parameter=value` - Set a kernel parameter.
- `ulimit -a` - Show user limits.
- `strace -p PID` - Trace system calls and signals.
- `lsof -i` - List open files and the processes using them.
- `renice -n priority -p PID` - Change the priority of a running process.
- `at now + 5 minutes` - Schedule a command to run in 5 minutes.
- `crontab -l` - List cron jobs for the current user.
- `crontab -e` - Edit cron jobs for the current user.

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
- `grep -C 3 'pattern' filename` - Show 3 lines before and after matches.
- `find /path -iname 'filename'` - Case-insensitive file search.
- `find /path -type d -name 'dirname'` - Find directories by name.
- `awk '{sum += $1} END {print sum}' filename` - Sum the values in the first column.
- `awk 'length($0) > 80' filename` - Print lines longer than 80 characters.
- `sed 's/\<word\>/replacement/g' filename` - Replace whole words.
- `sed -i 's/old/new/g' filename` - Edit a file in-place.
- `cut -f1,3 filename` - Extract specific fields from a tab-delimited file.
- `cut -d, -f1-3 filename` - Extract fields from a CSV file.
- `sort -n filename` - Sort numerically.

## 🔒 Security and Permissions 🔒

### Simple
- `passwd` - Change user password.
- `chmod 755 filename` - Set file permissions.
- `chown user:group filename` - Change file owner and group.
- `umask 022` - Set default file permissions.
- `sudo command` - Execute a command as another user.
- `groups` - Show groups a user is a member of.
- `id` - Display user identity.
- `ssh-keygen` - Generate an SSH key pair.
- `ssh-copy-id user@host` - Install an SSH key on a remote server.
- `sudo -i` - Start a root shell session.

### Intermediate
- `visudo` - Edit the sudoers file safely.
- `sshd` - OpenSSH server daemon.
- `firewall-cmd --state` - Check the status of firewalld.
- `firewall-cmd --permanent --add-service=http` - Add a service to the firewall.
- `firewall-cmd --reload` - Reload firewalld configuration.
- `semanage fcontext` - Manage SELinux file contexts.
- `restorecon -v filename` - Restore SELinux context.
- `auditctl -l` - List audit rules.
- `ausearch -m avc` - Search audit logs for SELinux denials.
- `faillock` - Display the user login failure attempts.

### Advanced
- `setenforce 0` - Set SELinux to permissive mode.
- `setenforce 1` - Set SELinux to enforcing mode.
- `getenforce` - Display current SELinux mode.
- `iptables -A INPUT -p tcp --dport 22 -j ACCEPT` - Allow SSH.
- `iptables-save > /etc/iptables/rules.v4` - Save iptables rules.
- `modprobe module_name` - Load a kernel module.
- `rmmod module_name` - Remove a kernel module.
- `auditctl -w /etc/passwd -p wa` - Watch for changes to the passwd file.
- `fail2ban-client status` - Display Fail2ban status.
- `fail2ban-client set jail unbanip IP` - Unban an IP address.

