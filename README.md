# Trope
Repository for trope and topic based analyis of film genre using
community generated data from tvtropes.org and user reviews from letterboxd.com
Authors: Fitz Koch and Jeremy Elliott

# Environments
* **NOTE: UNDER CONSTRUCTION** 
* First, make sure you have conda installed and running.
* Next, create environments using the following commands
    * `conda env create -f .\Environments\ENV1_environment.yml -n ENV_1` 
    * `conda env create -f .\Environments\ENV2_environment.yml -n ENV_2` 
* If you don't already have jupyter installed in your global environment, do that. Once you have it installed, use `python -m ipykernel install --user --name=<env_name> --display-name "Python (<env_name>)"` to set up the virtual environment you built from the yml so you can use the environment in your files for each environment you build above. (replace `<env_name>` with each environment name)
* For .py scripts, first enter `conda activate <env_name>` to make sure you're in the right environment. The actual env_name is listed at the top of the file.
* For .ipynb notebooks, make sure that you select the relevant `<env_name>` ipykernel to run the code successfully. The actual environment name is included at the top of each notebook. 
* **Note**: There might be new depencies since you last created the environment. If you have trouble, use `conda env remove -n <env_name>` to first remove your old environment and then complete the steps above to make sure everything is in place.

# Setup Steps

## Letterboxd Setup Steps
* Use the `letterboxd` 
* Run through the numbered `.py` scripts in the `Code\Letterboxd_Scraping` folder in order. If you want, you can handfix any movies that fail to match using `Code/Improved_scrape_books/2_51_link_handfixed_movies_to_letterboxd.ipynb`




# Data Sources 
* [Letterboxd.com](https://letterboxd.com/) for film reviews and metadata
* [Tropescraper](https://github.com/rhgarcia/tropescraper) for initial tv tropes scrape
* [TV Tropes](https://tvtropes.org/) for further tv tropes 

<!-- 
## Steps
* First, run the `Code/01_setup.ipynb` notebook to build the SEE_LAB Brightway Project and load it with the 3.9.1 and 3.11 ecoinvent cutoff databases. For some reason this seems to work better in a .ipynb jupyter notebook then in a .py script. 
* Second, make sure all your data is up to date. While I will attempt to host publically available and small indexing datasets in the repository, it's often better to build stuff if you can. See [Data Sources](#data-sources). 
* Next, go through the notebooks in `Exploratory_notebooks`  in order. Use the `SEE_BW` ipykernel you created in the [Environment](#environment) steps. While no later code relies upon these notebooks, they are helpful for understanding the proect.

# Data Sources
* [ecoQuery ecoinvent Database](https://ecoquery.ecoinvent.org/) for primary database

    ## Economic Data
    * [World Bank](https://data.worldbank.org/) for GDP Data

    ## Indexing Data
    * [Cloford.com] (https://cloford.com/resources/codes/index.htm) for indexing Country codes to sub-continental regions
    * [Country and Continent Codes (stevewithington GitHub) ](https://gist.github.com/stevewithington/20a69c0b6d2ff846ea5d35e5fc47f26c) for indexing Country codes to Continents

    ## Shapefiles
    * [Natural Earth](https://www.naturalearthdata.com/) for global state and territory shapefiles
 -->
