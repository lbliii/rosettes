items.each do |item|
  puts item
end

items.map { |x| x * 2 }

File.open("file.txt") do |f|
  f.each_line { |line| process(line) }
end