import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def get_ip_ports_from_website1():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    driver.get("https://spys.one/en/")

    ip_port_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]+\b')

    ip_ports_list = []

    elements = driver.find_elements(By.CLASS_NAME, "spy14")
    for element in elements:
        text = element.text
        ip_ports = ip_port_pattern.findall(text)
        ip_ports_list.extend(ip_ports)

    driver.quit()  
    print("\n 1. websitesi IP alındı. \n")
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
    print("\n 2. websitesi IP alındı. \n")

    return text.strip().split('\n')

def get_ip_ports_from_website3():
    
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    
        
    time.sleep(5)

    driver.get("https://proxyscrape.com/free-proxy-list")
    
    time.sleep(5)


    ip_ports_list = []

    rows = driver.find_elements(By.CSS_SELECTOR, "tr")

    for row in rows[1:]:
        columns = row.find_elements(By.CSS_SELECTOR, "td")
        if len(columns) >= 3:  
            ip = columns[1].text.strip()
            port = columns[2].text.strip()
            ip_ports_list.append(ip + ":" + port)

    driver.quit()
    print("\n 3. websitesi IP alındı. \n")

    return ip_ports_list

def get_current_ip_ports():
    ip_ports_website1 = get_ip_ports_from_website1()
    ip_ports_website2 = get_ip_ports_from_website2()
    ip_ports_website3 = get_ip_ports_from_website3()

    return ip_ports_website1, ip_ports_website2, ip_ports_website3

def append_to_file(file_path, data):
    existing_data = set()
    try:
        with open(file_path, 'r') as file:
            existing_data = set(file.read().splitlines())
    except FileNotFoundError:
        pass

    with open(file_path, 'a') as file:
        for item in data:
            if item not in existing_data:
                file.write(item + '\n')


def check_proxies(proxy_list):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    driver.get("https://proxyscrape.com/online-proxy-checker")

    textarea = driver.find_element(By.XPATH, "//textarea[@placeholder='0.0.0.0:1234\n127.0.0.1:3434\nlocalhost:8080' and contains(@class, 'form-control')]")
    textarea.clear()
    textarea.send_keys("\n".join(proxy_list))

    # Butonun CSS Selector kullanılarak bulunması ve tıklanması
    check_button = driver.find_element(By.CSS_SELECTOR, "div.btn-style-lg.text-uppercase.btn.btn-primary.fw-bold.m-auto")
    
    # ActionChains kullanarak tıklama işlemi
    actions = ActionChains(driver)
    actions.move_to_element(check_button).click().perform()
    time.sleep(15)

    valid_proxies = []
    rows = driver.find_elements(By.XPATH, "//tr[@class='table-success']")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        ip = cells[1].text
        port = cells[2].text
        valid_proxies.append(ip + ":" + port)

    driver.quit()

    return valid_proxies




def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(item + '\n')

def main():
    output_file = "new_ip_ports.txt"
    
    # Sonsuz bir döngü oluştur
    while True:
        ip_ports_website1, ip_ports_website2, ip_ports_website3 = get_current_ip_ports()

        append_to_file(output_file, ["1. websitesi ipleri: \n\n"])
        append_to_file(output_file, ip_ports_website1)
        append_to_file(output_file, ["\n\n2. websitesi ipleri:\n\n"])
        append_to_file(output_file, ip_ports_website2)
        append_to_file(output_file, ["\n\n3. websitesi ipleri:\n\n"])
        append_to_file(output_file, ip_ports_website3)

        print("\n\nYeni IP adresleri ve port numaraları dosyaya eklendi: \n", output_file)

        valid_proxies = check_proxies(ip_ports_website1 + ip_ports_website2 + ip_ports_website3)

        write_to_file("valid_proxy.txt", valid_proxies)

        print("\n\nÇalışan proxy'ler valid_proxy.txt dosyasına kaydedildi.")

        print("\n\nProgram sonlandırıldı.")

        print("\nToplam çalışan proxy sayısı: ", len(valid_proxies))

        time.sleep(300)

if __name__ == "__main__":
    main()
