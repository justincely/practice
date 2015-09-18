public class Euler{
  public static void main(String[]args){
    System.out.println("Problem 1:" + Euler.problem_1(1000));
    System.out.println("Problem 2:" + Euler.problem_2(4e6));
  }

  /*If we list all the natural numbers below 10 that are multiples of
    3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

    Find the sum of all the multiples of 3 or 5 below 1000.

  */
  public static int problem_1(Integer N){
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

  /* Each new term in the Fibonacci sequence is generated by adding the
    previous two terms. By starting with 1 and 2, the first 10 terms will be:

    1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

    By considering the terms in the Fibonacci sequence whose values do not
    exceed four million, find the sum of the even-valued terms.
  */
  public static double problem_2(Double limit){
    int sum = 0;
    int iteration = 0;
    int current = Functions.fibonacci(iteration);

    while (current < limit){
      if (current % 2 != 0)
        sum += current;

      iteration ++;
      current = Functions.fibonacci(iteration);

    };

    return sum;
  }


}