#Karan Shah
#Assignment 6

# Template for writing MapReduce programs using mrjob
# % python mrjob-template.py <input file>  -q

from mrjob.job import MRJob
from mrjob.step import MRStep

# change the name of the class
class MR_program(MRJob):

    def mapper(self, _, line):
        line = line.split()
        
        for el in line:
            yield int(el), line  

    def reducer_1(self, key, values):  # values is a generator
        # yield key, f(values)
        lst = list(values)
        val = len(lst)

        yield 'euler', (key, val) #key is euler so that when it is passed to reducer_2 the key,values will be aggregated to the key euler

    def reducer_2(self, key, values):  # values is a generator
        
        values = list(values)
        counter = 0  #counter used to count number of lines in file
        even_counter = 0 #counts the number of even degreed vertices
        for lst in values:
            first, second = lst
            if second % 2 == 0: 
                even_counter += 1
                counter += 1
            else:
                counter += 1

        if even_counter == counter: #checks if the number of even degreed vertices is the same as the number of lines in the text
            values += [["euler", True]] 
        else:
            values += [["euler", False]]

        for el in values:
            first, second = el
            yield first, second 

    def steps(self): #multi-step jobs
        return [MRStep(mapper=self.mapper)] + \
                [MRStep(reducer=self.reducer_1)] + \
                [MRStep(reducer=self.reducer_2)]



if __name__ == '__main__':
    # change to match the name of the class
    MR_program.run()