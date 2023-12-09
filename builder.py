import requests
import sys
import time

from bs4 import BeautifulSoup


def process_name(soup):
    # Extract the title
    title = soup.title.string if soup.title else "No title found"
    sections = title.split("by")
    name = sections[0].strip()

    list_of_all_links = soup.findAll('a')
    youtube = ""

    for link in list_of_all_links:                  
        if "youtube" in link['href']:
            youtube = (link['href'])
        elif "youtu.be" in link['href']:
            youtube = (link['href'])

    return(f"<a href=\"{youtube}\">{name}</a>")


def process_group(soup):
    # Extract the title
    title = soup.title.string if soup.title else "No title found"
    sections = title.split("by")
    group = sections[1].split("::")[0].strip()

    return(f"{group}")  


def process_platform(soup):
    platform_raw = str(soup.find("span", {"class": "platform"}))
    platform = platform_raw.split(">")[1].split("<")[0]

    if (platform == "Amiga OCS/ECS"):
        platform = "OCS/ECS Amiga's"
    elif (platform == "Windows"):
        platform = "Windows PC's"
    elif (platform == "MS-Dos"):
        platform = "MS-DOS PC's"
    elif (platform == "Commodore 64"):
        platform = "the C-64"
    elif (platform == "JavaScript"):
        platform = "JavaScript"
    elif (platform != "iOS"):
        platform = "the " + platform

    return(f"{platform}")


def process_links(input_url, soup):
    demozoo_raw = str(soup.find("li", {"id": "demozooID"}))
    demozoo_url = demozoo_raw.split("[")[1].split("]")[0]

    return(f"(<a href=\"{input_url}\">pouet</a>) ({demozoo_url})")


def process_line(input_url):
    pouet_prod_tag = "https://www.pouet.net/prod.php?which="

    if input_url.startswith(pouet_prod_tag):
        try:
            response = requests.get(input_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')

                name = process_name(soup)
                group = process_group(soup)
                platform = process_platform(soup)
                links = process_links(input_url, soup) 

                return(f"{name} by {group} for {platform} {links}")
 
            else:
                return("")


        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")        

# Check if arguments are provided
if len(sys.argv) <= 1:
    print("No arguments provided.")
else:
    file_path = sys.argv[1]

    with open(file_path, 'r') as file:
        print("<ul>")
        for line in file:
            output = process_line(line.strip())  # .strip() removes extra newline characters
            print(f"<li>{output}</li>")
            time.sleep(1)
        print("</ul>")   