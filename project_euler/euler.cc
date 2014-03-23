/* Practice

 */

#include <iostream>

#-------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------

int main()
{
  std::cout << "Problem 1: " << problem_1(1000) << "\n";
}
