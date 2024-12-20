# datascience
Readme for the project

0_Data_Import_ipnyb includes the API used for collecting data from ESIOS website, and some pre-processing of the data to then export it to csv format. It is not necessary to run this code as the csv files have already been downloaded in the /datas folder. 

/datas folder contains all the input files required to run the code. In addition to the data gathered through the API, it contains the gas prices for 2023 and 2024, gathered from MIBGAS website. 

1_Main_code.ipnyb is the main folder and contains all the model data, the methodology section of the report follows the same outline as the code. 

Please note that the blocks related to model fitting and hyperparametrization take significant time to run (around 15-25 minutes each).