# Practice doing some math in Ruby

require 'functions.rb'
#require 'prime'

def problem_3(num=600851475143)
  max_prime = 1
 
  lower_factor = 2
  upper_factor = num / lower_factor

  until lower_factor >= upper_factor

    if not (num / lower_factor == upper_factor)
      next
    end

    puts "#{lower_factor} #{upper_factor} #{max_prime}"
    if isprime?(lower_factor) && (lower_factor > max_prime)
      max_prime = lower_factor
    end

    if isprime?(upper_factor) && (upper_factor > max_prime)
      puts "here"
      max_prime = upper_factor
    end

    lower_factor += 1
    upper_factor = num / lower_factor
  end

  return max_prime

end


puts "Problem 3:  #{problem_3}"
