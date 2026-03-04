<?php
require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = trim($_POST['title']);
    $author = trim($_POST['author']);
    $description = trim($_POST['description']);
    
    if ($title && $author) {
        $stmt = $pdo->prepare("INSERT INTO books (title, author, description) VALUES (?, ?, ?)");
        $stmt->execute([$title, $author, $description]);
        
        header("Location: index.php");
        exit;
    } else {
        $error = "Заполните обязательные поля (название и автор)";
    }
}
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Добавить книгу</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 20px auto; padding: 0 20px; }
        form { background: #f5f5f5; padding: 20px; border-radius: 5px; }
        label { display: block; margin-top: 10px; }
        input, textarea { width: 100%; padding: 8px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin-top: 15px; }
        .back-link { display: inline-block; margin-bottom: 20px; color: #0066cc; text-decoration: none; }
        .error { color: red; margin-bottom: 15px; }
    </style>
</head>
<body>
    <a href="index.php" class="back-link">← Назад к списку книг</a>
    
    <h1>Добавить новую книгу</h1>
    
    <?php if (isset($error)): ?>
        <div class="error"><?= $error ?></div>
    <?php endif; ?>
    
    <form method="POST">
        <label for="title">Название книги *</label>
        <input type="text" id="title" name="title" required>
        
        <label for="author">Автор *</label>
        <input type="text" id="author" name="author" required>
        
        <label for="description">Описание</label>
        <textarea id="description" name="description" rows="4"></textarea>
        
        <button type="submit">Сохранить книгу</button>
    </form>
</body>
</html>