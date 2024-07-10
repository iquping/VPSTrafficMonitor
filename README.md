# VM Traffic Monitor

This script monitors the remaining traffic of VMs on Vultr, DigitalOcean, and Linode. If the remaining traffic is zero, it shuts down the VM and sends a notification via Telegram.

## Features

- Monitors VM traffic on Vultr, DigitalOcean, and Linode.
- Shuts down VM when traffic is depleted.
- Sends notification via Telegram.

## Setup

1. Clone the repository
```sh
git clone https://github.com/yourusername/vm-traffic-monitor.git

cd vm-traffic-monitor
```

2. Install dependencies
```sh
pip install requests pyyaml python-telegram-bot
```

3. Configure the config.yaml

4. Add execution permissions to the script
```sh
chmod +x check_traffic.py
```

5. Set up a cron job to run the script periodically
```sh
crontab -e
```
Add the following line to run the script every hour:
```sh
0 * * * * /usr/bin/python3 /path/to/check_traffic.py >> /path/to/check_traffic.log 2>&1

```

## Running as a Daemon(Optional)
To run the script as a daemon, you can use systemd on Linux:

1. Create a systemd service file
```sh
sudo nano /etc/systemd/system/vm-traffic-monitor.service
```
2. Add the following content to the service file
```ini
[Unit]
Description=VM Traffic Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/check_traffic.py
WorkingDirectory=/path/to
StandardOutput=file:/var/log/vm-traffic-monitor.log
StandardError=file:/var/log/vm-traffic-monitor.log
Restart=always

[Install]
WantedBy=multi-user.target

```
3. Reload systemd and start the service
```sh
sudo systemctl daemon-reload
sudo systemctl start vm-traffic-monitor
sudo systemctl enable vm-traffic-monitor
```
