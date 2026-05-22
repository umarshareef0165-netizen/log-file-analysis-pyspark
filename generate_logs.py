"""
Synthetic Apache Access Log Generator
Generates a realistic access.log file for Big Data Analytics project.
"""
import random
from datetime import datetime, timedelta

random.seed(42)

NUM_LINES = 5000
OUTPUT_FILE = "access.log"

NORMAL_IPS = [f"192.168.{random.randint(1,50)}.{random.randint(1,254)}" for _ in range(200)]
FREQUENT_IPS = ["203.124.45.18", "182.176.92.103", "39.45.211.7", "119.73.108.45", "110.93.224.66"]
SUSPICIOUS_IPS = ["185.220.101.42", "45.155.205.99", "194.165.16.77"]

URLS = [
    "/", "/index.html", "/about", "/contact", "/login", "/signup", "/dashboard",
    "/api/users", "/api/products", "/api/orders", "/api/cart", "/api/checkout",
    "/products", "/products/laptop", "/products/phone", "/products/tablet",
    "/blog", "/blog/post-1", "/blog/post-2", "/blog/post-3",
    "/images/logo.png", "/css/style.css", "/js/app.js", "/favicon.ico",
    "/admin", "/admin/users", "/admin/settings",
    "/wp-admin", "/.env", "/config.php",
    "/search?q=laptop", "/search?q=phone", "/cart", "/profile",
]

METHODS = ["GET"] * 85 + ["POST"] * 12 + ["PUT"] * 2 + ["DELETE"] * 1
STATUS_CODES_NORMAL = [200] * 75 + [301] * 5 + [304] * 8 + [404] * 8 + [500] * 2 + [403] * 2
STATUS_CODES_SUSPICIOUS = [404] * 50 + [403] * 30 + [401] * 15 + [500] * 5

USER_AGENTS_HUMAN = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

USER_AGENTS_BOT = [
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    "python-requests/2.31.0",
    "curl/7.88.1",
    "Wget/1.21.3",
    "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",
    "Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)",
]

def random_timestamp(base):
    days_offset = random.randint(0, 6)
    hour_weights = [1,1,1,1,1,2,3,5,8,10,12,13,12,11,10,9,8,7,6,5,4,3,2,1]
    hour = random.choices(range(24), weights=hour_weights)[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    ts = base + timedelta(days=days_offset, hours=hour, minutes=minute, seconds=second)
    return ts.strftime("%d/%b/%Y:%H:%M:%S +0000")

def main():
    base_date = datetime(2026, 5, 12, 0, 0, 0)
    lines = []
    for _ in range(NUM_LINES):
        r = random.random()
        if r < 0.04:
            ip = random.choice(SUSPICIOUS_IPS)
            url = random.choice(["/wp-admin", "/.env", "/config.php", "/admin", "/admin/users",
                                 "/wp-login.php", "/phpmyadmin", "/.git/config"])
            status = random.choice(STATUS_CODES_SUSPICIOUS)
            ua = random.choice(USER_AGENTS_BOT)
            method = random.choice(["GET", "POST"])
        elif r < 0.20:
            ip = random.choice(FREQUENT_IPS)
            url = random.choice(URLS)
            status = random.choice(STATUS_CODES_NORMAL)
            ua = random.choice(USER_AGENTS_HUMAN + USER_AGENTS_BOT)
            method = random.choice(METHODS)
        elif r < 0.30:
            ip = random.choice(NORMAL_IPS)
            url = random.choice(URLS + ["/robots.txt", "/sitemap.xml"])
            status = random.choice(STATUS_CODES_NORMAL)
            ua = random.choice(USER_AGENTS_BOT)
            method = "GET"
        else:
            ip = random.choice(NORMAL_IPS)
            url = random.choice(URLS)
            status = random.choice(STATUS_CODES_NORMAL)
            ua = random.choice(USER_AGENTS_HUMAN)
            method = random.choice(METHODS)
        size = random.randint(200, 25000) if status == 200 else random.randint(0, 500)
        ts = random_timestamp(base_date)
        line = f'{ip} - - [{ts}] "{method} {url} HTTP/1.1" {status} {size} "-" "{ua}"'
        lines.append(line)

    def extract_ts(line):
        try:
            ts_str = line.split("[")[1].split("]")[0]
            return datetime.strptime(ts_str, "%d/%b/%Y:%H:%M:%S +0000")
        except Exception:
            return datetime(2026, 1, 1)
    lines.sort(key=extract_ts)
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(lines))
    print(f"Generated {len(lines)} log lines into {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
