- `ls` - List files and directories.
- `cd directory_name` - Change directory.
- `touch filename` - Create a empty file.
- `mkdir directory_name` - Create a directory.
- `rm filename` - Remove a file.
- `rm -r directory_name` - Remove a directory.
- `cp source destination` - Copy files.
- `mv source destination` - Move or rename files.
- `cat filename` - Display file content.
- `cat file1 file2 > combined_file` - Concatenate files.
- `less filename` - View file content with pagination.
- `head -n N filename` - Display the first N lines of a file.
- `tail -n N filename` - Display the last N lines of a file.


- `ln -s target link_name` - Create a symbolic link.
- `chown user:group filename` - Change file owner and group.
- `chmod 755 filename` - Set file permissions.
- `umask 022` - Set default file permissions.
- `passwd` - Change user password.
- `locate filename` - Quickly find file paths.
- `sort filename` - Sort file contents.
- `uniq filename` - Remove duplicate lines.
- `wc -l filename` - Count lines in a file.
- `crontab -l` - List cron jobs for the current user.
- `crontab -e` - Edit cron jobs for the current user.
- `shutdown -h now` - Shut down the system immediately.
- `reboot` - Reboot the system.



- `find /path -name filename` - Find files by name.
- `find /path -type d -name 'dirname'` - Find directories by name.
- `find /path -type f -size +100M` - Find files larger than 100MB.
- `find /path -exec command {} \;` - Execute a command on found files.
- `find /path -mtime -1` - Find files modified in the last 24 hours.
- `find /path -perm 644` - Find files with specific permissions (644 in this case).
- `find /path -type f -empty` - Find empty files.
- `find /path -type d -empty `- Find empty directories.
- `find /path -type f -user username` - Find files owned by a specific user.
- `find /path -name "*.txt" -delete` - Find and delete all .txt files.


- `grep 'pattern' filename` - Search for a pattern in a file.
- `grep -r 'pattern' directory` - Recursively search for a pattern in a directory.
- `grep -i 'pattern' filename` - Case-insensitive search.
- `grep -v 'pattern' filename` - Invert match (exclude pattern).
- `grep -l 'pattern' directory/*` - List files containing the pattern.
- `grep -c 'pattern' filename` - Count occurrences of a pattern in a file.
- `grep -n 'pattern' filename` - Show line numbers for matching lines.
- `grep -E 'pattern1|pattern2' filename` - Search for multiple patterns.
- `grep -A 3 'pattern' filename` - Show 3 lines after matches.
- `grep -B 3 'pattern' filename` - Show 3 lines before matches.


- `awk '{print $1}' filename` - Print the first column.
- `awk -F: '{print $1}' /etc/passwd` - Print the first field using ':' as delimiter.
- `awk '/pattern/ {print $0}' filename` - Print lines matching a pattern.
- `awk '{sum += $1} END {print sum}' filename` - Sum the values in the first column.
- `awk 'length($0) > 80' filename` - Print lines longer than 80 characters.
- `awk '{print $1, $2}' filename` - Print multiple columns.
- `awk 'NR%2==0' filename` - Print every second line.
- `sed 's/old/new/g' filename` - Replace text in a file.
- `sed -n '5,10p' filename` - Print lines 5 to 10.
- `cut -d: -f1 /etc/passwd` - Extract the first field from /etc/passwd.
- `cut -c1-5 filename` - Extract characters 1 to 5.

- `ping hostname` - Check connectivity to a host.
- `nslookup hostname` - Query DNS records for a domain.
- `curl http://example.com` - Make a web request.
- `netstat -tuln` - Display listening ports and services.
- `netstat -rn` - Display routing table.
- `ifconfig` - Display network interface information.
- `ip a` - Display IP addresses and interfaces.
- `traceroute hostname` - Trace the route to a host.
- `tcpdump -i interface` - Capture network traffic.
- `tcpdump -i interface -w file.pcap` - Capture network traffic to a file.
- `tcpdump -nn -i interface 'port 80'` - Capture HTTP traffic.
- `strace -p PID` - Trace system calls and signals.



- `service service_name status/start/stop/restart` - Start, stop, or restart a service.
- `systemctl status/start/stop/restart service_name ` - Start, stop, or restart a systemd service.
- `sftp user@host` - Securely transfer files over SSH.
- `ssh user@hostname` - Connect to a remote host via SSH.
- `scp user@host:/path/file /local/path` - Securely copy a file from a remote host.
- `scp /local/path/file user@host:/path` - Securely copy a file to a remote host.
- `wget http://example.com/file` - Download a file.
- `hostname` - Display or set the system hostname.
- `rsync -avz source destination` - Synchronize files and directories.
- `vmstat` - Report virtual memory statistics.
- `iostat` - Display I/O statistics.



- `lsof | grep filename` - List open files and the processes using them.
- `lsof -i :port` - List open files and the processes using them on a specific port.
- `uname -a` - Display system information.
- `uptime` - Show system uptime.
- `du -sh directory` - Show the total size of a directory.
- `ulimit -a` - Show user limits.
- `free -h` - Display memory usage in human-readable format.
- `zip -r archive.zip directory` - Create a compressed archive.
- `unzip archive.zip` - Extract a compressed archive.
- `tar -cvf archive.tar directory` - Archive a directory.
- `tar -xvf archive.tar` - Extract an archive.
