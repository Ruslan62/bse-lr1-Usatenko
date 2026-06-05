IMAGES = ['jpg', 'png']
VIDEOS = ['mp4', 'mov']  
def process_media(file_path):
    if '.' not in file_path:
        return print("[Помилка] Файл повинен мати розширення!")
    stem, ext = file_path.rsplit('.', 1)
    ext = ext.lower()

    if ext in IMAGES:
        print(f"[OK] Знайдено зображення .{ext}. Оптимізуємо пікселі...")
    elif ext in VIDEOS:
        print(f"[OK] Знайдено відео .{ext}. Стискаємо кадри...")
    else:
        all_formats = IMAGES + VIDEOS
        print(f"[УВАГА] Формат .{ext} не підтримується. Доступні: {', '.join(all_formats)}")
        return

    print(f"[ГОТОВО] Файл '{stem}_compressed.{ext}' збережено.")

user_file = input("Введіть назву файлу: ").strip()

if user_file:
    process_media(user_file)
else:
    print("Назва файлу не може бути порожньою.")
#review