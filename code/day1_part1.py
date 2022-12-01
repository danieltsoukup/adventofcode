line_id = 0
current_sum = 0
largest_sum = -1

with open("inputs/day1.txt", "r") as file:
    for line in file:
        if line == "\n":
            # update largest
            largest_sum = max(current_sum, largest_sum)
            # reset current
            current_sum = 0
        else:
            # update current
            current_sum += int(line)
        
        line_id += 1

print(largest_sum)