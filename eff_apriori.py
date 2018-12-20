import pandas as pd
import numpy as np
from efficient_apriori import apriori
import os

os.chdir('./Data')
train = pd.read_csv('./train.csv', sep='\t')

user_id = train.user_id.unique()
for u in user_id[5:]:
    order_number = train[(train.user_id == u)].order_number.unique()
    ass_rul_eff = []
    for o in order_number:
        product_id = train[(train.user_id == u) & (train.order_number == o)].product_id.tolist()
        temp = tuple(product_id)
        ass_rul_eff.append(temp)
    print(ass_rul_eff)
    itemsets, rules = apriori(ass_rul_eff, min_support=0.5,  min_confidence=1)
    rules_rhs = filter(lambda rule: len(rule.rhs) == 1, rules)
    for rule in sorted(rules_rhs, key=lambda rule: rule.lift):
            print(f'User id: {u} with rule {rule}')


