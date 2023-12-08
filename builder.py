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
                
                print(f"The title of the page is: {title}")
            else:
                print(f"Failed to fetch URL. Status code: {response.status_code}")


        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")        

# Check if arguments are provided
if len(sys.argv) <= 1:
    print("No arguments provided.")
else:
    file_path = sys.argv[1]

    with open(file_path, 'r') as file:
        for line in file:
            process_line(line.strip())  # .strip() removes extra newline characters