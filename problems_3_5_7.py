#  Adobe Programming Test Solution
#  Author:  Dan Stevens
#  Copyright: 11/18/2013
#  
#  This file contains solutions to the following three problems on
#  projecteuler.net:
# 
# Problem 3 -- Largest prime factor
# The prime factors of 13195 are 5, 7, 13 and 29.
# What is the largest prime factor of the number 600851475143 ?
# 
# Problem 5 -- Smallest multiple
# 2520 is the smallest number that can be divided by each of the numbers from 
# 1 to 10 without any remainder.
# What is the smallest positive number that is evenly divisible by all of 
# the numbers from 1 to 20?
# 
# Problem 7 -- 10001st prime
# By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that 
# the 6th prime is 13.
# What is the 10 001st prime number?

import sys
import test_data
import timeit

class SieveTooSmall(Exception):
     def __init__(self, size, prime_count, largest_prime, requested_count):
         self.size = size
         self.prime_count = prime_count
         self.largest_prime = largest_prime
         self.requested_prime = requested_count
     def __str__(self):
         return 'The sieve was initialized with a size of %d.  %d primes were found, the largest being %d, but the %dth prime was requested.' % ( self.size, self.prime_count, self.largest_prime, self.requested_prime)

class Sieve(object):
    ''' Implements a Sieve of Eratosthenes to find prime numbers.
        This object will throw SieveTooSmall if a prime number >= size is requested.'''

    def __init__(self, size):
        # The list of numbers.  If an element of the list is 0 then
        # it has been determined to be <2 or non-prime.
        self.size = max(16, size)
        self.sieve = [1] * self.size
        
        # Seed list of primes with 2
        self.primes = [2]

        # The point before which we have found and recorded primes.
        self.cursor = 3   
        self.sieve[1] = 0 # The number 1 is not prime.
        self.sieve[0] = 0 # The number 0 is not prime.

        # The 0-based element of the prime list whose multiples
        # are next to be removed from the sieve.
        self.applied_primes_cursor = 0

    def filter_list_of_multiples(self, factor):
        index = 0
        mults = range(self.filtered_until(), self.get_size(), factor)
        for i in mults:
            self.sieve[i] = 0

    def get_size(self):
        return self.size

    def filtered_until(self):
        ret = -1
        if self.primes:
            # Any number before p**2 will have been filtered previously
            p = self.primes[self.applied_primes_cursor - 1] 
            p_2 = p*p
            ret = min(p_2, self.get_size())
        else:
            ret = 1
        return ret

    def apply_filter(self):
        next_filter_prime  = self.primes[self.applied_primes_cursor]
        self.applied_primes_cursor = self.applied_primes_cursor + 1
            
        self.filter_list_of_multiples(next_filter_prime)
        
        for i in range(self.cursor, self.filtered_until()):
            if self.sieve[i]:
                self.primes.append(i)
            else:
                continue
            self.cursor = i + 1
        return

    def get_nth_prime(self, n):
        while not (len(self.primes) > n):
            if self.get_size() == self.filtered_until():
              raise SieveTooSmall(self.get_size(), len(self.primes), self.primes[-1], n + 1)

            self.apply_filter()
        return self.primes[n]

def find_prime_factors(n):
    ''' Given a number, return the list of its prime factors.'''

    pfactors = []
    idx_prime = 0
    biggest_necessary_prime = int(pow(n, 0.5)) + 1
    s = Sieve(biggest_necessary_prime)
    prime = s.get_nth_prime(idx_prime)
    while n  >= prime*prime:
        quotient, remainder = divmod(n, prime)
        if remainder:
            idx_prime = idx_prime + 1
            try:
                prime = s.get_nth_prime(idx_prime)
            except SieveTooSmall:
                # Sieve was big enough to find largest prime factor,
                # but not big enough to find the next biggest prime.
                # That's OK.  We only needed that to test the while condition.
                # So just break out of the loop here.
                break  
        else:
            pfactors.append(prime)
            n = quotient

    if n > 1:
        pfactors.append(n)
    return pfactors

def find_lcm(n_list):
    ''' Given a list of integers, return the least common multiple'''

    common_prime_factors = {}
    for n in n_list:
        pfactors = find_prime_factors(n)
        factcount = {}
        # Count how many of each factor there are and put the count in a dictionary.
        for pfactor in pfactors:
            factcount[pfactor] = factcount.get(pfactor, 0) + 1

        # Add these factors to the list of common prime factors.
        for pfactor in factcount.keys():
            common_prime_factors[pfactor] = max(common_prime_factors.get(pfactor, 0), factcount[pfactor])

    # Multiply the factors out to find the least common multiple.
    lcm = 1
    for pfactor, count in common_prime_factors.items():
        lcm = lcm * pow(pfactor, count)
    return lcm

def test_3():
    factors = { 169: [13, 13], 
                338: [2, 13, 13], 
                4: [2,2],
                20: [2, 2, 5],
                7789: [7789],
                0: [],  # By definition
                1: [],  # By definition
                2: [2],
                15485867: [15485867] # from bigprimes.net
                }

    bFailed = False
    for n in factors.keys():
        prime_factors = factors[n]
        found_prime_factors = find_prime_factors(n)
        if prime_factors != found_prime_factors:
            print 'For %d, factors should have been %s, but were %s' % (n, str(prime_factors), str(found_prime_factors))
            bFailed = True
    if not bFailed:
        print 'Passed.'

def test_5():
    lcms = { 20: [4, 5, 20],
             30: [2, 3, 5],
             32: [4, 8, 32],
             45: [9, 5, 3],
             101: [101]
}
    bPassed = 1
    for lcm in lcms.keys():
        found_lcm = find_lcm(lcms[lcm])
        if found_lcm != lcm:
            print 'Failed!  For ints %s, found lcm as %d, but it should have been %d' % (str(lcms[lcm]), found_lcm, lcm)
    if bPassed:
        print 'Passed.'

def test_7():
    
    s = Sieve(200000)
    i = 0
    bPassed = 1
    for p in test_data.first_1000_primes:
        p_found = s.get_nth_prime(i)
        i = i + 1
        if p != p_found:
            print 'Error at %dth prime.  Got %d but expected %d' % (i, p_found, p)
            bPassed = 0
            break

    if bPassed:
        print 'Passed.'

def test():
    test_3()
    test_5()
    test_7()

def run():

    print 'Problem 3:'
    print '  answer:', max(find_prime_factors(600851475143))
    t = timeit.Timer('max(find_prime_factors(600851475143))', setup='from __main__ import find_prime_factors')
    print '    time:', min(t.repeat(10, 1))

    print 'Problem 5:'
    print '  answer:', find_lcm(range(1, 21))
    t = timeit.Timer('find_lcm(range(1, 21))', setup='from __main__ import find_lcm')
    print '    time:', min(t.repeat(10, 1))

    print 'Problem 7:'
    print '  answer:',  Sieve(200000).get_nth_prime(10000)
    t = timeit.Timer('Sieve(200000).get_nth_prime(10000)', setup='from __main__ import Sieve') # 0th based
    print '    time:', min(t.repeat(10, 1))

if __name__ == '__main__':
  if sys.argv[1] == 'test':
      test()
  elif sys.argv[1] == 'run':
      run()
  else:
      print 'usage:  problems_3_5_7.py <test | run>'
