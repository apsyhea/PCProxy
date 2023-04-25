from asyncio import Task
import asyncio
import aiohttp
from bs4 import BeautifulSoup, NavigableString, Tag

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
    """ Extract the individual proxy fields from the <td> elements."""
    ip_address: str = all_td[COLUMNS['IP Address']].text
    port: str = all_td[COLUMNS['Port']].text
    code: str = all_td[COLUMNS['Code']].text
    country: str = all_td[COLUMNS['Country']].text
    anonymity: str = all_td[COLUMNS['Anonymity']].text
    google: str = all_td[COLUMNS['Google']].text
    https: str = all_td[COLUMNS['Https']].text
    last_checked: str = all_td[COLUMNS['Last Checked']].text
    # Return the proxy information as a tuple.
    return (
        f"{ip_address}:{port}",
        f"{ip_address:<20} {port:<10} {code:<5} {country:<25}"
        f"{anonymity:<15} {google:<5} {https:<5} {last_checked:<10}"
    )


# Scrape the proxy information from a single <tr> element.


async def scrape_proxy_info(t_tr) -> None:
    """ Extract all <td> elements from the <tr> element."""
    all_td: str = t_tr.find_all('td')
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
    """ Send a GET request to the specified URL and retrieve the page content."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            page: str = await response.text()
            soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
            # Find the <div> element containing the proxy table.
            all_proxy_div: Tag | NavigableString | None = soup.find(
                'div', class_='table-responsive')
            if all_proxy_div is None:
                raise Exception(
                    'Error: div with class "table-responsive" not found')
            # Find the <table> element containing the proxy information.
            top_table: Tag | NavigableString | int | None = all_proxy_div.find(
                'table')
            if top_table is None:
                raise Exception('Error: table not found')
            # Extract all <tr> elements from the <table> element.
            all_tr: set = top_table.find_all('tr')  # type: ignore
            type(all_tr)
            tasks: list = []
            # Create a task for each <tr> element and add it to the list of tasks.
            for p_tr in all_tr:
                task: Task[None] = asyncio.create_task(scrape_proxy_info(p_tr))
                tasks.append(task)
            # Wait for all tasks to complete before moving on.
            await asyncio.gather(*tasks)

# Define a function to write the scraped proxy information to a file


def write_to_file(proxy) -> None:
    """ Write the given proxy string to a file named 'proxy.txt'."""
    with open("proxy.txt", "a") as file:
        file.write(proxy + "\n")


# Define the main function that will scrape the proxy information
if __name__ == '__main__':
    url: str = 'https://free-proxy-list.net/'

    # Print the headers for the proxy information table
    print(f"{'IP Address':<20} {'Port':<10} {'Code':<5} {'Country':<25}"
          f"{'Anonymity':<15} {'Google':<5} {'Https':<5} {'Last Checked':<10}")

    # Print a separator line to make the table easier to read
    print("------------------------------------------------------" +
          "------------------------------------------------------"
          )
    asyncio.run(scrape_page(url))
