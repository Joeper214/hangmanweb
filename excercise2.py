cars = 100
space_in_a_car = 4.0
drivers = 30
passengers = 90
cars_not_driven = cars - drivers
cars_driven = drivers
carpool_capacity = cars_driven * space_in_a_car
average_passengers_per_car = passengers / cars_driven

print "There are", cars, "cars available."
print "There are only", drivers, "drivers available."
print "There will be", cars_not_driven, "empty cars today."
print "We can transport", carpool_capacity, "people today."
print "We have", passengers, "to carpool today."
print "We need to put about", average_passengers_per_car, "in each car."


print "\n\n"
my_name = "Rich"
my_age = 25
my_height = 74 #inches
my_weight = 64.10 * 2.204 #lbs
# %r is used for debugging
print "Let's talk about %s." % my_name
print "My age %r" % my_name
print "If I add %d, %d, and %d I get %d." % (my_age, my_height, my_weight, my_age + my_height + my_weight)

hilarious = False
joke_evaluation = "Isn't that joke so funny?! %r"

print joke_evaluation % hilarious

w = "This is left side..."
e = "a string with right side"

print w + e

print "\n\nexcercise 7\n\n"

print "." * 10

end1 = "Cheese"
end2 = "and"
end3 = "Burger"

print end1 + end2
print end3
