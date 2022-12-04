.PHONY: files add inputs

# create files for the day
files: inputs
	echo "INPUT_FILE='inputs/day$(day).txt'" > "code/day$(day)_part1.py"
	cat code/template >> "code/day$(day)_part1.py"
	
	echo "INPUT_FILE='inputs/day$(day).txt'" > "code/day$(day)_part2.py" 
	cat code/template >> "code/day$(day)_part2.py"

inputs:
	curl --cookie session="$(sessionid)" "https://adventofcode.com/2022/day/$(day)/input" > "inputs/day$(day).txt"

# add new code and inputs to git
add:
	git add code/* inputs/*
