price(veg_burger, 7).
contains(veg_burger, bun).
contains(veg_burger, lettuce).
contains(veg_burger, tomato).
contains(veg_burger, patty).
price(cheese_pizza, 12).
contains(cheese_pizza, dough).
contains(cheese_pizza, cheese).
contains(cheese_pizza, tomato_sauce).
price(pepperoni_pizza, 15).
contains(pepperoni_pizza, dough).
contains(pepperoni_pizza, cheese).
contains(pepperoni_pizza, tomato_sauce).
contains(pepperoni_pizza, pepperoni).
valid(X) :- price(X, _), not invalid(X).
#show valid/1.
