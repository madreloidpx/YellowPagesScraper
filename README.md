Setting up:
1. First download Python for Windows here: https://www.python.org/downloads/
2. Download get-pip.py here: https://bootstrap.pypa.io/get-pip.py
3. In cmd, type 'python get-pip.py'
4. In cmd, type 'pip install beautifulsoup4'
5. In the cmd, type 'yellowpagesscraper.py [filename] [keyword]' where filename is the csv file for the zipcodes and keyword is for the keyword to be input in the search bar. Typing the filename and the keyword in the command prompt is optional since the program can ask the user to input the details manually after running.
example valid:
	yellowpagesscraper.py us_postal_codes.csv verizon
	yellowpagesscraper.py us_postal_codes.csv
	yellowpagesscraper.py
The first one goes straight to scraping without the need for user input, while the others asl for the file/keyword.
