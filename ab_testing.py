#####################################################
# Comparison of AB Test and Conversion of Bidding Methods
#####################################################

#####################################################
# Business Problem
#####################################################

# Facebook recently introduced a new bidding type called "average bidding" as an alternative to the existing "maximum bidding" bidding type. 
# One of our clients, bombabomba.com, has decided to test this new feature to determine whether average bidding brings in more conversions than maximum bidding. 
# The A/B test has been running for one month, and bombabomba.com now expects you to analyze the results of this A/B test.
# The ultimate success metric for bombabomba.com is "Purchase." Therefore, the focus should be on the "Purchase" metric for statistical testing.


#####################################################
# The story of the dataset
#####################################################

In this data set, which includes the website information of a company, there is information such as the number of advertisements that users see and click, 
# as well as earnings information from here. There are two separate data sets, the control and test groups. These datasets are in separate sheets of 
# the ab_testing.xlsx Excel. Maximum Bidding was applied to the control group and Average Bidding was applied to the test group.

# Variables:

# Impression: Number of ad views
# Click: Number of clicks on the displayed ad
# Purchase: Number of products purchased after ads clicked
# Earning: Earnings after purchased products


#####################################################
# Project Tasks
#####################################################

####################### ####
# AB Testing (Independent Two Sample T Test)
####################### ####

# 1. Establish Hypotheses
# 2. Assumption Checking
# 2.1. Normality Assumption (shapiro)
# 2.2 Variance Homogeneity (levene)
# 3. Application of Hypothesis
# 3.1. Independent two sample t test if assumptions are met
# 3.2. Mannwhitneyu test if assumptions are not met
# 4. Interpret the results according to the p-value
# Note:
# - If normality is not achieved, direct number 2. If variance homogeneity is not achieved, argument number 1 is entered.
# - It may be useful to perform outlier review and correction before normality review.


#####################################################
# Task 1: Preparing and Analyzing Data
#####################################################

# Library Imports and Dataset Reading

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Step 1: Step 1: Read the dataset ab_testing_data.xlsx consisting of control and test group data.
# Assign control and test group data to separate variables.

control_df = pd.read_excel("ABTesti/ab_testing.xlsx", sheet_name="Control Group")
test_df = pd.read_excel("ABTesti/ab_testing.xlsx", sheet_name="Test Group")

df_control = control_df.copy()
df_test = test_df.copy()

# Step 2: Analyze control and test group data.

def check_df(dataframe, head=5):
    print("###################### SHAPE #########")
    print(dataframe.shape)
    print("###################### TYPES #########")
    print(dataframe.dtypes)
    print("###################### HEAD #########")
    print(dataframe.head())
    print("###################### TAIL #########")
    print(dataframe.tail())
    print("###################### NA #########")
    print(dataframe.isnull().sum())
    print("###################### SUMMARY STATISTICS #########")
    print(dataframe.describe().T)
check_df(df_control)
check_df(df_test)


# Step 3: After the analysis process, combine the control and test group data using the concat method.

df_control["Group"] = 'Control'
df_test["Group"] = 'Test'
df_control.head()

df = pd.concat([df_control, df_test], axis=0, ignore_index=True)
df.head(50)


#####################################################
# Task2: Defining the Hypothesis of A/B Testing
#####################################################

# Step 1: Define the hypothesis.

# H0: M1 = M2 (There is no statistically significant difference between the purchasing averages of the control group and the test group.)
# H1: M1 != M2 (There is a statistically significant difference between the purchasing averages of the control group and the test group.)


# Step 2: Analyze the purchase (earning) averages for the control and test group.

df.groupby('Group').agg({'Purchase': "mean"})


#####################################################
# Task3: Performing Hypothesis Testing
#####################################################

######################################################
# AB Testing
######################################################

# Step 1: Perform hypothesis checks before hypothesis testing.
# These are Assumption of Normality and Homogeneity of Variance. Test separately whether the control and test groups
# comply with the assumption of normality over the Purchase variable.

############################
# Normality Assumption
############################

# H0: Normal distribution assumption is provided.
# H1: Normal distribution assumption is not provided.
# p < 0.05 H0 REJECT , p > 0.05 H0 CANNOT REJECT


test_stat, test_pvalue = shapiro(df.loc[df['group'] == 'control', 'Purchase'])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, control_pvalue))
# Test Stat = 0.9773, p-value = 0.5891

test_stat, test_pvalue = shapiro(df.loc[df['group'] == 'test', 'Purchase'])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, test_pvalue))
# Test Stat = 0.9589, p-value = 0.1541


# Note: 
# The p-value of the Control Group and Test Group is above 0.05. In this case, we cannot reject the H0 hypothesis. The assumption of normality is provided.


############################
# Variance Homogeneity
############################

# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.
# p < 0.05 H0 REJECT , p > 0.05 H0 CANNOT REJECT

test_stat, pvalue = levene(df.loc[df["Group"] == "Control", "Purchase"],
                           df.loc[df["Group"] == "Test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 2.6393, p-value = 0.1083

# Note: 
# Since the p-value is greater than 0.05, we cannot reject the H0 hypothesis. In this case, the variance is homogeneous.


# Step 2: Select the appropriate test according to the Normality Assumption and Variance Homogeneity results.

################  ANSWER  #######################
# Since both assumptions are satisfied, we will apply the independent two-sample t-test (parametric test).


# Step 3: Considering the p_value obtained as a result of the test, interpret whether there is a statistically
# significant difference between the purchasing averages of the control and test groups.

test_stat, pvalue = ttest_ind(df.loc[df["Group"] == "Control", "Purchase"],
                              df.loc[df["Group"] == "Test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9416, p-value = 0.3493

################  ANSWER #######################
# p-value = 0.3493
# The p-value value is greater than 0.005. In this case, we cannot reject the HO hypothesis. 
# This shows that there is no statistically significant difference between the purchasing averages of the control and test groups.


##############################################################
# Task 4: Analysis of Results
##############################################################

# Step 1: Which test did you use, state the reasons.
###################### ANSWER ##############################
# In the Normality Assumption stage, we used the Shapiro method in the Scipy library,
# In the Variance Homogeneity stage, we used the Levene method from the Scipy Library and
# We saw that the p-values we obtained satisfied the assumptions and decided that an independent two-sample t-test (parametric test) was appropriate.



Step 2: Advise the customer according to the test results you have obtained.
###################### ANSWER ##############################
# As a result, there is no statistically significant difference in the A/B test that bombabomba.com conducted to test a new feature. 
# Since there is no significant difference, we can recommend the customer to use both methods.
