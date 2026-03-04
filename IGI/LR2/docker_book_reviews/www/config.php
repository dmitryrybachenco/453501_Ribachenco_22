<?php
// В Docker сервис MySQL доступен по имени "mysql"
$host = 'mysql';  // Важно: это имя сервиса из docker-compose.yml!
$dbname = 'book_reviews';
$username = 'bookuser';
$password = 'bookpass123';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Ошибка подключения: " . $e->getMessage());
}
?>