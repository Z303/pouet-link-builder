import requests
import sys
from bs4 import BeautifulSoup

def process_line(input):
    POUET_PROD_TAG = "https://www.pouet.net/prod.php?which="

    if input.startswith(POUET_PROD_TAG):
        try:
            response = requests.get(input)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract the title
                title = soup.title.string if soup.title else "No title found"
                sections = title.split("by")

                name = sections[0].strip()
                group = sections[1].split("::")[0].strip()

                demozoo_raw = str(soup.find("li", {"id": "demozooID"}))
                demozoo_url = demozoo_raw.split("[")[1].split("]")[0]
 
                listOfAllLinks = soup.findAll('a')
                youtube = ""

                for link in listOfAllLinks:                  
                    if "youtube" in link:
                        youtube = (link['href'])
          
                platform_raw = str(soup.find("span", {"class": "platform"}))
                platform = platform_raw.split(">")[1].split("<")[0]

                return(f"<a href=\"{youtube}\">{name}</a> by {group} for {platform} (<a href=\"{input}\">pouet</a>) ({demozoo_url})")
 
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
        print("</ul>")   