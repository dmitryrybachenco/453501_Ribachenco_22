<?php
require_once 'config.php';

// Получаем все книги
$stmt = $pdo->query("SELECT * FROM books ORDER BY created_at DESC");
$books = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Отзывы о книгах</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 20px auto; padding: 0 20px; }
        .book { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
        .book h2 { margin-top: 0; color: #333; }
        .book a { text-decoration: none; color: #0066cc; }
        .add-book { background: #4CAF50; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>📚 Каталог книг</h1>
    
    <a href="add_book.php" class="add-book">+ Добавить книгу</a>
    
    <?php foreach ($books as $book): ?>
        <div class="book">
            <h2><a href="book.php?id=<?= $book['id'] ?>"><?= htmlspecialchars($book['title']) ?></a></h2>
            <p><strong>Автор:</strong> <?= htmlspecialchars($book['author']) ?></p>
            <p><?= htmlspecialchars($book['description']) ?></p>
            <p><a href="book.php?id=<?= $book['id'] ?>">Читать отзывы →</a></p>
        </div>
    <?php endforeach; ?>
</body>
</html>