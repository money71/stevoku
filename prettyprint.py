'''prettyprint.py

Pretreat strings with ANSI formatting control sequences
'''

import re

# format code constants
RESET = 0
BOLD = 1
TEXT_RED = 31
TEXT_GREEN = 32
TEXT_YELLOW = 33
TEXT_BLUE = 34
TEXT_MAGENTA = 35
TEXT_CYAN = 36
BG_RED = 41
BG_GREEN = 42
BG_YELLOW = 43
BG_BLUE = 44
BG_MAGENTA = 45
BG_CYAN = 46


def format(text, *codes):

	'''Format text with the given ANSI SGR codes

	Merges with existing format lists if possible
	'''

	# null operations
	if text == '' or len(codes) == 0:
		return text

	# check if text already contains control sequence
	match = re.match('^\033\[(\d{1,3}(?:;\d{1,3})*)m(.*)\033\[0m', text)
	if match:
		existingCodes = set(match.group(1).split(';'))
		newCodes = existingCodes.union(set(codes))
		startCode = '\033[{}m'.format( ';'.join([str(i) for i in newCodes]) )
		endCode = '\033[0m'

	else:
		startCode = '\033[{}m'.format( ';'.join([str(i) for i in codes]) )
		endCode = '\033[0m'

	return startCode + text + endCode


def bold(text):
	return format(text, BOLD)

