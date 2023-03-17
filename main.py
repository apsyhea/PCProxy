import asyncio
import aiohttp
from bs4 import BeautifulSoup
from asyncio import Task


COLUMNS: dict[str, int] = {
    'IP Address': 0,
    'Port': 1,
    'Code': 2,
    'Country': 3,
    'Anonymity': 4,
    'Google': 5,
    'Https': 6,
    'Last Checked': 7
}

def format_proxy_info(all_td) -> tuple[str, str]:
    ip_address: str = all_td[COLUMNS['IP Address']].text
    port: str = all_td[COLUMNS['Port']].text
    code: str = all_td[COLUMNS['Code']].text
    country: str = all_td[COLUMNS['Country']].text
    anonymity: str = all_td[COLUMNS['Anonymity']].text
    google: str = all_td[COLUMNS['Google']].text
    https: str = all_td[COLUMNS['Https']].text
    last_checked: str = all_td[COLUMNS['Last Checked']].text
    return f"{ip_address}:{port}", "{:<20} {:<10} {:<5} {:<25} {:<15} {:<5} {:<5} {:<10}".format(
            ip_address, port, code, country, anonymity, google, https, last_checked)

async def scrape_proxy_info(tr) -> None:
    all_td: str = tr.find_all('td')
    if len(all_td) > 0:
        proxy: str
        string: str 
        proxy, string = format_proxy_info(all_td)
        write_to_file(proxy)
        print(string)

async def scrape_page(url) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            page: str = await response.text()
            soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
            all_proxy_div = soup.find('div', class_='table-responsive')
            if all_proxy_div is None:
                raise Exception('Error: div with class "table-responsive" not found')
            top_table = all_proxy_div.find('table')
            if top_table is None:
                raise Exception('Error: table not found')
            all_tr = top_table.find_all('tr') # type: ignore
            tasks: list = []
            for tr in all_tr[1:]:
                task: Task[None] = asyncio.create_task(scrape_proxy_info(tr))
                tasks.append(task)
            await asyncio.gather(*tasks)

def write_to_file(proxy) -> None:
    with open("proxy.txt", "a") as file:
        file.write(proxy + "\n")

if __name__ == '__main__':
    url: str = 'https://free-proxy-list.net/'
    print("{:<20} {:<10} {:<5} {:<25} {:<15} {:<5} {:<5} {:<10}".format(
        'IP Address', 'Port', 'Code', 'Country', 'Anonymity', 'Google', 'Https', 'Last Checked')
    )
    print("------------------------------------------------------"+
          "------------------------------------------------------"
          )
    asyncio.run(scrape_page(url))