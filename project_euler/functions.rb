def isprime?(number)
  puts "That's not an integer." unless number.is_a? Integer

  if number == 2
    return true
  elsif (number < 2) | (number % 2 == 0) 
    return false
  else
    for value in 3...number
      if number % value == 0
        return false
      end
    end
  end

  return true

end
