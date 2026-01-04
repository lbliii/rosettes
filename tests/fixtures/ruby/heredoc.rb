sql = <<~SQL
  SELECT *
  FROM users
  WHERE active = true
SQL

html = <<-HTML
  <div>Content</div>
HTML