.PHONY: files add inputs test

SESSIONID=`cat sessionid`

# create files for the day
# use as `make files year=2023 day=2`
files: inputs
	mkdir -p "$(year)/code"
	echo "INPUT_FILE='$(year)/inputs/day$(day).txt'" > "$(year)/code/day$(day)_part1.py"
	cat template >> "$(year)/code/day$(day)_part1.py"
	
	echo "INPUT_FILE='$(year)/inputs/day$(day).txt'" > "$(year)/code/day$(day)_part2.py" 
	cat template >> "$(year)/code/day$(day)_part2.py"

inputs:
	mkdir -p "$(year)/inputs"
	curl --cookie session="$(SESSIONID)" "https://adventofcode.com/$(year)/day/$(day)/input" > "$(year)/inputs/day$(day).txt"

# add new code and inputs to git
add:
	git add $(year)/code/* $(year)/inputs/*

test:
	pytest -s $(year)/code/test.py
