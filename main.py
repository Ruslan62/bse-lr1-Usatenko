SUPPORTED = ['jpg', 'png', 'mp4', 'avi']

def process_media(file_path):
    if '.' not in file_path:
        return print("[Помилка] Файл повинен мати розширення!")

    # Спрощений поділ: stem — назва, ext — розширення без крапки
    stem, ext = file_path.rsplit('.', 1)
    ext = ext.lower()

    if ext in SUPPORTED:
        print(f"[OK] Формат .{ext} підтримується.")
        print(f"[ГОТОВО] Файл '{stem}_compressed.{ext}' збережено.")
    else:
        print(f"[УВАГА] Формат .{ext} не підтримується. Доступні: {', '.join(SUPPORTED)}")

# Основна логіка без зайвих функцій
user_file = input("Введіть назву файлу: ").strip()

if user_file:
    process_media(user_file)
else:
    print("Порожнє введення.")