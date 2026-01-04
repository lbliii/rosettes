# Variables
$name = "World"
$count = 10

# Function
function Greet {
    param([string]$Name)
    Write-Host "Hello, $Name!"
}

# Conditionals
if ($name -eq "World") {
    Write-Host "Hello World"
} elseif ($name -eq "") {
    Write-Host "No name"
} else {
    Write-Host "Hello $name"
}

# Loops
foreach ($i in 1..$count) {
    Write-Host "Iteration $i"
}

# Arrays
$items = @("one", "two", "three")
Write-Host $items[0]