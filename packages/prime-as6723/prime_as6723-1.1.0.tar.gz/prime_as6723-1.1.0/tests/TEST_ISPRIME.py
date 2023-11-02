#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os

# Get the current working directory
current_directory = os.getcwd()

# Print the current working directory
print("Current Working Directory:", current_directory)


# In[7]:


import os

# Specify the new directory path
new_directory = r'C:\Users\arush\yay\prime_as6723'

# Change the working directory
os.chdir(new_directory)

# Confirm the new working directory
current_directory = os.getcwd()
print("New Working Directory:", current_directory)


# In[8]:


import math

def is_prime(n):
    """
    To check if a number is prime or not.

    Its inputs are integers and outputs are 'True' or 'False' depending on whether the input integer is prime or not respectively. 
    
    Example:
        1) is_prime(7)
        True

        2) is_prime(9)
        False
    """
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


# In[10]:


import pytest


# In[11]:


# Defining the test cases with input numbers and expected results
test_cases = [
    (2, True),    # 2 is a prime number
    (7, True),    # 7 is a prime number
    (8, False),   # 8 is not a prime number
    (9, False),   # 9 is not a prime number
    (-1, False),  # -1 is not a prime number
    (0, False),   # 0 is not a prime number
    (1, False),   # 1 is not a prime number
]

# Creating the test_is_prime_param function to run the test cases
@pytest.mark.parametrize("number, expected_result", test_cases)
def test_is_prime_param(number, expected_result):
    assert is_prime(number) == expected_result 


# In[ ]:





# In[ ]:




