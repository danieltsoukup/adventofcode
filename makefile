.PHONY: files add

# create files for the day
files:
	touch "inputs/day$(day).txt"
	
	echo "INPUT_FILE='inputs/day$(day).txt'" > "code/day$(day)_part1.py"
	cat code/template >> "code/day$(day)_part1.py"
	
	echo "INPUT_FILE='inputs/day$(day).txt'" > "code/day$(day)_part2.py" 
	cat code/template >> "code/day$(day)_part2.py"
	
# add new code and inputs to git
add:
	git add code/* inputs/*
 