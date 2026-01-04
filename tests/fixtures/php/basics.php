<?php
namespace App\Models;

use App\Traits\Loggable;

class User {
    public string $name;
    private int $age;
    
    public function __construct(string $name, int $age) {
        $this->name = $name;
        $this->age = $age;
    }
    
    public function greet(): string {
        return "Hello, {$this->name}!";
    }
}

$user = new User("John", 30);
echo $user->greet();

// Arrow function
$double = fn($x) => $x * 2;

// Match expression
$result = match($status) {
    "active" => 1,
    "inactive" => 0,
    default => -1,
};
?>
