import pandas as pd
import numpy as np
from efficient_apriori import apriori
import os

os.chdir('./Data')
train = pd.read_csv('./train.csv', sep='\t')

user_id = train.user_id.unique()
for u in user_id:
    product_id = train[train.user_id == u].product_id.unique().tolist()
    total_order = len(train[train.user_id == u].order_number.unique())
    ass_rul_eff = []
    order_number = train[(train.user_id == u)].order_number.unique()
    for o in order_number:
        temp = []
        for p in product_id:
            if not (train[(train.user_id == u) & (train.order_number == o) & (train.product_id == p)]).empty:
                temp.append(p)
        temp = tuple(temp)
        ass_rul_eff.append(temp)
    itemsets, rules = apriori(ass_rul_eff, min_support=0.4,  min_confidence=1)
    rules_rhs = filter(lambda rule: len(rule.lhs) == 2 and len(rule.rhs) == 1, rules)
    for rule in sorted(rules_rhs, key=lambda rule: rule.lift):
            print(f'User id: {u} with rule {rule}')

# TODO: Association Rules Mining for user u.

