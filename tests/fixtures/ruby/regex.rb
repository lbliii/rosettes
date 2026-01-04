pattern = /\A[a-z]+\z/i
text =~ /hello/
text.match?(/world/)
gsub(/old/, "new")