# Напиши функцію check_file_size, яка приймає розмір у байтах. Якщо розмір більше 100 МБ, повертає False, інакше True. Також виведи повідомлення про ліміт.

def check_file_size(file_size):
    limit = 100 * 1024 * 1024
    if file_size > limit:
        return False
    else:
        return True
    