#Karan Shah
#Assignment 6

# Template for writing MapReduce programs using mrjob
# % python mrjob-template.py <input file>  -q

from mrjob.job import MRJob
from mrjob.step import MRStep

# change the name of the class
class MR_program(MRJob):

    def mapper(self, _, line):
        if '?' in str(line):
            anagram = '?' + line.replace('?','').strip()
        else:
            anagram = line.strip()
        
        word = line.replace('?','').strip()
        sorted_word = "".join(sorted(word))

        yield sorted_word, anagram

            

    def reducer(self, key, values):  # values is a generator
        lst = list(values)
        
        if any('?' in el for el in lst): #condition allows output to only be for the jumble.txt and not the sowpods.txt
            key = len(lst)
            yield key, lst

if __name__ == '__main__':
    # change to match the name of the class
    MR_program.run()
    
