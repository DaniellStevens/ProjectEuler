1.  A Sample of the Output
> python ./problems_3_5_7.py run
Problem 3:
  answer: 6857
    time: 0.30354809761
Problem 5:
  answer: 232792560
    time: 0.000549077987671
Problem 7:
  answer: 104743
    time: 0.127998113632

2.  How I Chose the Problems I Did?
I spent about an hour scanning, the first problems, then skipped to somewhere in the middle and the end.  I was most interested in Problem 7 because it's a familiar problem ("find the nth prime") but I'd never solved it and I knew that calculating primes is difficult in general.  I then realized that the answer to question 7 was related to Problem 3 and Problem 5, so I decided to do the set. I also thought it was kind of clever that they chose to ask about primes in the problems numbered after the first non-even primes (3, 5, 7).

3.  The Process I Used to Solve the Problems
I started with Problem 7 because I thought that would be the most challenging and once I'd solved it the others would be straightforward.  I knew about the Sieve of Eratosthenes method from somewhere and decided to implement it, see how it performed, and then search for optimizations to the algorithm or alternate algorithms if it was too slow.  For a test I downloaded the first 1000 from http://primes.utm.edu/lists/small/1000.txt.  It was pretty fast, but I went to Wikipedia and found that although I had known my sieve was filtering up to p**2, I was applying subsequent filters below that point in the sieve.  I made that optimization.  I subsecond times for finding the 10,001st prime were good enough and moved on.

After I had a prime number generator, the other two problems were mathematically and programmatically straight forward.  Here, the math was simple enough to create my test cases by hand.  I spent a little time figuring out how to guarantee the sieve object would be large enough and adding better error handling if it wasn't.  One way this could be enhanced would be to make the sieve grow as necessary and discard the already filtered regions once we were done with them.

Originally, I'd been timing individual cases using the unix command "time", but now I instrumented the code using the timeit module.  I took the best of 10 times for each problem as the final measurement.  

4.  Reference sources:
a.  http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
b.  https://code.google.com/p/projecteuler-solutions/
c.  http://primes.utm.edu/lists/small/1000.txt

5.  I spent about three hours a day on this; i.e. nine hours.
