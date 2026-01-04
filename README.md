# DataHive Auto Farming Bot

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/mejri02/datahive-bot.svg)](https://github.com/mejri02/datahive-bot/stargazers)
[![GitHub forks](https://img.shields.io/badge/GitHub_forks-datahive--bot-lightgrey)](https://github.com/mejri02/datahive-bot/network)

## 🔗 Join DataHive & Get a Bonus
👉 **[Join DataHive with referral bonus](https://datahive.ai?invite=vxrkrxr)**

---

## 📌 Overview

**DataHive Auto Farming Bot** is a Python automation tool designed to maximize earnings on the DataHive platform.  
It supports multiple accounts, proxy rotation, and automatic session handling.

---

## ✨ Features

### 🎯 Multi-Account Management
- Run multiple accounts simultaneously
- Per-account monitoring
- Real-time point tracking
- Automatic session management

### 🛡️ Anti-Detection System
- Random user-agent per account
- Realistic browser headers
- Device ID synchronization
- Platform diversity (Windows / Mac / Linux)

### 🔄 Smart Proxy Support
- HTTP / HTTPS / SOCKS4 / SOCKS5
- Automatic proxy rotation
- Free proxies from Proxyscrape
- Private proxy support
- Failed proxy blacklisting

### 📊 Real-Time Monitoring
- Live point statistics
- Connection status indicators
- IP address verification
- Session performance analytics

### ⚡ Automation
- Auto-ping every 60 seconds
- Error recovery system
- 24/7 continuous operation
- Proxy failover mechanism

### 🎨 User Interface
- Color-coded console output
- Email masking for privacy
- WIB timezone display
- Progress indicators

---

## 🚀 Installation & Setup

### 1️⃣ Clone the repository

```bash
https://github.com/mejri02/datahive-bot.git
cd datahive-bot
```

### 2️⃣ Install required packages

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure your accounts

1. Open `accounts.txt`
2. Add your **DataHive bearer tokens** (one per line)

#### How to get your token

- Log in to **DataHive Web**
- Open **DevTools** (F12)
- Go to **Network**
- Look for calls to `api.datahive.ai`
- Copy the **Bearer token** from the **Authorization header**

Example:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4️⃣ Configure proxies (optional)

1. Open `proxy.txt`
2. Add proxies (one per line)

Supported formats:

- `http://ip:port`
- `https://ip:port`
- `socks4://ip:port`
- `socks5://ip:port`
- `ip:port` (defaults to HTTP)

Example:

```text
http://proxy1.com:8080
socks5://proxy2.com:1080
192.168.1.1:3128
```

---

## ▶️ Usage

Run the bot:

```bash
python bot.py
```

You will see options:

```
1. Run with free Proxyscrape proxies
2. Run with private proxies
3. Run without proxies
```

The bot will then:

1. Load accounts
2. Assign proxies (if used)
3. Ping every 60 seconds
4. Display live earnings
5. Run until stopped (Ctrl + C)

---

## 📁 Project Structure

```
datahive-bot/
├── bot.py              # Main bot script
├── requirements.txt    # Python dependencies
├── README.md           # Documentation
├── .gitignore          # Git ignore file
├── accounts.txt        # Tokens (add manually)
└── proxy.txt           # Proxy list (optional)
```

---

## ⚙️ Requirements

`requirements.txt` should include:

```text
requests>=2.31.0
pytz>=2023.3
colorama>=0.4.6
```

---

## 📊 Example Output

```bash
$ python bot.py

DataHive Auto Farming BOT
Version v0.2.5

Accounts loaded: 3
Proxies loaded: 50

[ Account: exa***ple@email.com - 24h: 15.23 PTS - Total: 125.50 PTS ]
[ Account: us***ail.com - Status: PING Success ]
[ Account: te***com - IP: 192.168.1.100 ]

Session Summary:
• Total Points: 450.75 PTS
• 24h Points: 65.89 PTS
• Average per Account: 150.25 PTS
```

---

## 🔧 Advanced Settings

### Custom User-Agents
Each account receives a unique user-agent:

- Chrome (Windows)
- Firefox (Mac)
- Edge (Windows)
- Chrome (Linux)

### Proxy Rotation

To enable rotation:

```bash
Rotate invalid proxies? [y/n] -> y
```

### Without Proxy

Choose **option 3** (best for single account)

---

## ❓ FAQ

**Q: How many accounts can I run?**  
As many as you want. Start with 3–5 to test.

**Q: Do I need proxies?**  
Recommended for multiple accounts.

**Q: How often does it ping?**  
Every 60 seconds per account.

---

## ⚠️ Important Notes

- Keep tokens private
- Use proxies for multiple accounts
- Monitor logs regularly
- Respect platform limits
- Update the bot when possible

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.

- Not affiliated with DataHive
- Use at your own risk
- Follow platform ToS
- Do not abuse the service

---

## 📄 License

Licensed under the **MIT License**.  
See the `LICENSE` file for details.

---

## 🤝 Contributing

Contributions are welcome:

1. Fork the repo
2. Create a branch
3. Commit changes
4. Push to your branch
5. Open a pull request

---

## 🔗 Useful Links

**DataHive**
- Join with bonus: https://datahive.ai?invite=vxrkrxr
- Dashboard: https://app.datahive.ai

**Python**
- https://python.org/downloads
- https://pip.pypa.io

---

<div align="center">
Made with ❤️ by <a href="https://github.com/mejri02">mejri02</a><br/>
<sub>If this helped you, consider giving a ⭐ on GitHub</sub>
</div>
