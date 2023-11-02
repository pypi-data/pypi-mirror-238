# Title: BioBeee
BioBeee: A bioinformatics tool for scrapping data from various types of Biological Databases using python programs for creating biological datasets also provides pre-processing and analysis on it. 
 
# Introduction
Simply, Bioinformatics is the interdisciplinary field of computer science and information technology that’s use to analysing, storing and managing biological data. These biological data such as DNA, RNA, protein and some small molecule or drug molecule and information related to those drugs (i.e., pharmacokinetic, pharmacodynamic properties) stored in the large cloud database. 
Drug Bank, EMBL-EBI (European Bioinformatics Institute), Uniprot, NCBI (National Center for Biotechnology Information) are some of the major databases I will use in this program.
Drug bank is a comprehensive, free-to-access, online database containing information on drugs and drugs and drug targets. Drug Bank started in 2006 in Dr. David Wishart’s lab at the University of Alberta. It began as a project to help academic researchers get detailed structured information about drugs. In 2011 it became a part of The Metabolomics Innovation Center (TMIC). The project continued to grow in scope and popularity and was spun out into OMx Personal Health Analytics Inc in 2015.(
https://go.drugbank.com/about).

EMBL-EBI is international, innovative and interdisciplinary, and a champion of open data in the life sciences. We are part of the European Molecular Biology Laboratory (EMBL), an intergovernmental research organisation funded by over 20 member states, prospect and associate member states. We are situated on the Wellcome genome campus near Cambridge, UK, one of the world’s largest concentrations of scientific and technical expertise in genomics. (https://www.ebi.ac.uk/about).

The National Center for Biotechnology Information advances science and health by providing access to biomedical and genomic information. (https://www.ncbi.nlm.nih.gov/).

In this project work I will try to create a basic tool in python programming for retrieving data from some of these biological databases.

# Objectives
•	Analysing API’s that is provided by the different databases to access it by their HTML or XML programs.\
•	Creating a request method to generate queries.\
•	Extracting essential information from responded HTML and XML by regular expression.\
•	Providing different file formats like, txt, data, csv, tsv to store extracted information.

# Justification
•	To provides easier a method for access biological databases by programmatically.\
•	It will be highly reusable, smother to retrieve data and store it into csv or txt files\
•	Provide some other analysis and pre-processing on various biological data for machine learning & deep learning tasks.

Mostly, I ‘m focused on providing a way to analyse RNA, DNA, protein sequence for users can create biological dataset from python package and also can pre-process it.
# Materials
•	Python >= 3.x\
•	Requests module >= 2.28.1\
•	SQLite DB >= 3.7.15\
•	Beautifullsoup4 module >= 4.11.1\
•	Entrez Direct (available on Linux Macintosh only)

# Method
•	By the python programming I will scrap data from website through request module and store variable in the string, just find the tags with beautiful soup 4 or regular expression.\
•	I can also try to provide analysis such as; graphs, language processing for sequence, vectorizations etc, and pre-processing on that retrieved data to prepare datasets for ML and DL.

![workflow](https://gitlab.com/aniket4033426/mini_project/-/raw/main/miniworkflow.png?ref_type=heads) 

# Expected Outputs
•	Suppose, we need to get the id of a drug like; “morphine” with name of the drug:
   
    def DID(drug_name):
        '''Search for drug-by-drug name from drug bank database\nreturns very first drug ID from drug list
        \nupdated method of 'drug_ID' function in some times drug_ID method doesn't work, in this case you can use this method'''

        try:
            url = f'https://go.drugbank.com/unearth/q?query={drug_name}&button=&searcher=drugs'
            soup = BeautifulSoup(requests.get(url).text, 'lxml')
            id_list = []
            for dd in soup.find('dd', {'class': 'col-xl-4 col-md-9 col-sm-8'}):
                id_list.append(dd.get_text())
            return id_list[0]
        except:
            return '%s\nprobabilly wrong or spell mistake' %exception

    drug_IDs = DID('morphine')
    print(drug_IDs)
Output: 
    DB00295

•	We have another example of this where we are finding the IUPAC name of drug by their drug bank id:

    class drug_info():

        def __init__(self, drugBank_ID):
            self.id = drugBank_ID

        def drug_detail(self):
            try:
                url = 'https://go.drugbank.com/drugs/%s' %self.id
                soup = BeautifulSoup(requests.get(url).text, 'lxml')
                (key_lis, value_lis) = ([], [])
                for dt, dd in zip(soup.select('.card-content dl dt'), soup.select('.card-content dl dd')):
                    key_lis.append(dt.string)
                    value_lis.append(dd.string)
    
                data = {key_lis[i]: value_lis[i] for i in range(len(key_lis))}
                return data
            except:
                return exception
        def IUPAC_name(self):
            data = self.drug_detail()
            return data['IUPAC Name']

    print(drug_info('DB00316').IUPAC_name())
Output:
    N-(4-hydroxyphenyl) acetamide
