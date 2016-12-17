import matplotlib.pyplot as plt

results_file = open('result.txt', 'r')

x_values = []
y_values = []

for line in results_file:
    nobrackets = (line.replace("(","")).replace(")","")
    values = nobrackets.split(",")

    x_values.append(values[0])
    y_values.append(values[1])

plt.plot(x_values,y_values)
plt.show()
