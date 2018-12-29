import os
from collections import Counter
import pandas as pd
import numpy as np

# Path configuration
os.chdir('./Data/')

test = pd.read_csv('./testx.csv', sep='\t')
order_number_test = []
for u in test.user_id.unique():
    order_number_test.append(len(test[test.user_id == u].order_number.unique().tolist()))
    print(test[test.user_id == u].order_number.unique().tolist())
    print(len(test[test.user_id == u].order_number.unique().tolist()))
print(order_number_test, type(order_number_test))
print(Counter(order_number_test))
