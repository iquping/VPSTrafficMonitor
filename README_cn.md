# VM Traffic Monitor

此脚本可以监控Vultr、DigitalOcean和Linode上的VPS剩余流量。如果剩余流量为零，它会关机VPS并通过Telegram发送通知。

功能

- 监控Vultr、DigitalOcean和Linode上的VPS流量。
- 流量耗尽时关闭VPS。
- 通过Telegram发送通知。

设置

1. 克隆仓库 
```sh
git clone https://github.com/yourusername/vm-traffic-monitor.git

cd vm-traffic-monitor
```

2. 安装依赖 
```sh
pip install requests pyyaml python-telegram-bot
```

3. 配置config.yaml

4. 添加脚本执行权限
```sh
chmod +x check_traffic.py
```

5. 设置定时任务定期运行脚本 
```sh
crontab -e
```
添加以下行以每小时运行一次脚本：
```sh
0 * * * * /usr/bin/python3 /path/to/check_traffic.py >> /path/to/check_traffic.log 2>&1

```

## 作为守护进程运行（可选）

要将脚本作为守护进程运行，可以在Linux上使用systemd：

1. 创建一个systemd服务文件 
```sh
sudo nano /etc/systemd/system/vm-traffic-monitor.service
```

2. 添加以下内容到服务文件 
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

3. 重新加载systemd并启动服务 
```sh
sudo systemctl daemon-reload
sudo systemctl start vm-traffic-monitor
sudo systemctl enable vm-traffic-monitor
```