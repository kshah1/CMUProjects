#Karan Shah
#Assignment 6

# Template for writing MapReduce programs using mrjob
# % python mrjob-template.py <input file>  -q

from mrjob.job import MRJob
from mrjob.step import MRStep

# change the name of the class
class MR_program(MRJob):

    def mapper(self, _, line):
        # yield key, value
        line = line.replace(':','').split()
        friend, *network = line
        pairs = (sorted((friend, person)) for person in network) #creates sorted pair 

        for pair in pairs:
            yield pair, network #output of mapper is each pair and their network

    def reducer(self, key, values):  # values is a generator
        lst1, lst2 = values
        intersection = list(set(lst1) & set(lst2))
        yield key, sorted(intersection)


if __name__ == '__main__':
    # change to match the name of the class
    MR_program.run()