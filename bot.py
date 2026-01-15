import requests
import json
from datetime import datetime
import pytz
import time
from colorama import Fore, Back, Style, init
import uuid
import platform
import os
import random
import hashlib
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

class DataHiveBot:
    def __init__(self):
        self.base_url = "https://api.datahive.ai/api"
        self.wib = pytz.timezone('Asia/Jakarta')
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.account_user_agents = {}
        self.account_device_info = {}
        self.failed_proxies = set()
        self.session_cache = {}
        self.lock = threading.Lock()
        self.stats_lock = threading.Lock()
        
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def generate_device_fingerprint(self, account_key):
        base = f"{account_key}-{uuid.uuid4()}"
        return hashlib.md5(base.encode()).hexdigest()

    def get_persistent_device_info(self, account_key):
        if account_key not in self.account_device_info:
            device_id = str(uuid.uuid4())
            self.account_device_info[account_key] = {
                "device_id": device_id,
                "os": f"{platform.system()} {platform.release()}",
                "cpu_model": random.choice(["Intel Core i5-10400", "Intel Core i7-9700", "AMD Ryzen 5 3600", "Intel Core i5-11400"]),
                "cpu_arch": "x86_64",
                "cpu_count": str(random.choice([4, 6, 8])),
                "fingerprint": self.generate_device_fingerprint(account_key)
            }
        return self.account_device_info[account_key]

    def get_user_agents(self):
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        ]

    def get_random_user_agent_for_account(self, account_key):
        if account_key not in self.account_user_agents:
            self.account_user_agents[account_key] = random.choice(self.get_user_agents())
        return self.account_user_agents[account_key]

    def get_headers(self, token, device_info, account_key=None):
        if account_key:
            user_agent = self.get_random_user_agent_for_account(account_key)
        else:
            user_agent = random.choice(self.get_user_agents())
        
        if "Chrome" in user_agent and "Edg" not in user_agent:
            browser = "Google Chrome"
            version = user_agent.split("Chrome/")[1].split(".")[0] if "Chrome/" in user_agent else "120"
            sec_ch_ua = f'"Chromium";v="{version}", "{browser}";v="{version}", "Not_A Brand";v="99"'
        elif "Firefox" in user_agent:
            browser = "Firefox"
            version = user_agent.split("Firefox/")[1].split(".")[0] if "Firefox/" in user_agent else "121"
            sec_ch_ua = f'"Firefox";v="{version}", "Not_A Brand";v="99"'
        elif "Edg" in user_agent:
            browser = "Microsoft Edge"
            version = user_agent.split("Edg/")[1].split(".")[0] if "Edg/" in user_agent else "122"
            sec_ch_ua = f'"Chromium";v="{version}", "Microsoft Edge";v="{version}", "Not_A Brand";v="99"'
        else:
            sec_ch_ua = '"Chromium";v="120", "Google Chrome";v="120", "Not_A Brand";v="99"'
        
        if "Windows" in user_agent:
            platform_os = "Windows"
            device_model = "PC x86 - Chrome"
            device_name = "windows pc"
            device_os = "Windows 10.0.0"
            if "Firefox" in user_agent:
                device_model = "PC x86 - Firefox"
            elif "Edg" in user_agent:
                device_model = "PC x86 - Edge"
        elif "Macintosh" in user_agent:
            platform_os = "macOS"
            device_model = "Mac - Chrome"
            device_name = "mac pc"
            device_os = "macOS 10.15.7"
        elif "Linux" in user_agent:
            platform_os = "Linux"
            device_model = "Linux PC - Chrome"
            device_name = "linux pc"
            device_os = "Linux 5.15.0"
        else:
            platform_os = "Windows"
            device_model = "PC x86 - Chrome"
            device_name = "windows pc"
            device_os = "Windows 10.0.0"
        
        return {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {token}",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "chrome-extension://kpehiknhddgllkbmdkjeffonbhkfbfoe",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "sec-ch-ua": sec_ch_ua,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": f'"{platform_os}"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": user_agent,
            "x-app-version": "0.2.5",
            "x-cpu-architecture": device_info["cpu_arch"],
            "x-cpu-model": device_info["cpu_model"],
            "x-cpu-processor-count": device_info["cpu_count"],
            "x-device-id": device_info["device_id"],
            "x-device-model": device_model,
            "x-device-name": device_name,
            "x-device-os": device_os,
            "x-device-type": "extension",
            "x-s": "f",
            "x-user-agent": user_agent,
            "x-user-language": "en-US"
        }

    def get_wib_time(self):
        return datetime.now(self.wib).strftime('%x %X %Z')

    def log(self, message):
        with self.lock:
            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {self.get_wib_time()} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
                flush=True
            )

    def print_banner(self):
        banner = f"""
        {Fore.GREEN + Style.BRIGHT}DataHive {Fore.BLUE + Style.BRIGHT}Auto Farming BOT
        {Fore.WHITE + Style.DIM}Enhanced v0.4.0 (Concurrent Multi-Threading System)
        {Fore.YELLOW + Style.DIM}⚡ Parallel Processing + Anti-Detection
        """
        print(banner)

    def mask_email(self, email):
        if "@" in email:
            local, domain = email.split('@', 1)
            if len(local) <= 6:
                hide_local = local[:2] + '*' * 3 + local[-1:]
            else:
                hide_local = local[:3] + '*' * 3 + local[-3:]
            return f"{hide_local}@{domain}"
        return email

    def print_account_info(self, account_num, email, proxy, ua_info, status_color, message):
        proxy_display = f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}{Fore.CYAN + Style.BRIGHT}Proxy: {Style.RESET_ALL}{Fore.WHITE + Style.BRIGHT}{proxy[:30]}...{Style.RESET_ALL}" if proxy else ""
        ua_display = f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}{Fore.CYAN + Style.BRIGHT}UA: {Style.RESET_ALL}{Fore.WHITE + Style.BRIGHT}{ua_info}{Style.RESET_ALL}" if ua_info else ""
        
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{self.mask_email(email)}{Style.RESET_ALL}"
            f"{proxy_display}"
            f"{ua_display}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status: {Style.RESET_ALL}"
            f"{status_color + Style.BRIGHT}{message}{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} ]{Style.RESET_ALL}"
        )

    def load_accounts(self, filename="accounts.txt"):
        try:
            with open(filename, 'r') as f:
                tokens = [line.strip() for line in f if line.strip()]
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(tokens)}{Style.RESET_ALL}"
            )
            return tokens
        except FileNotFoundError:
            self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
            return []

    def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        loaded_proxies = []
        
        try:
            if use_proxy_choice == 1:
                self.log(f"{Fore.YELLOW + Style.BRIGHT}Downloading proxies...{Style.RESET_ALL}")
                response = requests.get("https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt", timeout=30)
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                raw_proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return []
                with open(filename, 'r') as f:
                    raw_proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not raw_proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return []
            
            for proxy in raw_proxies:
                cleaned_proxy = self.validate_and_format_proxy(proxy)
                if cleaned_proxy:
                    loaded_proxies.append(cleaned_proxy)
            
            self.proxies = loaded_proxies
            
            http_count = sum(1 for p in loaded_proxies if p.startswith("http://"))
            https_count = sum(1 for p in loaded_proxies if p.startswith("https://"))
            socks4_count = sum(1 for p in loaded_proxies if p.startswith("socks4://"))
            socks5_count = sum(1 for p in loaded_proxies if p.startswith("socks5://"))
            
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Loaded: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(loaded_proxies)}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}   HTTP: {http_count} | HTTPS: {https_count} | SOCKS4: {socks4_count} | SOCKS5: {socks5_count}{Style.RESET_ALL}"
            )
            
            return loaded_proxies
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []
            return []

    def validate_and_format_proxy(self, proxy_str):
        proxy_str = proxy_str.strip()
        
        if not proxy_str:
            return None
        
        schemes = ["http://", "https://", "socks4://", "socks5://", "socks4h://", "socks5h://"]
        for scheme in schemes:
            if proxy_str.startswith(scheme):
                return proxy_str
        
        if ":" in proxy_str and not proxy_str.startswith("["):
            parts = proxy_str.split(":")
            if len(parts) >= 2:
                ip = parts[0]
                port = parts[1]
                
                try:
                    port_num = int(port)
                    if port_num == 80:
                        return f"http://{ip}:{port}"
                    elif port_num == 443:
                        return f"https://{ip}:{port}"
                    elif port_num in [1080, 9050]:
                        return f"socks5://{ip}:{port}"
                    else:
                        return f"http://{ip}:{port}"
                except:
                    return f"http://{proxy_str}"
        
        return f"http://{proxy_str}"

    def get_next_proxy_for_account(self, account):
        with self.lock:
            if account not in self.account_proxies:
                if not self.proxies:
                    return None
                
                attempts = 0
                while attempts < 5 and len(self.proxies) > 0:
                    proxy = self.proxies[self.proxy_index]
                    
                    if proxy in self.failed_proxies:
                        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
                        attempts += 1
                        continue
                    
                    self.account_proxies[account] = proxy
                    self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
                    return proxy
                
                if len(self.proxies) > 0:
                    proxy = self.proxies[self.proxy_index]
                    self.account_proxies[account] = proxy
                    self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
                    return proxy
            
            return self.account_proxies.get(account)

    def rotate_proxy_for_account(self, account):
        with self.lock:
            if not self.proxies:
                return None
            
            current_proxy = self.account_proxies.get(account)
            if current_proxy:
                self.failed_proxies.add(current_proxy)
            
            attempts = 0
            while attempts < len(self.proxies):
                proxy = self.proxies[self.proxy_index]
                
                if proxy in self.failed_proxies:
                    self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
                    attempts += 1
                    continue
                
                self.account_proxies[account] = proxy
                self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
                
                self.log(f"{Fore.YELLOW + Style.BRIGHT}[ {account} ] Proxy rotated{Style.RESET_ALL}")
                return proxy
                
                attempts += 1
            
            proxy = self.proxies[self.proxy_index]
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
            return proxy

    def print_question(self):
        while True:
            try:
                print(f"\n{Fore.CYAN + Style.BRIGHT}{'='*60}{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Free Proxyscrape Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                print(f"{Fore.CYAN + Style.BRIGHT}{'='*60}{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Free Proxyscrape" if choose == 1 else 
                        "With Private" if choose == 2 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate_input = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()
                if rotate_input in ["y", "n"]:
                    rotate = rotate_input == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate

    def get_worker_info(self, token, device_info, account_num, email, proxy=None, account_key=None):
        try:
            url = f"{self.base_url}/worker"
            headers = self.get_headers(token, device_info, account_key)
            proxies = {"http": proxy, "https": proxy} if proxy else None
            
            response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                points_24h = data.get('points24h', 0)
                
                if 'user' in data:
                    user = data['user']
                    total_points = user.get('points', 0)
                    
                    ua_info = self.get_user_agent_info(headers["user-agent"])
                    
                    self.print_account_info(
                        account_num,
                        email,
                        proxy,
                        ua_info,
                        Fore.WHITE,
                        f"24h: {Fore.YELLOW + Style.BRIGHT}{points_24h:.2f} PTS{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}Total: {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{total_points:.2f} PTS{Style.RESET_ALL}"
                    )
                
                return data
            else:
                ua_info = self.get_user_agent_info(self.get_headers(token, device_info, account_key)["user-agent"])
                self.print_account_info(account_num, email, proxy, ua_info, Fore.RED, f"Failed Get Info: Status {response.status_code}")
                return None
                
        except Exception as e:
            ua_info = self.get_user_agent_info(self.get_headers(token, device_info, account_key)["user-agent"])
            self.print_account_info(account_num, email, proxy, ua_info, Fore.RED, f"Error: {str(e)}")
            return None

    def get_user_agent_info(self, user_agent):
        if "Chrome" in user_agent and "Edg" not in user_agent:
            if "Windows" in user_agent:
                return "Chrome/Win"
            elif "Macintosh" in user_agent:
                return "Chrome/Mac"
            elif "Linux" in user_agent:
                return "Chrome/Linux"
            else:
                return "Chrome"
        elif "Firefox" in user_agent:
            return "Firefox"
        elif "Edg" in user_agent:
            return "Edge"
        else:
            return "Browser"

    def ping_uptime(self, token, device_info, account_num, email, proxy=None, account_key=None):
        try:
            url = f"{self.base_url}/ping/uptime"
            headers = self.get_headers(token, device_info, account_key)
            proxies = {"http": proxy, "https": proxy} if proxy else None
            
            response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
            
            if response.status_code == 200:
                ua_info = self.get_user_agent_info(headers["user-agent"])
                self.print_account_info(account_num, email, proxy, ua_info, Fore.GREEN, "PING Success")
                return True
            else:
                ua_info = self.get_user_agent_info(headers["user-agent"])
                self.print_account_info(account_num, email, proxy, ua_info, Fore.RED, f"PING Failed: Status {response.status_code}")
                return False
                
        except Exception as e:
            ua_info = self.get_user_agent_info(self.get_headers(token, device_info, account_key)["user-agent"])
            self.print_account_info(account_num, email, proxy, ua_info, Fore.RED, f"PING Failed: {str(e)}")
            return False

    def send_heartbeat(self, token, device_info, account_num, email, proxy=None, account_key=None):
        try:
            url = f"{self.base_url}/heartbeat"
            headers = self.get_headers(token, device_info, account_key)
            proxies = {"http": proxy, "https": proxy} if proxy else None
            
            payload = {
                "timestamp": int(time.time() * 1000),
                "deviceId": device_info["device_id"]
            }
            
            response = requests.post(url, headers=headers, json=payload, proxies=proxies, timeout=30)
            
            if response.status_code == 200:
                ua_info = self.get_user_agent_info(headers["user-agent"])
                self.print_account_info(account_num, email, proxy, ua_info, Fore.GREEN, "Heartbeat Sent")
                return True
            else:
                return False
                
        except Exception as e:
            return False

    def check_worker_ip(self, token, device_info, account_num, email, proxy=None, account_key=None):
        try:
            url = f"{self.base_url}/network/worker-ip"
            headers = self.get_headers(token, device_info, account_key)
            proxies = {"http": proxy, "https": proxy} if proxy else None
            
            response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip', 'Unknown')
                ua_info = self.get_user_agent_info(headers["user-agent"])
                self.print_account_info(account_num, email, proxy, ua_info, Fore.GREEN, f"IP Check: {ip}")
                return True
            else:
                ua_info = self.get_user_agent_info(headers["user-agent"])
                self.print_account_info(account_num, email, proxy, ua_info, Fore.RED, f"IP Check Failed: Status {response.status_code}")
                return False
                
        except Exception as e:
            ua_info = self.get_user_agent_info(self.get_headers(token, device_info, account_key)["user-agent"])
            self.print_account_info(account_num, email, proxy, ua_info, Fore.RED, f"IP Check Failed: {str(e)}")
            return False

    def register_worker(self, token, device_info, account_num, email, proxy=None, account_key=None):
        try:
            url = f"{self.base_url}/worker/register"
            headers = self.get_headers(token, device_info, account_key)
            proxies = {"http": proxy, "https": proxy} if proxy else None
            
            payload = {
                "deviceId": device_info["device_id"],
                "deviceModel": headers["x-device-model"],
                "deviceOs": headers["x-device-os"],
                "cpuModel": device_info["cpu_model"],
                "cpuArchitecture": device_info["cpu_arch"],
                "cpuProcessorCount": device_info["cpu_count"]
            }
            
            response = requests.post(url, headers=headers, json=payload, proxies=proxies, timeout=30)
            
            if response.status_code in [200, 201]:
                ua_info = self.get_user_agent_info(headers["user-agent"])
                self.print_account_info(account_num, email, proxy, ua_info, Fore.GREEN, "Worker Registered")
                return True
            else:
                return False
                
        except Exception as e:
            return False

    def process_worker_cycle(self, worker, rotate_proxy, use_proxy):
        account_key = worker['account_key']
        proxy = worker.get('proxy')
        
        random_delay = random.uniform(0.5, 2.5)
        time.sleep(random_delay)
        
        uptime_ok = self.ping_uptime(
            worker['token'], 
            worker['device_info'], 
            worker['num'], 
            worker['email'], 
            proxy, 
            account_key
        )
        
        result = {
            'success': uptime_ok,
            'points': 0,
            'points_24h': 0
        }
        
        if uptime_ok:
            time.sleep(random.uniform(0.8, 1.5))
            self.send_heartbeat(
                worker['token'], 
                worker['device_info'], 
                worker['num'], 
                worker['email'], 
                proxy, 
                account_key
            )
            
            time.sleep(random.uniform(0.8, 1.5))
            self.check_worker_ip(
                worker['token'], 
                worker['device_info'], 
                worker['num'], 
                worker['email'], 
                proxy, 
                account_key
            )
        else:
            if rotate_proxy and use_proxy:
                new_proxy = self.rotate_proxy_for_account(account_key)
                worker['proxy'] = new_proxy
                proxy = new_proxy
                
                time.sleep(random.uniform(0.5, 1.2))
                uptime_ok = self.ping_uptime(
                    worker['token'], 
                    worker['device_info'], 
                    worker['num'], 
                    worker['email'], 
                    proxy, 
                    account_key
                )
                
                if uptime_ok:
                    time.sleep(random.uniform(0.8, 1.5))
                    self.send_heartbeat(
                        worker['token'], 
                        worker['device_info'], 
                        worker['num'], 
                        worker['email'], 
                        proxy, 
                        account_key
                    )
                    time.sleep(random.uniform(0.8, 1.5))
                    self.check_worker_ip(
                        worker['token'], 
                        worker['device_info'], 
                        worker['num'], 
                        worker['email'], 
                        proxy, 
                        account_key
                    )
        
        time.sleep(random.uniform(0.5, 1.2))
        worker_info = self.get_worker_info(
            worker['token'], 
            worker['device_info'], 
            worker['num'], 
            worker['email'], 
            proxy, 
            account_key
        )
        
        if worker_info:
            if 'user' in worker_info:
                result['points'] = worker_info['user'].get('points', 0)
            result['points_24h'] = worker_info.get('points24h', 0)
        
        return result

    def run_concurrent_cycle(self, active_workers, rotate_proxy, use_proxy, max_workers=10):
        self.log(f"{Fore.BLUE + Style.BRIGHT}⚡ Starting concurrent ping cycle for {len(active_workers)} accounts...{Style.RESET_ALL}")
        
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.process_worker_cycle, worker, rotate_proxy, use_proxy): worker 
                for worker in active_workers
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.log(f"{Fore.RED + Style.BRIGHT}Thread error: {e}{Style.RESET_ALL}")
        
        return results

    def run(self):
        self.clear_terminal()
        self.print_banner()
        
        tokens = self.load_accounts()
        
        if not tokens:
            self.log(f"{Fore.RED + Style.BRIGHT}No Accounts Loaded.{Style.RESET_ALL}")
            return
        
        use_proxy_choice, rotate_proxy = self.print_question()
        
        use_proxy = False
        if use_proxy_choice in [1, 2]:
            use_proxy = True
        
        self.clear_terminal()
        self.print_banner()
        self.log(
            f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{len(tokens)}{Style.RESET_ALL}"
        )
        
        if use_proxy:
            self.load_proxies(use_proxy_choice)
        
        self.log(f"{Fore.CYAN + Style.BRIGHT}={'='*75}{Style.RESET_ALL}")
        
        active_workers = []
        
        self.log(f"{Fore.YELLOW + Style.BRIGHT}🔧 Initializing workers...{Style.RESET_ALL}")
        
        for i, token in enumerate(tokens, 1):
            account_key = f"account_{i}"
            
            device_info = self.get_persistent_device_info(account_key)
            
            proxy = self.get_next_proxy_for_account(account_key) if use_proxy else None
            
            try:
                headers = self.get_headers(token, device_info, account_key)
                proxies = {"http": proxy, "https": proxy} if proxy else None
                response = requests.get(f"{self.base_url}/worker", headers=headers, proxies=proxies, timeout=30)
                
                if response.status_code != 200:
                    ua_info = self.get_user_agent_info(headers["user-agent"])
                    self.print_account_info(i, f"account_{i}@temp.com", proxy, ua_info, Fore.RED, "Failed to get worker info")
                    if rotate_proxy and use_proxy:
                        proxy = self.rotate_proxy_for_account(account_key)
                    continue
                    
                worker_data = response.json()
                real_email = worker_data.get('user', {}).get('email', f'unknown{i}@email.com')
                
                server_device_id = worker_data.get('deviceId')
                if server_device_id:
                    device_info['device_id'] = server_device_id
                    self.account_device_info[account_key]['device_id'] = server_device_id
                
            except Exception as e:
                ua_info = self.get_user_agent_info(self.get_headers(token, device_info, account_key)["user-agent"])
                self.print_account_info(i, f"account_{i}@temp.com", proxy, ua_info, Fore.RED, f"Connection failed: {e}")
                if rotate_proxy and use_proxy:
                    proxy = self.rotate_proxy_for_account(account_key)
                continue
            
            if worker_data:
                points_24h = worker_data.get('points24h', 0)
                total_points = worker_data.get('user', {}).get('points', 0)
                
                ua_info = self.get_user_agent_info(self.get_headers(token, device_info, account_key)["user-agent"])
                
                self.print_account_info(
                    i,
                    real_email,
                    proxy,
                    ua_info,
                    Fore.WHITE,
                    f"24h: {Fore.YELLOW + Style.BRIGHT}{points_24h:.2f} PTS{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{total_points:.2f} PTS{Style.RESET_ALL}"
                )
                
                active_workers.append({
                    'num': i,
                    'token': token,
                    'device_info': device_info,
                    'email': real_email,
                    'proxy': proxy,
                    'account_key': account_key,
                    'ping_interval': random.randint(58, 62)
                })
                
                time.sleep(0.5)
        
        if not active_workers:
            self.log(f"{Fore.RED + Style.BRIGHT}No Active Workers.{Style.RESET_ALL}")
            return
        
        self.log(f"{Fore.CYAN + Style.BRIGHT}={'='*75}{Style.RESET_ALL}")
        self.log(f"{Fore.GREEN + Style.BRIGHT}Active Workers: {Style.RESET_ALL}{Fore.WHITE + Style.BRIGHT}{len(active_workers)}{Style.RESET_ALL}")
        
        ua_distribution = {}
        for worker in active_workers:
            ua = self.account_user_agents.get(worker['account_key'], "Unknown")
            ua_distribution[ua] = ua_distribution.get(ua, 0) + 1
        
        self.log(f"{Fore.CYAN + Style.BRIGHT}User Agent Distribution:{Style.RESET_ALL}")
        for ua, count in ua_distribution.items():
            browser = self.get_user_agent_info(ua)
            self.log(f"  {Fore.WHITE}{browser}: {Fore.YELLOW}{count} accounts{Style.RESET_ALL}")
        
        self.log(f"{Fore.CYAN + Style.BRIGHT}={'='*75}{Style.RESET_ALL}")
        
        self.log(f"{Fore.YELLOW + Style.BRIGHT}🚀 Starting initial registration and ping...{Style.RESET_ALL}")
        
        def init_worker(worker):
            time.sleep(random.uniform(0.2, 1.5))
            self.register_worker(
                worker['token'], 
                worker['device_info'], 
                worker['num'], 
                worker['email'], 
                worker['proxy'], 
                worker['account_key']
            )
            time.sleep(random.uniform(0.5, 1.2))
            self.ping_uptime(
                worker['token'], 
                worker['device_info'], 
                worker['num'], 
                worker['email'], 
                worker['proxy'], 
                worker['account_key']
            )
            time.sleep(random.uniform(0.5, 1.2))
            self.send_heartbeat(
                worker['token'], 
                worker['device_info'], 
                worker['num'], 
                worker['email'], 
                worker['proxy'], 
                worker['account_key']
            )
            time.sleep(random.uniform(0.5, 1.2))
            self.check_worker_ip(
                worker['token'], 
                worker['device_info'], 
                worker['num'], 
                worker['email'], 
                worker['proxy'], 
                worker['account_key']
            )
        
        with ThreadPoolExecutor(max_workers=min(10, len(active_workers))) as executor:
            executor.map(init_worker, active_workers)
        
        self.log(f"{Fore.CYAN + Style.BRIGHT}={'='*75}{Style.RESET_ALL}")
        self.log(f"{Fore.GREEN + Style.BRIGHT}✅ Initial setup complete. Starting farming loop...{Style.RESET_ALL}")
        self.log(f"{Fore.CYAN + Style.BRIGHT}={'='*75}{Style.RESET_ALL}")
        
        ping_count = 0
        
        try:
            while True:
                avg_interval = sum(w['ping_interval'] for w in active_workers) / len(active_workers)
                
                for remaining in range(int(avg_interval), 0, -1):
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {self.get_wib_time()} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE + Style.BRIGHT}⏳ Next cycle in {remaining}s...{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(1)
                
                print(" " * 100, end="\r")
                
                ping_count += 1
                
                start_time = time.time()
                results = self.run_concurrent_cycle(active_workers, rotate_proxy, use_proxy, max_workers=min(15, len(active_workers)))
                cycle_duration = time.time() - start_time
                
                successful_pings = sum(1 for r in results if r['success'])
                failed_pings = len(results) - successful_pings
                total_points_session = sum(r['points'] for r in results)
                total_points_24h = sum(r['points_24h'] for r in results)
                
                self.log(f"{Fore.CYAN + Style.BRIGHT}={'='*75}{Style.RESET_ALL}")
                
                if total_points_session > 0:
                    avg_points = total_points_session / len(active_workers)
                    self.log(
                        f"{Fore.GREEN + Style.BRIGHT}💰 Cycle #{ping_count} Summary:{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}   • Duration: {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{cycle_duration:.2f}s{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} (⚡ {len(active_workers)/cycle_duration:.1f} accounts/s){Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}   • Total Points: {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}{total_points_session:.2f} PTS{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}   • 24h Points: {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}{total_points_24h:.2f} PTS{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}   • Avg per Account: {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}{avg_points:.2f} PTS{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}   • Success Rate: {Style.RESET_ALL}"
                        f"{Fore.GREEN}{successful_pings}✓ {Fore.RED}{failed_pings}✗ {Style.RESET_ALL}"
                        f"{Fore.WHITE}({(successful_pings/len(active_workers)*100):.1f}%){Style.RESET_ALL}"
                    )
                    self.log(f"{Fore.CYAN + Style.BRIGHT}={'='*75}{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(
                f"\n{Fore.CYAN + Style.BRIGHT}[ {self.get_wib_time()} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}[ EXIT ] DataHive - BOT{Style.RESET_ALL}                                       "
            )
            
            total_pings = ping_count * len(active_workers) * 3
            self.log(
                f"{Fore.YELLOW + Style.BRIGHT}📊 Final Statistics:{Style.RESET_ALL}\n"
                f"{Fore.CYAN + Style.BRIGHT}   • Total Cycles: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{ping_count}{Style.RESET_ALL}\n"
                f"{Fore.CYAN + Style.BRIGHT}   • Active Accounts: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(active_workers)}{Style.RESET_ALL}\n"
                f"{Fore.CYAN + Style.BRIGHT}   • Total API Calls: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{total_pings}{Style.RESET_ALL}\n"
                f"{Fore.CYAN + Style.BRIGHT}   • Mode: {Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT}Concurrent Multi-Threading{Style.RESET_ALL}"
            )

if __name__ == "__main__":
    try:
        bot = DataHiveBot()
        bot.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
