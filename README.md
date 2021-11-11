# Project 2: Air quality data (40 marks)

[OpenAQ](https://openaq.org/#/) is an NGO which aggregates and distributes open data on **air quality** in many different countries, sourced mainly from government sources. Their website explains:

> We are currently collecting data in 130 different countries and primarily aggregate PM2.5, PM10, ozone (O3), sulfur dioxide (SO2), nitrogen dioxide (NO2), carbon monoxide (CO), and black carbon (BC) measurements. Additional pollutants outside of those standard set of pollutants are now available through low cost sensor sources at certain locations.

The data is accessible via a public API (see Week 7 workshop task), and conveniently, there exists a [Python package called `py-openaq`](http://dhhagan.github.io/py-openaq/index.html) which makes requesting data using Python very easy. We will install this package and learn to use it in the **Week 8 workshop**.

---

## Goal and structure

The goal of this project is for you to present a **coherent and well-coded investigation** into some aspects of the dataset. You should do this in the Jupyter notebook called **`project-2-report.ipynb`**, which will contain your code, as well as any results and visualisations. You should also use Markdown cells to structure the notebook, describe your investigations, and present/explain your results.

This project is an **open-ended** task, so you should come up with your **own ideas** to analyse the dataset and extract useful information or interesting facts. Some ideas of questions you might address in your analysis will be given in the section "Some ideas to get you started"; they are a guide to some things you could think about to get you started, but...

#### you don't need to answer them all, and you are strongly encouraged to answer questions that are not listed.

When you are presenting your investigation of each problem, be sure to make a coherent discussion for each task (using Markdown, maths as appropriate and code cells). In particular, since you are working as a group, some work will be needed to combine all of the code and writing that you each contribute into the submitted notebook -- this is something that you should plan to do, and the quality of **presentation** will be marked.

---

## Data

Go through the [Week 8 workshop task](https://github.com/pypr-2122/pp-w08-workshop) to start exploring the data, and to learn to use the `py-openaq` package to retrieve data.

#### Useful links

- [OpenAQ data policy](https://github.com/openaq/openaq-info/blob/master/DATA-POLICY.md) -- the terms of use for the OpenAQ data.
- [Data type definitions](https://github.com/openaq/openaq-data-format/blob/master/data-type-definitions.md) -- a summary of the data format.
- [API reference for py-openaq](http://dhhagan.github.io/py-openaq/api.html) -- full documentation detailing how to request data with `py-openaq` and detailing the format of the results.
- [Air pollution - European Environment Agency](https://www.eea.europa.eu/themes/air) -- a very useful information page on air pollution in Europe, with lots of great examples of data visualisations, general information about the sources of different pollutants, fact sheets by country, etc.

You are also free to download and use more related data (from the links above or from other sources -- just make sure the data is licensed in a way which allows you to use it!) to complement your investigation if you wish.

---

## Some ideas to get you started

Generally speaking, it's probably a good idea to **limit the scope of your report**, in space and in time. Here are a few examples of what you could consider:

- You could focus your investigation on a particular city, region, or country.
- You could focus your investigation on 1 or 2 specific pollutant(s).
- You could investigate how air pollution varies over time -- for example, how it has generally evolved over the past few years, or how it changes depending on the season or month, depending on the day of the week, or depending on the time of day.

Here are some example questions your report could address. Again, **you should not cover all of them**, and you are certainly encouraged to come up with your own questions too. The important thing is that your report is **coherent and well-presented**, that your code works as intended, and that you explore some of the aspects of this dataset in reasonable depth, presenting results in a way which help you answer relevant questions or queries. If you investigate 1 or 2 of these with sufficient depth, this should be plenty enough for a good report.

- Investigate the influence of city size (for example in terms of population size or density) on air pollution. Remember that for example, the [geocoding API from the Week 7 workshop](https://open-meteo.com/en/docs/geocoding-api) can give you useful information on cities.
- Investigate the influence of weather conditions on air pollution (temperature, humidity, precipitation, wind speed...). A good place to obtain historical weather data is, for example, the [Meteostat API](https://dev.meteostat.net/guide.html), which also has a handy [Python package](https://dev.meteostat.net/python/) you can install and use (similar to `py-openaq`).
- Choose a city, region, or country with many different stations, and visualise the levels of air pollution on a map. For example, OpenAQ have a [world map](https://openaq.org/#/map) on their website showing the latest measurements all over the world, and colour-coding the different levels to quickly visualise hot spots.
- Choose a city, region, or country which has data available over a few years, and which has recently implemented policies to tackle air pollution. Investigate whether these policies have been successful. For example, there is a UN report titled "[Global report summary of air quality policies around the world](https://www.unep.org/resources/report/global-report-summary-air-quality-policies-around-world)" which might be helpful in finding information about this.
- The [Oxford Covid-19 Government Response Tracker (OxCGRT) project](https://www.bsg.ox.ac.uk/research/research-projects/covid-19-government-response-tracker) has collected worldwide data of different countries' measures to limit the spread of Covid since the start of 2020. Investigate the potential impact of some of these measures on air quality -- for example, we might expect that beyond the slowing down of industry, limiting long-distance travel or closing public transportation could have an influence on air pollution. [Here is another example visualisation](https://www.eea.europa.eu/themes/air/air-quality-and-covid19) from the European Environment Agency you could draw inspiration from.


---

### Working on your project

During the Week 8 workshop, or as soon as possible after this, you should discuss with your group and come up with a **plan**.

- **Pair-program** as much as possible! You will likely be much more productive if you have another person to bounce ideas off of about what to investigate or how to present results, and help each other solve problems. You can do this in pairs, you can mix up pairs, you can even do "group programming" sessions with one driver and 2-3 navigators if that's helpful.
- Schedule quick **code reviews** for each other, to help each other stay on track and write better code.
- Use your shared GitHub repo to **collaborate**. Every time you start working on the project, start by **pulling** the latest version from GitHub. Then, as you work, **commit** your changes regularly. When you are done for the day (or even before that), **push** your work to the GitHub repo to share it with your team.
- To **submit** your project, the process will be the same as for Project 1: first, **push** your final version (ready for submission) **to your GitHub repo**, then submit your repo to Gradescope. Gradescope will be set up so that one person can submit the report on behalf of their group.

---

### Packages

You will create a new conda environment called `pp-proj2`, with the help of the `environment.yml` file, during the [Week 8 workshop](https://github.com/pypr-2122/pp-w08-workshop).

Beyond the packages installed in your new `pp-proj2` environment, you can also use any package or library that you find convenient. If there are any other packages you want to use:

- **Modify the `environment.yml` file** to add them to the list.
    - If the package can be installed with `conda`, then add it to the main list below `dependencies:`.
    - If the package can only be installed with `pip`, then add it to the secondary list below `- pip:`
- If you use Anaconda Navigator:
    - **Remove the old `pp-proj2` environment** in Anaconda Navigator, by clicking on it in the list of environments, and selecting "Remove" at the bottom.
    - **Import the (new) `environment.yml`** into Anaconda Navigator to re-create the environment `pp-proj2` with the new packages you've added.
- If you use the terminal:
    - Run the command `conda env update -f path/to/environment.yml`.
- **Activate** `pp-proj2` before launching Jupyter again.

Alternatively, you could also create a new environment with a different name, if you'd like to keep the original one! Just change the `name:` field in `environment.yml` and follow the instructions from the [Week 8 workshop](https://github.com/pypr-2122/pp-w08-workshop) to set it up. In any case, **make sure to include your `environment.yml` file in your repository when you submit.**

Here are a few packages you might find useful:

- If you choose to visualise anything on a map (e.g. using latitudes/longitudes of stations), packages like [folium](https://python-visualization.github.io/folium/) or [geopandas](https://geopandas.org/) might be useful.
- If you fancy making interactive visualisations, with things like toggle buttons or sliders, you could look into [IPython widgets](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Basics.html). (This is how the "Reveal solutions" buttons are made in your tutorial notebooks, for example.)
- If you work with weather data, you could use the [Meteostat Python package](https://dev.meteostat.net/python/).

---

---

### Marking scheme

Your project will be marked on 4 criteria:

- Code and implementation (12 marks)
- Quality and depth of investigation (16 marks)
- Presentation and cohesion of the report (8 marks)
- Code comments, docstrings, code style and readability (4 marks)

The detailed marking scheme is available in your repositories under `project-2-markingscheme.md`.


### Providing references

Most of the content of your submission must be **authored by your group**. That being said, you may use any code from the course material (e.g. workshop tasks, tutorial sheets, videos), without citing it.

You may also use **small pieces of code** (a few lines max at a time) that you found elsewhere -- e.g. examples from the documentation, a textbook, forums, blogs, etc... You may use this code *verbatim* (i.e. almost exactly as you found it), or adapt it to write your own solution.

A programming assignment is just like any other academic assignment -- and therefore, **you must provide a citation for any such code**, whether you use it *verbatim* or adapt it. To do so, include a code comment at the start of your script or notebook cell, indicating:
- the line numbers where the code was used or adapted,
- the URL of the source (or, if it's from a book, a full reference to the book),
- the date you accessed the source,
- the author of the code (if the information is available).

You can use this template -- delete one of the URL or book reference lines as appropriate:
```python
# Lines X-Y: Author Name
# URL: http://...
# Book Title, year published, page number.
# Accessed on 20 Nov 2021.
```

You must also provide **detailed code comments** for any such code, in your own words, to demonstrate that you fully understand how it works -- you will lose marks if you use external code without explaining it, even if it's cited correctly.

Remember to exercise caution if you use any code from external sources -- there are a lot of blogs and forums out there with very bad code! I'd recommend that you review the Week 4 video on searching the documentation.

Of course, any **non-code sources** that you used for any of your work should also be cited appropriately. You can have a "**References**" section at the end of the notebook, in a Markdown cell, to give your list of references for such sources.

With all that, we trust that you'll be able to use your best judgement, and to cite your sources appropriately -- if anything is not clear, please do ask. Note that **all submissions** will be automatically checked (and manually reviewed) for plagiarism and collusion (between groups), and [the University's academic misconduct policy](https://www.ed.ac.uk/academic-services/staff/discipline/academic-misconduct) applies.
