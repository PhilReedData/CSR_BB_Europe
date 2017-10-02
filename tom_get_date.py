import fileinput, re

lower_limit = 2000
upper_limit = 2020
match_limit = 10

# Process a file and try to guess the date
# python get_date.py 2000_40_GB0002162385_CR1.txt
years = {}
count = 1
for line in fileinput.input(openhook=fileinput.hook_encoded("iso-8859-1")):
	results = re.findall('[^\d](\d{4})(?:[\-\/](\d{4}|\d{2}))?[^\d]', line)
	for result in results:
		match_number = 0
		if (result[1] == ''):
			# Single number match
			match_number = int(result[0])
		else:
			# Range match - take the last number and pad to 4 digits
			if len(result[1]) == 2:
				match_number = int('20' + result[1])
			else:
				match_number = int(result[1])

		# Filter and record a weighted score (earlier results count for more)
		if match_number >= lower_limit and match_number <= upper_limit:
			score = 1.0 / count
			count += 1
			
			if match_number in years:
				years[match_number] += score
			else:
				years[match_number] = score

			# Only process the first few matches
			if count == match_limit:
				break;
	if count == match_limit:
		break;

# Output the sorted results and scores
sorted_years = sorted(years, key=years.get, reverse=True)
for sorted_year in sorted_years:
	print(sorted_year, years[sorted_year])