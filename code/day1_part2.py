import heapq

sum_heap = []

line_id = 0
current_sum = 0

with open("inputs/day1.txt", "r") as file:
    for line in file:
        if line == "\n":
            # update heap with negative sum
            heapq.heappush(sum_heap, -current_sum)
            # reset current
            current_sum = 0
        else:
            # update current
            current_sum += int(line)
        
        line_id += 1

# get sum of top 3
result = 0
for _ in range(3):
    result += heapq.heappop(sum_heap)

print(-result)