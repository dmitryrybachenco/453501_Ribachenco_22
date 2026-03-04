<?php
require_once 'config.php';

if (!isset($_GET['id']) || !is_numeric($_GET['id'])) {
    die('Книга не найдена');
}

$book_id = $_GET['id'];

// Получаем информацию о книге
$stmt = $pdo->prepare("SELECT * FROM books WHERE id = ?");
$stmt->execute([$book_id]);
$book = $stmt->fetch();

if (!$book) {
    die('Книга не найдена');
}

// Получаем отзывы
$stmt = $pdo->prepare("SELECT * FROM reviews WHERE book_id = ? ORDER BY created_at DESC");
$stmt->execute([$book_id]);
$reviews = $stmt->fetchAll();

// Добавление нового отзыва
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name']);
    $rating = (int)$_POST['rating'];
    $comment = trim($_POST['comment']);
    
    if ($name && $rating >= 1 && $rating <= 5 && $comment) {
        $stmt = $pdo->prepare("INSERT INTO reviews (book_id, reviewer_name, rating, comment) VALUES (?, ?, ?, ?)");
        $stmt->execute([$book_id, $name, $rating, $comment]);
        
        // Перенаправляем, чтобы избежать повторной отправки формы
        header("Location: book.php?id=$book_id");
        exit;
    } else {
        $error = "Пожалуйста, заполните все поля корректно";
    }
}
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title><?= htmlspecialchars($book['title']) ?> - отзывы</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 20px auto; padding: 0 20px; }
        .book-info { background: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 30px; }
        .review { border-bottom: 1px solid #eee; padding: 15px 0; }
        .rating { color: #ffc107; font-size: 20px; }
        .review-form { background: #f5f5f5; padding: 20px; border-radius: 5px; margin-top: 30px; }
        input, textarea, select { width: 100%; padding: 8px; margin: 5px 0 15px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .back-link { display: inline-block; margin-bottom: 20px; color: #0066cc; text-decoration: none; }
        .error { color: red; margin-bottom: 15px; }
    </style>
</head>
<body>
    <a href="index.php" class="back-link">← Назад к списку книг</a>
    
    <div class="book-info">
        <h1><?= htmlspecialchars($book['title']) ?></h1>
        <p><strong>Автор:</strong> <?= htmlspecialchars($book['author']) ?></p>
        <p><?= htmlspecialchars($book['description']) ?></p>
    </div>
    
    <h2>Отзывы читателей (<?= count($reviews) ?>)</h2>
    
    <?php if (empty($reviews)): ?>
        <p>Пока нет отзывов. Будьте первым!</p>
    <?php else: ?>
        <?php foreach ($reviews as $review): ?>
            <div class="review">
                <div class="rating">
                    <?php for ($i = 1; $i <= 5; $i++): ?>
                        <?= $i <= $review['rating'] ? '★' : '☆' ?>
                    <?php endfor; ?>
                </div>
                <p><strong><?= htmlspecialchars($review['reviewer_name']) ?></strong> 
                   <small>(<?= date('d.m.Y', strtotime($review['created_at'])) ?>)</small></p>
                <p><?= htmlspecialchars($review['comment']) ?></p>
            </div>
        <?php endforeach; ?>
    <?php endif; ?>
    
    <div class="review-form">
        <h3>Оставить отзыв</h3>
        
        <?php if (isset($error)): ?>
            <div class="error"><?= $error ?></div>
        <?php endif; ?>
        
        <form method="POST">
            <label for="name">Ваше имя:</label>
            <input type="text" id="name" name="name" required>
            
            <label for="rating">Оценка:</label>
            <select id="rating" name="rating" required>
                <option value="5">5 ★</option>
                <option value="4">4 ★</option>
                <option value="3">3 ★</option>
                <option value="2">2 ★</option>
                <option value="1">1 ★</option>
            </select>
            
            <label for="comment">Отзыв:</label>
            <textarea id="comment" name="comment" rows="5" required></textarea>
            
            <button type="submit">Отправить отзыв</button>
        </form>
    </div>
</body>
</html>