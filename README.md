DataHive Auto Farming Bot
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/mejri02/datahive-bot.svg)](https://github.com/mejri02/datahive-bot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/mejri02/datahive-bot.svg)](https://github.com/mejri02/datahive-bot/network)

## 🔗 Join DataHive & Get Bonus
**👉 Join DataHive with referral bonus:** [Join DataHive Now](https://datahive.ai?invite=vxrkrxr)

---

## 📌 Overview

**DataHive Auto Farming Bot** is an advanced Python automation tool designed to maximize your earnings on the DataHive platform. Run multiple accounts 24/7 with intelligent proxy rotation and anti-detection features.

## ✨ Features

### 🎯 **Multi-Account Management**
- ✅ Run unlimited accounts simultaneously
- ✅ Individual account monitoring
- ✅ Real-time point tracking
- ✅ Automatic session management

### 🛡️ **Anti-Detection System**
- ✅ Random User Agent per account
- ✅ Realistic browser headers
- ✅ Device ID synchronization
- ✅ Platform diversity (Windows/Mac/Linux)

### 🔄 **Smart Proxy Support**
- ✅ HTTP/HTTPS/SOCKS4/SOCKS5 proxies
- ✅ Automatic proxy rotation
- ✅ Free proxies from Proxyscrape
- ✅ Private proxy support
- ✅ Failed proxy blacklisting

### 📊 **Real-time Monitoring**
- ✅ Live point statistics
- ✅ Connection status indicators
- ✅ IP address verification
- ✅ Session performance analytics

### ⚡ **Automation**
- ✅ Auto-ping every 60 seconds
- ✅ Error recovery system
- ✅ 24/7 continuous operation
- ✅ Proxy failover mechanism

### 🎨 **User Interface**
- ✅ Color-coded console output
- ✅ Email privacy protection
- ✅ WIB timezone display
- ✅ Progress indicators

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/mejri02/datahive-bot.git
cd datahive-bot

2. Install required packages



pip install -r requirements.txt

3. Configure your accounts


4. Open accounts.txt


5. Add your DataHive bearer tokens (one per line)



How to get your token:

· Login to DataHive AI web app
· Open browser DevTools (F12)
· Go to Network tab
· Look for API requests to api.datahive.ai
· Copy the Bearer token from the Authorization header

Example accounts.txt:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

4. Configure proxies (Optional)


5. Open proxy.txt


6. Add your proxies (one per line)



Supported formats:

· http://ip:port
· https://ip:port
· socks4://ip:port
· socks5://ip:port
· ip:port (will default to http)

Example proxy.txt:

http://proxy1.com:8080
socks5://proxy2.com:1080
192.168.1.1:3128
103.10.63.120:8080


---

📖 Usage

Run the bot:

python bot.py

Bot Options:

When starting, you'll see these options:

1. Run With Free Proxyscrape Proxy
2. Run With Private Proxy
3. Run Without Proxy

What happens next:

1. Bot loads your accounts


2. Shows real-time status for each account


3. Auto-pings every 60 seconds


4. Displays earnings statistics


5. Runs 24/7 until stopped (Ctrl+C)




---

📁 File Structure

datahive-bot/
├── bot.py              # Main bot script
├── requirements.txt    # Python dependencies
├── README.md           # This documentation
├── .gitignore          # Git ignore file
├── accounts.txt        # Your tokens (add manually)
└── proxy.txt           # Proxy list (optional)


---

⚙️ Requirements

Create requirements.txt with:

requests>=2.31.0
pytz>=2023.3
colorama>=0.4.6


---

📊 Usage Example

$ python bot.py

DataHive Auto Farming BOT
Updated v0.2.5 (Auto Sync DeviceID + Random UA per Account)

Account's Total: 3
Proxies Loaded: 50 (HTTP: 30 | HTTPS: 15 | SOCKS4: 5)

[ Account: exa***ple@email.com - Proxy: http://proxy1.com:8080 - Status: 24h: 15.23 PTS - Total: 125.50 PTS ]
[ Account: us***ail.com - Proxy: socks5://proxy2.com:1080 - Status: PING Success ]
[ Account: te***com - Proxy: None - Status: IP Check: 192.168.1.100 ]

💰 Session #1 Summary:
   • Total Points: 450.75 PTS
   • 24h Points: 65.89 PTS
   • Avg per Account: 150.25 PTS
   • Pings: 3✓ 0✗


---

🔧 Advanced Configuration

Custom User Agents

Each account gets unique user agents:

· Chrome on Windows
· Firefox on Mac
· Edge on Windows
· Chrome on Linux

Proxy Rotation

Enable rotation when prompted:

Rotate Invalid Proxy? [y/n] -> y

Running Without Proxies

Choose option 3 for direct connection (not recommended for multiple accounts)


---

❓ FAQ

Q: How many accounts can I run?

A: As many as you want, but start with 3-5 to test stability.

Q: Do I need proxies?

A: For multiple accounts, YES. For single account, optional but recommended.

Q: How to get free proxies?

A: Choose option 1 - bot will download free proxies automatically.

Q: Is this safe?

A: Use responsibly. Don't overload the service.

Q: How often does it ping?

A: Every 60 seconds per account.


---

⚠️ Important Notes

1. Keep tokens secure - Never share accounts.txt


2. Use proxies for multiple accounts to avoid IP bans


3. Monitor regularly - Check logs for issues


4. Respect rate limits - Don't run too many accounts


5. Update regularly - Check for new versions




---

⚠️ Disclaimer

This bot is for educational purposes only. Use at your own risk.

· The bot is not affiliated with DataHive
· Follow DataHive's Terms of Service
· Don't overload the service
· Keep your tokens secure


---

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.


---

🤝 Contributing

Contributions are welcome!

1. Fork the repository


2. Create your feature branch (git checkout -b feature/AmazingFeature)


3. Commit your changes (git commit -m 'Add some AmazingFeature')


4. Push to the branch (git push origin feature/AmazingFeature)


5. Open a Pull Request




---

🔗 Important Links & Resources

🌐 DataHive Platform

· Join DataHive with bonus
· Official Website
· Dashboard

🐍 Python Resources

· Python Downloads
· Requests Library
· Pip Documentation

📚 Documentation

· This Bot Documentation
· GitHub Issues
· Discussions

🔧 Tools

· Proxy Testing
· User Agent List
· GitHub Desktop


---

📋 Quick Copy URLs

For easy copying, here are all important URLs:

=== JOIN DATAHIVE ===
https://datahive.ai?invite=vxrkrxr

=== THIS BOT REPOSITORY ===
https://github.com/mejri02/datahive-bot

=== PYTHON INSTALLATION ===
https://python.org/downloads
https://pip.pypa.io/en/stable/installation/

=== PROXY RESOURCES ===
https://github.com/monosans/proxy-list
https://ipinfo.io
https://useragentstring.com


---

💖 Support

If you find this helpful, consider:

· Giving a ⭐ star on GitHub
· Sharing with friends
· Reporting issues


---

<div align="center">
  Made with ❤️ by [mejri02](https://github.com/mejri02)
  <br>
  <sub>If this helped you earn more, consider supporting!</sub>
</div>
---

Join DataHive now: https://datahive.ai?invite=vxrkrxr

---

✅ All referral links are now **clickable** in Markdown.  

You can replace your old `README.md` with this version and push to GitHub:

```bash
git add README.md
git commit -m "Fix referral links to be clickable"
git push
