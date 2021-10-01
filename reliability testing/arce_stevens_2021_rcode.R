##
## Script name: arce_stevens_2021_rcode.R
##
## Purpose of script: This script analyzes the data investigating the reliability of a computer-controlled precision treat dispenser for canine research.
##
## Author: Jeffrey R. Stevens (jeffrey.r.stevens@gmail.com)
##
## Date Created: 2021-10-01
##
## Date Finalized: 2021-10-01
##
## License: All materials presented here are released under the Creative Commons Attribution 4.0 International Public License (CC BY 4.0).
##  You are free to:
##   Share — copy and redistribute the material in any medium or format
##   Adapt — remix, transform, and build upon the material for any purpose, even commercially.
##  Under the following terms:
##   Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
##   No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.
##
## ---
##
## Notes:
## Instructions: Place this file and the data files in the main directory.
##  At the R command prompt, type
## 	> source("arce_stevens_2021_rcode.R")
## 	This will run the script, adding all of the calculated variables to the workspace. 
##  If packages do not load properly, install them with install.packages("package_name").
##
## Data files:
## ---
## arce_stevens_2021_data.csv
##  dispenser - dispenser number (1-5)
##  expected - expected number of treats dispensed
##  actual - actual number of treats dispensed
##
## ---

# Load library and input data ------------------------------------------------------------

library(tidyverse)  # load tidyverse for data input and processing

data <- read_csv("arce_stevens_2021_data.csv") %>%  # input data
  mutate(error = actual - expected,  # create column of errors
         abs_error = abs(error))  # calculate the absolute value of errors

# Analyze data --------------------------------------------------------------

# Calculate accuracy and error rate for each dispenser
dispenser_data <- data %>% 
  group_by(dispenser) %>% 
  summarise(total = sum(expected),
            errors = sum(abs_error)) %>% 
  mutate(correct = total - errors,
         accuracy = correct / total * 100,
         error_rate = round(errors / total * 100, 1)) %>% 
  select(total, correct, errors, accuracy, error_rate)
  
dispenser_means <- dispenser_data %>% summarise(across(everything(), mean))

# Calculate accuracy and error rate for each number of expected treats
number_data <- data %>% 
  group_by(expected) %>% 
  summarise(total = sum(expected),
            errors = sum(abs_error)) %>% 
  mutate(correct = total - errors,
         accuracy = correct / total * 100,
         error_rate = round(errors / total * 100, 1)) %>% 
  select(total, correct, errors, accuracy, error_rate)
