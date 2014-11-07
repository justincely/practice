# Practice doing some math in Ruby

require 'functions.rb'
require 'mathn'

def problem_1(n)
  sum = 0

  for i in 0...n
    if i % 3 == 0
      sum += i
    elsif i % 5 == 0
      sum += i
    end
  end

  return sum
end



def problem_3(num=600851475143)
  max_prime = 1

  for factor in num.prime_division.flatten
    if isprime?(factor) && (factor > max_prime)
      max_prime = factor
    end
  end

  return max_prime

end



puts "Problem 1:  #{problem_1(1000)}"
puts "Problem 3:  #{problem_3}"
