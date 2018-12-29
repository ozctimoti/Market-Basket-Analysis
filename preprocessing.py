import os
import csv
import numpy as np
import pandas as pd

# Path configuration
os.chdir('./Data/')

orders = []
with open('orders.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 4021:
            break
        if line_count == 0:
            line_count += 1
        elif line_count == 1:
            orders = row
            line_count += 1
        else:
            orders = np.vstack([orders, row])
            line_count += 1


val = ((orders[:, 2] == 'train').tolist())
test = ((orders[:, 2] == 'test').tolist())

val = orders[val, 1].tolist()
test = orders[test, 1].tolist()

prior_col = []
val_col = []
test_col = []

for i in range(orders.shape[0]):
    if (orders[i, 1] in val) & (orders[i, 2] == 'prior'):
        prior_col.append(i)
    elif (orders[i, 1] in val) & (orders[i, 2] == 'train'):
        val_col.append(i)
    elif orders[i, 1] in test:
        test_col.append(i)

train = orders[prior_col]
val = orders[val_col]
test = orders[test_col]

train = np.delete(train, [2, 4, 5], 1)
val = np.delete(val, [2, 4, 5], 1)
test = np.delete(test, [2, 4, 5], 1)

train[train == ''] = 0.0
train = train.astype(float).astype(int)
val = val.astype(float).astype(int)

test[test == ''] = 0.0
test = test.astype(float).astype(int)

train = pd.DataFrame(data=train, columns=['order_id', 'user_id', 'order_number', 'days_since_prior_order'])

user_id = train.user_id.unique()
for u in user_id:
        order_number = train[(train.user_id == u)].order_number
        same_day = 0
        for o in order_number[1:]:
            if train[(train.user_id == u) & (train.order_number == o)].days_since_prior_order.unique()[0] == 0:
                same_day += 1
            train.at[(train.user_id == u) & (train.order_number == o), 'order_number'] = o - same_day

val = pd.DataFrame(data=val, columns=['order_id', 'user_id', 'order_number', 'days_since_prior_order'])

train['days_since_first_order'] = pd.Series((np.zeros(len(train.user_id))))
train.days_since_first_order = train.days_since_first_order.astype(int)


val = pd.DataFrame(data=val, columns=['order_id', 'user_id', 'order_number', 'days_since_prior_order'])

# test = pd.DataFrame(data=test, columns=['order_id', 'user_id', 'order_number', 'days_since_prior_order'])

product_train = pd.read_csv('order_products__prior.csv', sep=',')
product_val = pd.read_csv('order_products__train.csv', sep=',')

product_train = product_train.drop('add_to_cart_order', axis=1)
product_val = product_val.drop('add_to_cart_order', axis=1)

product_train = product_train.apply(pd.to_numeric)
product_val = product_val.apply(pd.to_numeric)

train = pd.merge(train, product_train, how='inner', on=['order_id'])
val = pd.merge(val, product_val, how='inner', on=['order_id'])

order_days_since_first_order = []
user_id = train.user_id.unique()
for u in user_id:
    product_id = train[train.user_id == u].product_id.unique()
    days_since_prior_order = []
    for d in train[train.user_id == u].order_number.unique():
        days_since_prior_order.append(train[(train.user_id == u) & (train.order_number == d)].days_since_prior_order.unique()[0])
    order_days_since_first_order.append(sum(days_since_prior_order))
    for p in product_id:
        order_number = train[(train.user_id == u) & (train.product_id == p)].order_number
        same_day = 0
        last_order_sum = 0
        for o in order_number[1:]:
            train.at[(train.user_id == u) & (train.product_id == p) & (train.order_number == o), 'days_since_first_order'] \
                = sum(days_since_prior_order[0: o])

val['days_since_first_order'] = pd.Series((np.zeros(len(val.user_id))))
val.days_since_first_order = val.days_since_first_order.astype(int)

user_id = train.user_id.unique()
i = 0
for u in user_id:
    val.at[val.user_id == u, 'days_since_first_order'] = order_days_since_first_order[i] + int(val[(val.user_id == u)].days_since_prior_order.unique()[0])
    i += 1

train.to_csv('./train.csv', sep=',', encoding='utf-8', index=False)
val.to_csv('./test.csv', sep=',', encoding='utf-8', index=False)

# test.to_csv('./test.csv', sep=',', encoding='utf-8', index=False)
