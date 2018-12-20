import pandas as pd
import numpy as np
from efficient_apriori import apriori
import os

os.chdir('./Data')
train = pd.read_csv('./train.csv', sep='\t')

user_id = train.user_id.unique()
for u in user_id:
    order_number = train[(train.user_id == u)].order_number.unique()
    ass_rul_eff = []
    for o in order_number:
        product_id = train[(train.user_id == u) & (train.order_number == o)].product_id.tolist()
        temp = tuple(product_id)
        ass_rul_eff.append(temp)
    itemsets, rules = apriori(ass_rul_eff, min_support=0.6,  min_confidence=1)
    rules_rhs = filter(lambda rule: len(rule.lhs) == 1 and len(rule.rhs) == 1, rules)
    for rule in sorted(rules_rhs, key=lambda rule: rule.lift):
        if len(order_number) > 4:
            print(f'User id: {u} with rule {rule}')


