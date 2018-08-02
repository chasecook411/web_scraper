from selenium import webdriver
import csv

driver = None

def scrape_listing(directory_listing):
    row = [ driver.current_url ]
    for list_item in directory_listing:
        # keep the url for a current listing
        row = row[0:1]

        row.append(list_item.text)
        # we'll deal with three kinds of files here
        # directories, hidden files, and regular files
        if is_directory(list_item):
            row.append('Directory')
        elif is_hidden(list_item):
            row.append('Hidden File')
        else:
            row.append('Regular File')

        # write the row to our file
        writer.writerow(row)

def is_directory(elem):
    return '/' in elem.text

def is_hidden(elem):
    return elem.text[0] == '.'

try:
    driver = webdriver.Chrome('./chromedriver')
except:
    print('No ChromeDriver available, or not valid permissions to execute')
    exit(1)

try:
    spreadsheet = open('./page-contents.csv', 'wb')
    header = ['URL', 'File Name', 'File Type']
    writer = csv.writer(spreadsheet, delimiter = ',')
    writer.writerow(header)
except Exception as e:
    print('Could not create CSV file', e)

try:
    driver.get('http://localhost:8000')
    directory_listing = driver.find_elements_by_tag_name('a')
    scrape_listing(directory_listing)
except Exception as e:
    print('Caught Exception retrieving data: ', e)

if driver is not None:
    driver.quit()
