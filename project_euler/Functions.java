public class Functions{
  
  public static int fibonacci(double n){
    if (n == 0)
      return 0;
    else if (n == 1)
      return 1;
    else
      return Functions.fibonacci(n - 1) + Functions.fibonacci(n - 2);
  }

}
