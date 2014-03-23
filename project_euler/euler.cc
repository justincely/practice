/* Practice

 */

#include <iostream>
#include <cmath>

//------------------------------------------------------------------------------

int fibonacci(double n)
{
  if (n == 0)
    return 0;
  else if (n == 1)
    return 1;
  else
    return fibonacci(n - 1) + fibonacci(n - 2);
}

//------------------------------------------------------------------------------

bool isprime(int number)
{
  if ((number < 2) || (number % 2 == 0))
    return false;

  if (number == 2)
    return true;

  for (int value=3; value < sqrt(number) + 1; value+=2){
    if (number % value == 0)
      return false;
  };

  return true;

}

//------------------------------------------------------------------------------



//------------------------------------------------------------------------------

int problem_1(int N)
{
  /*If we list all the natural numbers below 10 that are multiples of 
    3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

    Find the sum of all the multiples of 3 or 5 below 1000.

  */

  int sum = 0;
    
    for (int i=0; i<N; i++){
      if (i % 3 == 0)
	sum += i;
      else if (i % 5 == 0)
	sum += i;
      else
	{};
    }
    
    return sum;
}

//------------------------------------------------------------------------------

int problem_2(double limit=4e6)
{
  /* Each new term in the Fibonacci sequence is generated by adding the 
    previous two terms. By starting with 1 and 2, the first 10 terms will be:

    1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

    By considering the terms in the Fibonacci sequence whose values do not 
    exceed four million, find the sum of the even-valued terms.
  */

  int sum = 0;
  int iteration = 0;
  int current = fibonacci(iteration);

  while (current < limit){
    if (current % 2 != 0)
      sum += current;

    iteration ++;
    current = fibonacci(iteration);

  };
  
  return sum;
}

//------------------------------------------------------------------------------

int problem_3(double value=600851475143)
{
  /*prime factors of 13195 are 5, 7, 13 and 29.

    What is the largest prime factor of the number 600851475143 ?
  */

  int max_prime_fac = 1;

  for (int i=0; i<sqrt(value)+1; i++){
    if (isprime(i) && (remainder(value, i) == 0) && (i > max_prime_fac)){
      max_prime_fac = i;
    };

  };
  
  return max_prime_fac;
}

//------------------------------------------------------------------------------

int main()
{
  std::cout << "Problem 1: " << problem_1(1000) << "\n";
  std::cout << "Problem 2: " << problem_2(4e6) << "\n";
  std::cout << "Problem 3: " << problem_3() << "\n";
}
