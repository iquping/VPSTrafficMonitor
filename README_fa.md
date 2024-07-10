## VM Traffic Monitor

VPS ترافیک مانیتور

این اسکریپت ترافیک باقی مانده VPS در Vultr، DigitalOcean و Linode را نظارت می‌کند. اگر ترافیک باقی مانده صفر باشد، VM را خاموش کرده و از طریق تلگرام اعلان می‌فرستد.

ویژگی‌ها

- نظارت بر ترافیک VPS در Vultr، DigitalOcean و Linode.
- خاموش کردن VPS هنگامی که ترافیک تمام می‌شود.
- ارسال اعلان از طریق تلگرام.

تنظیمات

1. کلون کردن مخزن 
```sh
git clone https://github.com/yourusername/vm-traffic-monitor.git

cd vm-traffic-monitor
```

2. نصب وابستگی‌ها 
```sh
pip install requests pyyaml python-telegram-bot
```

3. پیکربندی config.yaml

4. افزودن مجوز اجرا به اسکریپت 
```sh
chmod +x check_traffic.py
```

5. تنظیم یک کرون جاب برای اجرای دوره‌ای اسکریپت 
```sh
crontab -e
```
 اضافه کردن خط زیر برای اجرای اسکریپت هر ساعت: 
 ```sh
0 * * * * /usr/bin/python3 /path/to/check_traffic.py >> /path/to/check_traffic.log 2>&1

```

## اجرای به عنوان یک دیمن (اختیاری)

برای اجرای اسکریپت به عنوان یک دیمن، می‌توانید از systemd در لینوکس استفاده کنید:

1. ایجاد یک فایل سرویس systemd 
```sh
sudo nano /etc/systemd/system/vm-traffic-monitor.service
```

2. افزودن محتوای زیر به فایل سرویس 
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

3. بارگذاری مجدد systemd و شروع سرویس 
```sh
sudo systemctl daemon-reload
sudo systemctl start vm-traffic-monitor
sudo systemctl enable vm-traffic-monitor
```