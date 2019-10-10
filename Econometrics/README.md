## R (and Python) for Econometrics
This module of the course covers non-structural econometric methods and how to apply these tools using open source software: mainly in R, but also in Python.

## 1. Installing R and Setting up Kernal for Jupyter Notebooks

There are a couple option here and some are more or less straight forward depending on your OS and if you already have R installed already.

### Method 1:
* Follow [these instructions](https://docs.anaconda.com/anaconda/navigator/tutorials/r-lang/) to install the R kernal for Jupyter Notebook using the Anaconda navigator.

### Method 2:
Do the following:
1. [Install R from CRAN](https://cran.r-project.org)
2. If you want a popular IDE for R, [intall RStudio](https://www.rstudio.com)
3. With R installed, go to your command line and do the following to create an R kernal for Jupyter Notebooks:
    * `$ R` # to launch R
    * `install.packages(c('repr', 'IRdisplay', 'evaluate', 'crayon', 'pbdZMQ', 'devtools', 'uuid', 'digest'))`
    * `devtools::install_github('IRkernel/IRkernel')`
    * `IRkernel::installspec()` or, to install system-wide for all users do `IRkernel::installspec(user = FALSE)`

Additionally, if you like Atom and want to continue using it for writing R scripts, you will want to add the following plug-ins:
* `linter-lintr` # linter for R
* `language-r` # syntax highlighting for R
* `r-exec` # to execute R from Atom

(Note that Anaconda's package manager Conda does manage R packages, but at least in my experience with OSX, this manager has not worked well.  Thus I recommend installing from CRAN as outlined above.)

## 2. Notebooks we worked through in class

* [Intro to R data structures](https://github.com/jdebacker/CompEcon_Fall19/blob/master/Econometrics/R_Basics.ipynb)
* [Reading and writing data in R](https://github.com/jdebacker/CompEcon_Fall19/blob/master/Econometrics/R_Data.ipynb)
* [Writing functions, numerical optimization in R](https://github.com/jdebacker/CompEcon_Fall19/blob/master/Econometrics/R_Functions.ipynb)

## 3. Problem Set

* [Problem Set #5](https://github.com/jdebacker/CompEcon_Fall19/blob/master/Econometrics/PS5.pdf)


## 4. Useful Links

* R
	* [Guide to R for Stata Users](http://dss.princeton.edu/training/RStata.pdf)
	* [Panel Data Models in R](https://www.princeton.edu/~otorres/Panel101R.pdf)
	* [The R Plot Gallery](http://www.r-graph-gallery.com/portfolio/ggplot2-package/)
* Python
	* [Stata to Python cheat sheet](https://cheatsheets.quantecon.org/stats-cheatsheet.html)
	* [StatsModel Package](http://www.statsmodels.org/dev/index.html)
	* [QuantEcon: Linear regression in Python](https://lectures.quantecon.org/py/ols.html)
	* Panel Data Models in Python via the [linearmodels package](https://pypi.python.org/pypi/linearmodels)
	* [rpy2 for calling R from Python](http://rpy2.readthedocs.io/en/version_2.8.x/overview.html)
