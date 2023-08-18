import requests
from bs4 import BeautifulSoup
import csv

def getcontact(url):
    import requests
    from bs4 import BeautifulSoup

    headers = { 
            'User-Agent':"Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"}
    response = requests.get(url,headers=headers,)
    soup = BeautifulSoup(response.text, 'html.parser')

    phone = soup.find_all(attrs={"itemprop":"telephone"})
    adress = soup.find_all(attrs={"class":"adr"})
    
    if phone!=[] and adress!=[]:
        phone = str(phone[0].text)
        adr = str(adress[0].text)
        return adr, phone
    elif adress==[] and phone!=[]:
        adr = "No info"
        phone = str(phone[0].text)
        return adr, phone
    elif phone==[] and adress!=[]:
        phone = "No info"
        adr = str(adress[0].text)
        return adr, phone
    else:
        adr, phone = "No info", "No info"
        return adr, phone

# Store the collected data from multiple URLs
all_data = []
filename=1

# Loop from 1 to 10 to change the value inside the curly braces
for i in range(1, 11):
    # Construct the URL with the updated value inside the curly braces
    url = f'https://cafes.heyplaces.in/Mumbai/?sida={i}&distance=9999'

    # Send a GET request to the URL with specified headers
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
    }
    response = requests.get(url, headers=headers)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all h3 tags and store them in heading3
    heading3 = soup.find_all("h3")
    heading3 = str(heading3)
    heading3 = BeautifulSoup(heading3, 'html.parser')

    # Initialize lists to store gym names and URLs
    links = []
    name = []

    # Extract gym names and URLs from the h3 tags
    print("Finding Cafes")
    for a in heading3.find_all('a', href=True):
        name.append(a.text)
        s = str("https://gyms.heyplaces.in" + (a['href']))
        links.append(s)

    # Initialize dictionaries to store gym information
    dic = {
        "Name": "",
        "number": "+9123456743"
    }

    adress = []
    phone = []

    # Loop through the URLs to get contact information using the 'getcontact(i)' function
    print("Extracting Data")
    for i in links:
        t = getcontact(i)
        adress.append(t[0])
        phone.append(t[1])

    # Store the collected data in a dictionary
    data = {
        "Name": name,
        "Address": adress,
        "Phone": phone
    }

    # Append the data from the current URL to the 'all_data' list
    all_data.append(data)

# Write the collected data to a CSV file
    
    print(f"Adding data to csv fiel no {filename}")
    output_file = "collecteddata.csv"
    with open(output_file, mode='a+', newline='',encoding="utf-8") as file:
        fieldnames = ['Name', 'Address', 'Phone']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for data in all_data:
            for i in range(len(data['Name'])):
                writer.writerow({'Name': data['Name'][i], 'Address': data['Address'][i], 'Phone': data['Phone'][i]})

    print(f"Data written to stage {filename}", output_file)
    all_data=[]
    filename+=1