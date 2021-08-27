# songwriter.py
# Match rhyme and meter between lines of source text to generate song verses
# Syllable estimator: https://pypi.org/project/syllables/
# Rhyming dictionary: https://github.com/jameswenzel/Phyme

from Phyme import Phyme # pip install phyme
import syllables # pip install syllables
import re

# lyricDict will contain a lyric dictionary built from the source text
# The key will be the last word of each line
# The value will be a two-dimensional list:
#   element 0, a two-dimentional list of every line ending in that word
#      element 0, the line text itself
#      element 1, the number of syllables estimated in that line
#   element 1, a two-dimentional list of every known rhyme with that word:
#      element 0, the rhyme word
#      element 1, the type of rhyme:
#                 0 = Perfect rhyme (FOB, DOG)
#                 1 = same vowels and consonants of the same type regardless of voicing (HAWK, DOG)
#                 2 = same vowels and consonants as well as any extra consonants (DUDES, DUES)
#                 3 = same vowels and a subset of the same consonants (DUDE, DO)
#                 4 = same vowels and some of the same consonants, with some swapped for other consonants (FACTOR, FASTER)
#                 5 = same vowels and arbitrary consonants (CASH, CATS)
#                 6 = not the same vowels but the same consonants (CAT, BOT)
#                 so, the higher this index, the less "rhymey" is it, kinda

lyricDict = {}

if __name__ == "__main__":

	# Read the entire source file in to a string for later splitting and manipulation
	# This is very inefficient but hello-world quality for now
	# Read in and kill the newlines because they're unimportant
	sourceTextFile = open('bible.txt', 'r') # some public domain text as a test case
	sourceTextBlob = sourceTextFile.read().replace('\n', ' ')
	sourceTextFile.close()

	sourceSentences = re.split('[,.!]', sourceTextBlob) # Break it apart at every comma,period,ep
	
	for sourceSentence in sourceSentences:

			if len(sourceSentence) > 1: # Empty elements get caught up in here and crash, look for >1 element sentences only

				sourceSentence = sourceSentence.strip()
				sourceSentenceWords = sourceSentence.split()
				lastWord = sourceSentenceWords[-1]

				sourceSentenceSyllables = 0
				for sourceSentenceWord in sourceSentenceWords:
					sourceSentenceSyllables += syllables.estimate(sourceSentenceWord)

				#print("DEBUG -- sentence:", sourceSentence, " --- lastword:", lastWord, " --- syllables:", sourceSentenceSyllables)

				if not lastWord in lyricDict:
					# Haven't encountered this last word before, so build a lyricDict entry for this last word
					newLyric = {lastWord:[[sourceSentence, sourceSentenceSyllables]]}
					lyricDict.update(newLyric)
				#else:
					#print("DEBUG: found key in lyricDict:", lastWord)
					#print("lyricDict[lastWord][0]:",lyricDict[lastWord][0])
					#if sourceSentence not in lyricDict[lastWord][0]:
					#	lyricDict[lastWord][0].append([sourceSentence, sourceSentenceSyllables])
					#print(lyricDict[lastWord])
					#print(lyricDict[lastWord][1])
					#lyricDict[lastWord][1] += 1
	print(lyricDict)
