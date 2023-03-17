import asyncio
import aiohttp
from bs4 import BeautifulSoup
from asyncio import Task

# A dictionary that maps column names to their indices in the proxy table.
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

# Given a list of <td> elements, extract the relevant proxy information and return it as a tuple.
def format_proxy_info(all_td) -> tuple[str, str]:
    # Extract the individual proxy fields from the <td> elements.
    ip_address: str = all_td[COLUMNS['IP Address']].text
    port: str = all_td[COLUMNS['Port']].text
    code: str = all_td[COLUMNS['Code']].text
    country: str = all_td[COLUMNS['Country']].text
    anonymity: str = all_td[COLUMNS['Anonymity']].text
    google: str = all_td[COLUMNS['Google']].text
    https: str = all_td[COLUMNS['Https']].text
    last_checked: str = all_td[COLUMNS['Last Checked']].text
    # Return the proxy information as a tuple.
    return f"{ip_address}:{port}", "{:<20} {:<10} {:<5} {:<25} {:<15} {:<5} {:<5} {:<10}".format(
            ip_address, port, code, country, anonymity, google, https, last_checked)

# Scrape the proxy information from a single <tr> element.
async def scrape_proxy_info(tr) -> None:
    # Extract all <td> elements from the <tr> element.
    all_td: str = tr.find_all('td')
    if len(all_td) > 0:
        # Format the proxy information and write it to a file.
        proxy: str
        string: str 
        proxy, string = format_proxy_info(all_td)
        write_to_file(proxy)
        # Print the formatted proxy information to the console.
        print(string)

# Scrape the proxy information from a single page.
async def scrape_page(url) -> None:
    async with aiohttp.ClientSession() as session:
        # Send a GET request to the specified URL and retrieve the page content.
        async with session.get(url) as response:
            page: str = await response.text()
            soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
            # Find the <div> element containing the proxy table.
            all_proxy_div = soup.find('div', class_='table-responsive')
            if all_proxy_div is None:
                raise Exception('Error: div with class "table-responsive" not found')
            # Find the <table> element containing the proxy information.
            top_table = all_proxy_div.find('table')
            if top_table is None:
                raise Exception('Error: table not found')
            # Extract all <tr> elements from the <table> element.
            all_tr = top_table.find_all('tr') # type: ignore
            type(all_tr)
            tasks: list = []
            # Create a task for each <tr> element and add it to the list of tasks.
            for tr in all_tr[1:]:
                task: Task[None] = asyncio.create_task(scrape_proxy_info(tr))
                tasks.append(task)
            # Wait for all tasks to complete before moving on.
            await asyncio.gather(*tasks)

# Define a function to write the scraped proxy information to a file
def write_to_file(proxy) -> None:
    with open("proxy.txt", "a") as file:
        file.write(proxy + "\n")
        
        
# Define the main function that will scrape the proxy information
if __name__ == '__main__':
    url: str = 'https://free-proxy-list.net/'
    
    # Print the headers for the proxy information table
    print("{:<20} {:<10} {:<5} {:<25} {:<15} {:<5} {:<5} {:<10}".format(
        'IP Address', 'Port', 'Code', 'Country', 'Anonymity', 'Google', 'Https', 'Last Checked')
    )
    # Print a separator line to make the table easier to read
    print("------------------------------------------------------"+
          "------------------------------------------------------"
          )
    asyncio.run(scrape_page(url))