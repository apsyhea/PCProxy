import asyncio
from bs4 import BeautifulSoup
import aiohttp

print("{:<20} {:<10} {:<5} {:<25} {:<15} {:<5} {:<5} {:<10}".format(
    'IP Address', 'Port', 'Code', 'Country',
    'Anonymity', 'Google', 'Https', 'Last Checked')
)
print("------------------------------------------------------"+
      "------------------------------------------------------"
      )

async def scrape_proxy_info(tr) -> None:
    all_td: str = tr.find_all('td')
    if len(all_td) > 0:
        ip_address: str = all_td[0].text # type: ignore
        port: str = all_td[1].text # type: ignore
        code: str = all_td[2].text # type: ignore
        country: str = all_td[3].text # type: ignore
        anonymity: str = all_td[4].text # type: ignore
        google: str = all_td[5].text # type: ignore
        https: str = all_td[6].text # type: ignore
        last_checked: str = all_td[7].text # type: ignore
        write_to_file(f"{ip_address}:{port}")
        print("{:<20} {:<10} {:<5} {:<25} {:<15} {:<5} {:<5} {:<10}".format(
            ip_address, port, code, country, anonymity, google, https, last_checked)
              )

async def scrape_page(url) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            page: str = await response.text()
            soup: str = BeautifulSoup(page, "html.parser") # type: ignore
            all_proxy_div: str = soup.find('div', class_='table-responsive') # type: ignore
            top_table: str = all_proxy_div.find('table') # type: ignore
            all_tr: str = top_table.find_all('tr') # type: ignore
            tasks: list = []
            for tr in all_tr:
                task: str = asyncio.create_task(scrape_proxy_info(tr)) # type: ignore
                tasks.append(task)
            await asyncio.gather(*tasks)

def write_to_file(proxy) -> None:
    with open("proxy.txt", "a") as file:
        file.write(proxy + "\n")

if __name__ == '__main__':
    url: str = 'https://free-proxy-list.net/'
    asyncio.run(scrape_page(url))
