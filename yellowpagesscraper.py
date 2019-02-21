import csv
import requests
import sys
from bs4 import BeautifulSoup

class Store:
	def __init__(self, name, street, locality, state, zipcode, number):
		self.name = name
		self.street = street
		self.locality = locality
		self.state = state
		self.zipcode = zipcode
		self.number = number
	def returnData(self):
		return [self.name, self.street, self.locality, self.state, self.zipcode, self.number]

def openCSV(fn): #opens a CSV file with zipcode using the filename
	zipcodes = []
	try:
		with open(fn) as f:
			reader = csv.reader(f)
			for row in reader:
				if(row[0] != ''):
					zipcodes.append(row[0])
	except FileNotFoundError:
		print("Please input a valid filename (eg zipcodes.csv) ")
		quit()
	return zipcodes

def createFileName(keyword): #creates a filename "keyword"-results.csv
	return keyword + "-results.csv"

def save(filename, data): #saves the result to a csv file
	with open(filename, 'a+', newline = "") as file:
		writer = csv.writer(file)
		writer.writerows(data)
	file.close()

def inputKeyword(): #inputs keyword and csv filename
	filename = None;
	keyword = None;
	if(len(sys.argv) == 1):
		filename = input("What's the CSV's filename? ")
		keyword = input("What's the keyword? ")
	elif(len(sys.argv) == 2):
		filename = sys.argv[1]
		keyword = input("What's the keyword? ")
	elif(len(sys.argv) == 3):
		filename = sys.argv[1]
		keyword = sys.argv[2]
	else:
		print("Incorrect number of arguments. Please input '" + sys.argv[0] + " [filename] [keyword]'")
		quit()
	return filename, keyword

def search(keyword, zipcode, page=1, results = []): #from keyword and zipcode, run a search in the website
	url = ''
	if(page == 1):
		url = "https://www.yellowpages.com/search?search_terms=" + keyword + "&geo_location_terms=" + zipcode + "&s=distance"
	else:
		url = "https://www.yellowpages.com/search?search_terms=" + keyword + "&geo_location_terms=" + zipcode + "&s=distance&page=" + str(page)
	html = requests.get(url)
	soup = BeautifulSoup(html.text, "html.parser")
	page_results = getResults(soup)
	page_results = getValid(zipcode, page_results)
	if(page_results == []):
		return results
	results = results + page_results
	page += 1
	return search(keyword, zipcode, page, results)

def getResults(soup): #gets the unprocessed div results and returns as a list
	results = soup.findAll("div", {"class": "result"})
	return results

def getValid(zipcode, page_results): #gets only the valid search results
	pr = []
	for result in page_results:
		if(is_part(zipcode, result.find("p", {"class": "adr"}))):
			pr.append(result)
	return pr
	
def is_part(zipcode, address): #checks if zipcode is contained in the address
	try:
		zc = address.select('span')[3].get_text(strip=True)
		return zipcode == zc
	except:
		return False

def scrape(result): #scrape the results
	name = result.find('a', {"class": "business-name"}).get_text(strip=True)
	address = result.find('p', {"class": "adr"})
	street = address.select('span')[0].get_text(strip=True)
	locality = address.select('span')[1].get_text(strip=True)
	state = address.select('span')[2].get_text(strip=True)
	zipcode = address.select('span')[3].get_text(strip=True)
	number = result.find('div', {"class": "phones"}).get_text(strip=True)
	return Store(name, street, locality, state, zipcode, number)

def main():
	filename, keyword = inputKeyword()
	zipcodes = openCSV(filename)
	for zipcode in zipcodes:
		print("Searching " + keyword + " in " + zipcode)
		results = search(keyword, zipcode)
		print("Found " + str(len(results)))
		data = []
		for result in results:
			data.append(scrape(result).returnData())
		save(createFileName(keyword), data)
	print("Scraping Done")

if __name__ == "__main__":
	main()