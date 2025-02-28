# Tropes, Topics, Shifts, and More
Repository for trope and topic based analyis of film genre using
community generated data from tvtropes.org and user reviews from letterboxd.com


# Environments
* First, make sure you have conda installed and running.
* Next, create environments using the following commands
    * For the general use environment, enter `conda env create -f envs/tropes_letterboxd_general.yml`. Once conda finishes creating the environment, then enter `conda activate tropes_letterboxd_general` and then `pip install -e .`  These last two commands ensure that the general tools used across all scripts and notebooks are recognized. Use this environment for any of the scraping, data analysis, or shifting. Do not use for topic modelling. 
        * You may need to enter `playwright install` to succesfully scrape using playwright. Conda doesn't always capture that.  
    * For the `bertopic_env` environment, enter `conda env create -f envs/letterboxd_scrape.yml`, and then adapt the commands above. to finish setup. Use this environment for topic modelling and data analysis thereof. 


* For .py scripts, first enter `conda activate <env_name>` to make sure you're in the right environment. The actual env_name is listed at the top of the file.
* For .ipynb notebooks, make sure that you select the relevant `<env_name>` ipykernel to run the code successfully. The actual environment name is included at the top of each notebook. 
* **Note**: There might be new dependencies since you last created the environment. If you have trouble, use `conda env remove -n <env_name>` to first remove your old environment and then complete the steps above to make sure everything is in place.

# Setup Steps
## Letterboxd Setup Steps
* Use the `scrape_and_model` environment for all scripts and notebooks in this section.
* Run through the numbered `.py` scripts in the `Code\Letterboxd_Scraping` folder in order. If you want, you can handfix any movies that fail to match using `Code/Improved_scrape_books/2_51_link_handfixed_movies_to_letterboxd.ipynb`

# Data Sources 
* [Letterboxd.com](https://letterboxd.com/) for film reviews and metadata
* [Tropescraper](https://github.com/rhgarcia/tropescraper) for initial tv tropes scrape
* [TV Tropes](https://tvtropes.org/) for further tv tropes 


# Contributors
- [Fitz Koch](https://github.com/FWJK1)
- [Jeremy Elliott](https://github.com/JeremyE-uvm)