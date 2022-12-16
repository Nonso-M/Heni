# Custom Scrapers

This Repo contains custom scrapers for a product websites. It also
contains settings for the spiders, a module for data cleaning and formatting, and module 
for running the spiders.


## Prerequisites
***
Interpreter: Python 3.9.7

Scraping Framework: Scrapy==2.5.0


## Quick Start
The scrapers can be ran from the command line using the following command
```Comman Line/Bash
scrapy crawl bearspider
```

## Usage

All packages used are part of the Standard python Library except otherwise specified.

`pip install -r requirements.txt`
***
*How to Use this repo*
1. Create a Directory
2. Open the directory in your IDE
3. Make a virtual environment with `python -m venv .venv`
4. Clone this Repo into your directory 
5. Install the requirements from above individually or by using the requirements file with `pip install -r requirements.txt`
6. Change directory into the repo directory. `cd <yourdirectory>`
7. Change directory into Heni

8. Run the spider on the Command line using
```Comman Line
scrapy crawl bearspace
```

The expected output upon running these spiders is:
1. Output of the spider is sent as a csv during the execution to *Heni/data/products.csv*



## Future Improvements
The data going to the csv has to be cleaned further. Some wierd unicode was seen
upon inspection


## Contributing
Pull requests are welcome from team members. For major changes,
please open an issue first to discuss what you would like to change.
Make sure you assign the appropriate changelogs.
Please make sure to update tests as appropriate.
To contribute to custom-scraper, follow these steps:

Fork this repository.

1. Create a branch: git checkout -b <branch_name>.

2. Make your changes and commit them: git commit -m '<commit_message>'

3. Push to the original branch: git push origin <project_name>/<location>

4. Create the pull request.


## License

