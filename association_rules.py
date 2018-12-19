import pandas as pd
import numpy as np
import os

os.chdir('./Data')
train = pd.read_csv('./train.csv', sep='\t')

user_id = train.user_id.unique()
for u in user_id:
    product_id = train[train.user_id == u].product_id.unique().tolist()
    total_order = len(train[train.user_id == u].order_number.unique())
    arr = np.zeros((total_order, len(product_id))).astype(int)
    order_number = train[(train.user_id == u)].order_number.unique()
    for o in order_number:
        for p in product_id:
            if not (train[(train.user_id == u) & (train.order_number == o) & (train.product_id == p)]).empty:
                arr[o-1, product_id.index(p)] = 1

    ass_rul_df = pd.DataFrame(data=arr, index= list(range(0, total_order, 1)),columns=product_id).astype(int)
    # TODO: Association Rules Mining for user u.
