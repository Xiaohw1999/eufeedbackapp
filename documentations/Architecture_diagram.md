# Architecture

## design logic

The basic architecture design of the system:
![img.png](structure.png)

## data scraping pipline

![img.png](Dataupdatepipeline.png)

Pipeline description:

Pipeline: .github/workflows/scraping-job.yml

Folder: .src/scraping/ScrapingWithPDF/

Files: 
(1) functions: 

utilsScraping.py: Functions for scraping data from websites and storing it into MongoDB Atlas.

utilsPreprocessing.py: Functions for preprocessing metadata from MongoDB Atlas and restoring it.

(2) stages:





