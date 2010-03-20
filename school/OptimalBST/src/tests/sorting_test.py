# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
import random
from OptimalBST.quicksort import quicksort

class  Sorting_TestCase(unittest.TestCase):
    def setUp(self):
        self.arrays = []
        for i in range(100):
            new_range = random.randint(2, 1000)
            new_array = random.sample(xrange(10000000), new_range)
            self.arrays.append(new_array)
    

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_sorting_(self):
        for array in self.arrays:
            original_length = len(array)
            quicksort(array)
            # print array

            self.assertTrue(original_length == len(array), "Lengths are not the same.")
            
            for i in range(len(array)-1):
                self.assertTrue(array[i] <= array[i+1], "Ordering is not correct!")

        

if __name__ == '__main__':
    unittest.main()

