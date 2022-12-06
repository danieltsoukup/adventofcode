import string

letter_to_score = dict(zip(string.ascii_lowercase, range(1, 27)))
letter_to_score.update(dict(zip(string.ascii_uppercase, range(27, 53))))

total_score = 0
with open("inputs/day3.txt", "r") as file:
    for line in file:
        line = line.strip()

        idx = len(line) // 2
        comp_1, comp_2 = line[:idx], line[idx:]
        overlap = set(comp_1).intersection(set(comp_2))

        for letter in overlap:
            total_score += letter_to_score[letter]

print(total_score)
