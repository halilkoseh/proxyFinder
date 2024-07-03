# DB Name: proxy_db
# /Users/aitchkay/Desktop/proxyFinder/.venv/bin/python /Users/aitchkay/Desktop/proxyFinder/proxyList.py

import re
import time
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import requests
import base64

def get_ip_ports_from_website1():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    )
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
    options.add_argument("--headless")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)

    driver.get("https://free-proxy-list.net/")
    clipboard_icon = driver.find_element(By.CLASS_NAME, "fa-clipboard")
    clipboard_icon.click()

    time.sleep(2)
    textarea = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div/div[2]/textarea"
    )
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
    options.add_argument("--headless")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    )
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
    options.add_argument("--headless")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    )
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
    options.add_argument("--headless")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://proxy-port.com/en/free-proxy-list")
        time.sleep(5)

        ip_ports_list = []
        proxy_elements = driver.find_elements(
            By.XPATH, "//div[@class='address-container']"
        )
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
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://proxyscrape.com/online-proxy-checker")

        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//textarea[@placeholder='0.0.0.0:1234\n127.0.0.1:3434\nlocalhost:8080' and contains(@class, 'form-control')]",
                )
            )
        )
        textarea.clear()
        textarea.send_keys("\n".join(proxy_list))

        check_button = driver.find_element(
            By.CSS_SELECTOR,
            "div.btn-style-lg.text-uppercase.btn.btn-primary.fw-bold.m-auto",
        )
        actions = ActionChains(driver)
        actions.move_to_element(check_button).click().perform()

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@class='table-success']"))
        )

        valid_proxies = []
        rows = driver.find_elements(By.XPATH, "//tr[@class='table-success']")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            ip = cells[1].text
            port = cells[2].text
            valid_proxies.append(ip + ":" + port)
    except Exception as e:
        print(f"An error occurred: {e}")
        valid_proxies = []
    finally:
        driver.quit()

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

    while True:
        (
            ip_ports_website1,
            ip_ports_website2,
            ip_ports_website3,
            ip_ports_website4,
            ip_ports_website5,
            ip_ports_website6,
        ) = get_current_ip_ports()

        append_to_file(output_file, ["1. websitesi ipleri: \n\n"])
        append_to_file(output_file, ip_ports_website1)
        append_to_file(output_file, ["\n\n2. websitesi ipleri:\n\n"])
        append_to_file(output_file, ip_ports_website2)
        append_to_file(output_file, ["\n\n3. websitesi ipleri:\n\n"])
        append_to_file(output_file, ip_ports_website3)
        append_to_file(output_file, ["\n\n4. websitesi ipleri:\n\n"])
        append_to_file(output_file, ip_ports_website4)
        append_to_file(output_file, ["\n\n5. websitesi ipleri:\n\n"])
        append_to_file(output_file, ip_ports_website5)
        append_to_file(output_file, ["\n\n6. websitesi ipleri:\n\n"])
        append_to_file(output_file, ip_ports_website6)

        print(
            "\n\nYeni IP adresleri ve port numaraları dosyaya eklendi: \n", output_file
        )

        valid_proxies = check_proxies(
            ip_ports_website1
            + ip_ports_website2
            + ip_ports_website3
            + ip_ports_website4
            + ip_ports_website5
            + ip_ports_website6
        )

        write_to_file("valid_proxy.txt", valid_proxies)

        print("\n\nÇalışan proxy'ler valid_proxy.txt dosyasına kaydedildi.")

        insert_into_db(valid_proxies)

        print("\nToplam çalışan proxy sayısı: ", len(valid_proxies))

        time.sleep(300)


if __name__ == "__main__":
    all_proxies = get_current_ip_ports()


    ip_ports = get_current_ip_ports()
    print(f"{len(ip_ports)} proxy toplandı.")

    print("\nProxy kontrolü başlatılıyor...\n")
    valid_proxies = []
    for i in range(0, len(all_proxies), 500):
        proxies_batch = all_proxies[i : i + 500]
        valid_proxies_batch = check_proxies(proxies_batch)
        valid_proxies.extend(valid_proxies_batch)

    print(f"Geçerli proxy sayısı: {len(valid_proxies)}")

    write_to_file("valid_proxy.txt", valid_proxies)

    db_config = {
        "user": "root",
        "password": "",
        "host": "localhost",
        "database": "proxy_db",
    }

    insert_into_db(db_config, valid_proxies)




while True:
        ip_ports = get_current_ip_ports()
        valid_proxies = check_proxies(ip_ports)
        
        if valid_proxies:
            write_to_file("valid_proxy.txt", valid_proxies)
            insert_into_db(db_config, valid_proxies)

        print("Waiting for 7 minutes before checking again...")
        time.sleep(420)  