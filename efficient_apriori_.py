import pandas as pd
from efficient_apriori import apriori
import os

os.chdir('./Data')

train = pd.read_csv('./train.csv', sep='\t')

ass_rul_df = pd.DataFrame()
user_id = train.user_id.unique()
dataList=[]
for u in user_id:
    order_number = train[(train.user_id == u)].order_number.unique()
    ass_rul_eff = []
    for o in order_number:
        product_id = train[(train.user_id == u) & (train.order_number == o)].product_id.tolist()
        temp = tuple(product_id)
        ass_rul_eff.append(temp)
    itemsets, rules = apriori(ass_rul_eff, min_support=0.5,  min_confidence=1)
    rules_rhs = filter(lambda rule: len(rule.lhs) == 1 and len(rule.rhs) == 1, rules)
    for rule in sorted(rules_rhs, key=lambda rule: rule.lift):
        if len(order_number) >= 4:
            temp_df = pd.DataFrame(data=[[u, rule.lhs[0], rule.rhs[0], rule.confidence, rule.support, rule.lift]],
                                   columns=['user_id', 'rule_lhs', 'rule_rhs', 'confidence', 'support', 'lift'])
            ass_rul_df = ass_rul_df.append(temp_df, ignore_index=True)
ass_rul_df.to_csv('./association_rules.csv', sep='\t', encoding='utf-8', index=False)
