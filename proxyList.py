import re
import time
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import base64

def get_ip_ports_from_website1():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get("https://spys.one/en/")
    
    ip_port_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]+\b")
    ip_ports_list = []

    elements = driver.find_elements(By.CLASS_NAME, "spy14")
    for element in elements:
        text = element.text
        ip_ports = ip_port_pattern.findall(text)
        ip_ports_list.extend(ip_ports)

    driver.quit()
    print("\n1. websitesi IP alındı.\n")
    return ip_ports_list

def get_ip_ports_from_website2():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get("https://free-proxy-list.net/")
    clipboard_icon = driver.find_element(By.CLASS_NAME, "fa-clipboard")
    clipboard_icon.click()
    time.sleep(2)
    textarea = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/textarea")
    text = textarea.get_attribute("value")
    driver.quit()
    print("\n2. websitesi IP alındı.\n")
    return text.strip().split("\n")

def get_ip_ports_from_website3():
    url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text"
    try:
        response = requests.get(url)
        response.raise_for_status()
        ip_ports_list = [
            line.strip().split("://")[1]
            for line in response.text.splitlines()
            if line.strip() and "://" in line
        ]
        print("\n3. websitesi IP alındı.\n")
        return ip_ports_list
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
        return []

def get_ip_ports_from_website4():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    ip_ports_list = []
    for page_num in range(1, 4):
        url = f"https://advanced.name/freeproxy?page={page_num}"
        driver.get(url)

        rows = driver.find_elements(By.XPATH, "//table[@id='table_proxies']/tbody/tr")
        for row in rows:
            ip = row.find_element(By.XPATH, "./td[2]").text.strip()
            port = row.find_element(By.XPATH, "./td[3]").text.strip()
            ip_ports_list.append(f"{ip}:{port}")

        time.sleep(2)

    driver.quit()
    print("\n4. websitesi IP alındı.\n")
    return ip_ports_list

def get_ip_ports_from_website5():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get("https://proxy-list.org/english/index.php")
    time.sleep(5)

    ip_ports_list = []
    proxy_elements = driver.find_elements(By.XPATH, "//li[@class='proxy']/script")
    for element in proxy_elements:
        script_content = element.get_attribute("innerHTML")
        base64_data = re.search(r"Proxy\('(.+?)'\)", script_content).group(1)
        decoded_data = base64.b64decode(base64_data).decode("utf-8")
        ip_ports_list.append(decoded_data)

    driver.quit()
    print("\n5. websitesi IP alındı.\n")
    return ip_ports_list

def get_ip_ports_from_website6():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://proxy-port.com/en/free-proxy-list")
        time.sleep(5)

        ip_ports_list = []
        proxy_elements = driver.find_elements(By.XPATH, "//div[@class='address-container']")
        for element in proxy_elements:
            ip_port = element.text.strip()
            if ip_port:
                ip_ports_list.append(ip_port)

        print("\n6. websitesi IP alındı.\n")
        return ip_ports_list
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return []
    finally:
        driver.quit()

def get_current_ip_ports():
    ip_ports_website1 = get_ip_ports_from_website1()
    ip_ports_website2 = get_ip_ports_from_website2()
    ip_ports_website3 = get_ip_ports_from_website3()
    ip_ports_website4 = get_ip_ports_from_website4()
    ip_ports_website5 = get_ip_ports_from_website5()
    ip_ports_website6 = get_ip_ports_from_website6()
    return (
        ip_ports_website1
        + ip_ports_website2
        + ip_ports_website3
        + ip_ports_website4
        + ip_ports_website5
        + ip_ports_website6
    )

def append_to_file(file_path, data):
    existing_data = set()
    try:
        with open(file_path, "r") as file:
            existing_data = set(file.read().splitlines())
    except FileNotFoundError:
        pass

    with open(file_path, "a") as file:
        for item in data:
            if item not in existing_data:
                file.write(item + "\n")

def check_proxies(proxy_list):
    url = "https://www.amazon.com/dp/B06Y27V6TL"
    valid_proxies = []

    for proxy in proxy_list:
        print(f"Testing proxy: {proxy}")
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }

        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            if response.status_code == 200:
                print(f"Proxy {proxy} is valid.")
                valid_proxies.append(proxy)
            else:
                print(f"Proxy {proxy} is invalid.")
        except requests.RequestException:
            print(f"Proxy {proxy} failed.")

    return valid_proxies

def write_to_file(file_path, data):
    with open(file_path, "w") as file:
        for item in data:
            file.write(item + "\n")

def insert_into_db(db_config, data):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS proxy_list (
                id INT AUTO_INCREMENT PRIMARY KEY,
                proxy_ip VARCHAR(255) NOT NULL UNIQUE
            )
        """
        )

        for item in data:
            cursor.execute("INSERT INTO proxy_list (proxy_ip) VALUES (%s)", (item,))

        connection.commit()
        print("Veritabanına ekleme işlemi başarılı!")
    except mysql.connector.Error as err:
        print(f"Veritabanına eklenirken bir hata oluştu: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    output_file = "new_ip_ports.txt"
    db_config = {
        "user": "root",
        "password": "",
        "host": "localhost",
        "database": "proxy_db",
    }

    while True:
        ip_ports = get_current_ip_ports()
        append_to_file(output_file, ip_ports)
        print(f"\n\nYeni IP adresleri ve port numaraları dosyaya eklendi: {output_file}\n")
        print(f"{len(ip_ports)} proxy toplandı.")
        
        valid_proxies = check_proxies(ip_ports)
        write_to_file("valid_proxy.txt", valid_proxies)
        insert_into_db(db_config, valid_proxies)
        print(f"\nToplam çalışan proxy sayısı: {len(valid_proxies)}\n")
        
        print("Waiting for 7 minutes before checking again...")
        time.sleep(420)

if __name__ == "__main__":
    main()
