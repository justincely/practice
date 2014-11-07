# Practice doing some math in Ruby

require 'functions.rb'
require 'mathn'

def problem_3(num=600851475143)
  max_prime = 1

  for factor in num.prime_division.flatten
    if isprime?(factor) && (factor > max_prime)
      max_prime = factor
    end
  end

  return max_prime

end




puts "Problem 3:  #{problem_3}"
