from bs4 import BeautifulSoup
import requests
import threading


print("{:<20} {:<10} {:<5} {:<25} {:<15} {:<5} {:<5} {:<10}".format(
    'IP Address', 'Port', 'Code', 'Country', 'Anonymity', 'Google', 'Https', 'Last Checked')
      )
print("-----------------------------------------------------------------------------------------------------------")

def scrape_proxy_info(tr) -> None:
    all_td: str = tr.find_all('td')
    if len(all_td) > 0:
        ip_address: str = all_td[0].text
        port: str = all_td[1].text
        code: str = all_td[2].text
        country: str = all_td[3].text
        anonymity: str = all_td[4].text
        google: str = all_td[5].text
        https: str = all_td[6].text
        last_checked: str = all_td[7].text
        write_to_file(f"{ip_address}:{port}")
        print("{:<20} {:<10} {:<5} {:<25} {:<15} {:<5} {:<5} {:<10}".format(ip_address, port, code, country, anonymity, google, https, last_checked))
        


def scrape_page(url) -> None:
    page = requests.get(url)
    soup: object = BeautifulSoup(page.text, "html.parser")
    all_proxy_div: str = soup.find('div', class_='table-responsive')
    top_table: int = all_proxy_div.find('table')
    all_tr: str = top_table.find_all('tr')
    threads: list = []
    for tr in all_tr:
        thread = threading.Thread(target=scrape_proxy_info, args=(tr,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join() 

def write_to_file(proxy) -> None:
    with open("proxy.txt", "a") as file:
        file.write(proxy + "\n")

if __name__ == '__main__':
    url: str = 'https://free-proxy-list.net/'
    scrape_page(url)
