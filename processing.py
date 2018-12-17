import os
import pandas as pd
import numpy as np

# Path configuration
os.chdir('./Data/')

train = pd.read_csv('./train_middle.csv', sep='\t')
# test = pd.read_csv('./test_middle.csv', sep='\t')

'''
train[(train.user_id == u) & (train.product_id == p)])
print(train.query('user_id == u & product_id == p').order_number)
order_number = train[train[train.user_id == u].product_id == p].order_number.unique() # NOT WORKED
order_number = train.query('user_id == u & product_id = p') # NOT WORKED
'''

train['days_since_first_order'] = pd.Series((np.zeros(len(train.user_id))))
train.days_since_first_order = train.days_since_first_order.astype(int)

user_id = train.user_id.unique()
for u in user_id:
    product_id = train[train.user_id == u].product_id.unique()
    days_since_prior_order = []
    for d in train[train.user_id == u].order_number.unique():
        days_since_prior_order.append(train[(train.user_id == u) & (train.order_number == d)].days_since_prior_order.unique()[0])
    for p in product_id:
        order_number = train[(train.user_id == u) & (train.product_id == p)].order_number
        same_day = 0
        last_order_sum = 0
        for o in order_number[1:]:
            train.at[(train.user_id == u) & (train.product_id == p) & (train.order_number == o), 'days_since_first_order'] \
                = sum(days_since_prior_order[0: o])

'''    
c = 0
for o in order_number[::-1]:
    if c == 0:
        train[(train.user_id == u) & (train.product_id == p) & (train.order_number == o)].next_order_day = 0
        next_o = o
        c += 1
    else:
        train.at[(train.user_id == u) & (train.product_id == p) & (train.order_number == o), 'next_order_day'] = sum(days_since_prior_order[o: next_o])
        train[(train.user_id == u) & (train.product_id == p) & (train.order_number == next_o)].days_since_prior_order = sum(days_since_prior_order[o: next_o])
        next_o = o
'''

train.to_csv('./train.csv', sep='\t', encoding='utf-8', index=False)
print(train)

