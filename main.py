import csv
import env
from selenium import webdriver
from datetime import datetime

driver = webdriver.Chrome(env.CHROME_DRIVER_LOCATION)

def parse_number(text):
    text = text.replace(',', '')
    text = text.replace('.', '')
    text = text.replace('\'', '')
    return int(text)

### Login
driver.get("https://cygnus.astroempires.com/")

# Fill in email input
username = driver.find_element_by_name("email")
username.clear()
username.send_keys(env.EMAIL)

# Fill in password input
password = driver.find_element_by_name("pass")
password.clear()
password.send_keys(env.PASSWORD)

# Submit login form
driver.find_element_by_class_name("input-button").click()

### Go to GUILD page
driver.get("https://cygnus.astroempires.com/guild.aspx")

# sort table by name
driver.find_element_by_class_name('sorttable_alpha').click()

# Get table and rows, then remove headers
table = driver.find_element_by_class_name('tbllisting1')
rows = table.find_elements_by_tag_name('tr')
rows.pop(0)

guildies = []

for row in rows:
    cols = row.find_elements_by_tag_name('td')
    # Get data
    name = cols[2].text
    fleet = parse_number(cols[6].text)
    eco = parse_number(cols[5].text)
    # Append to member list
    guildies.append([name, eco, fleet])

# Print members
for member in guildies:
    print(member[0] + " :")
    print("\t", member[1])
    print("\t", member[2])

# Get date string for filename
file_name = str(datetime.now().strftime("%d-%m-%Y")) + '.csv'

# Write to CSV
with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=',')
    writer.writerows(guildies)

