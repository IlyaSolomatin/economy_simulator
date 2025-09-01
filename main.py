import numpy as np
from matplotlib import pyplot as plt

class Dude():

    def __init__(self, params):
        self.job = params['job']
        self.age = params['age']
        self.account = 0
        self.goods_stock = 0
        self.alive = True

# init: 1000 dudes working for government, with 3k monthly salary
# 300 farmers, producing 5 units of food monthly at initial price 1k per unit
# 10% vat tax, 10% salary tax

n_clerks = 1000
n_farmers = 300
vat = 0.1
inc_tax = 0.1
gvt_salary = 3000
food_price = 1000
food_prod = 5

gvt_spending = 0
gvt_income = 0
population = [Dude({'job': 'gvt', 'age': np.random.normal(loc=27)}) for _ in range(n_clerks)]
population += [Dude({'job': 'farm', 'age': np.random.normal(loc=27)}) for _ in range(n_farmers)]

while True:
    # clerks receive salaries
    for p in population:
        if p.job == 'gvt':
            p.account += gvt_salary * (1 - inc_tax)
            gvt_spending += gvt_salary
            gvt_income += gvt_salary * inc_tax

    # farmers make food
    for p in population:
        if p.job == 'farm':
            p.goods_stock += food_prod - 1

    # farmers bring all food to the barn
    food_stock = 0
    for p in population:
        if p.job == 'farm':
            food_stock += p.goods_stock
            p.goods_stock = 0

    # clerks make a random queue and buy out the food they need (if they can)
    food_revenue = 0
    for p in np.random.permutation(population):
        if p.job == 'gvt':
            if p.account >= food_price and food_stock >= 1:
                p.account -= food_price
                p.account -= food_price * vat
                gvt_income += food_price * vat
                food_revenue += food_price
                food_stock -= 1
            else:
                p.alive = False

    p = 0
    while True:
        if not population[p].alive:
            del population[p]
        else:
            p += 1
            if p >= len(population):
                break

    # farmers distribute collected money and unsold stock
    actual_n_farmers = sum([1 for p in population if p.job == 'farm'])
    for p in population:
        if p.job == 'farm':
            p.account += food_revenue / actual_n_farmers
            p.goods_stock = food_stock / actual_n_farmers

    # everyone ages
    for p in population:
        p.age += 1/12
