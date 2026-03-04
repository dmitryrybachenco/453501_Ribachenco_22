FROM php:8.2-apache

# Установка всех необходимых системных зависимостей
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    libicu-dev \
    libxslt1-dev \
    libssl-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        pdo_mysql \
        mysqli \
        mbstring \
        exif \
        pcntl \
        bcmath \
        gd \
        intl \
        zip \
        xsl \
        opcache \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Включение Apache модулей
RUN a2enmod rewrite headers

# Установка Composer (опционально)
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

# Настройка прав
RUN chown -R www-data:www-data /var/www/html