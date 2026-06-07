MIN_SEED_LENGTH = 3

class CipherConfiguration:
    """Клас для керування криптографічними конфігураціями та контролю пакетів даних."""

    def __init__(self, algorithm: str, key_size: int, transformation: str = "AES/CBC/PKCS5Padding"):
        """
        Ініціалізація конфігурації, перевірка сумісності криптоалгоритмів та встановлення безпечних лімітів довжини ключів.
        """
        self.algorithm = algorithm.strip().upper()
        self.transformation = transformation
        
        # Визначення масиву дозволених розмірів ключів для кожного підтримуваного стандарту
        if self.algorithm == "AES":
            self.allowed_sizes = [128, 192, 256]
        elif self.algorithm == "RSA":
            self.allowed_sizes = [2048, 4096]
        elif self.algorithm == "DES":
            self.allowed_sizes = [56, 64]
        else:
            # Захист системи від запуску несертифікованих або вразливих алгоритмів
            raise ValueError(f"Алгоритм '{algorithm}' не підтримується. Оберіть AES, RSA або DES.")

        # Контроль відповідності довжини ключа специфікаціям обраного алгоритму
        if key_size not in self.allowed_sizes:
            raise ValueError(f"Розмір ключа {key_size} біт не підходить для алгоритму {self.algorithm}.")

        self.key_size = key_size
        self.history_logs = []  # Журнал для фіксації виконаних системою криптооперацій
        
    def generate_key(self, seed_phrase: str) -> str:
        """
        Генерація шаблону ключа - створення детермінованої текстової послідовності на основі користувацької секретної фрази (seed).
        """
        if not seed_phrase or len(seed_phrase.strip()) < MIN_SEED_LENGTH:
          raise ValueError(f"Фраза-зерно (seed) має містити хоча б {MIN_SEED_LENGTH} символи.") 
        # Розрахунок кількості структурних блоків ключа залежно від його загальної бітової довжини
        blocks_count = self.key_size // 64
        if blocks_count == 0:
            blocks_count = 1  # Запобігання нульовій довжині для низькобітного стандарту DES
            
        generated_key = ""
        cleaned_seed = seed_phrase.strip().upper()

        # Покрокове формування унікальних сегментів ключа за допомогою математичного зміщення фрази
        for i in range(1, blocks_count + 1):
            block_part = f"{cleaned_seed[:MIN_SEED_LENGTH]}{i * 7}"
            generated_key += block_part + "-"
            
        final_key = generated_key.rstrip("-")
        self.history_logs.append(f"Згенеровано шаблон ключа: {final_key}")
        return final_key

    def process_batch_data(self, data_packets: list) -> dict:
        """
        Пакетна обробка даних — аналіз та пре-валідація масиву вхідних повідомлень перед їх передачею в конвеєр шифрування.
        """
        if not isinstance(data_packets, list):
            raise TypeError("Вхідні дані повинні бути представлені списком пакетів.")
            
        report = {"processed": 0, "failed": 0, "details": []}
        index = 0
        
        # Послідовний перебір та ізольований аналіз кожного пакету з отриманої черги даних
        while index < len(data_packets):
            packet = data_packets[index]
            
            # Контроль цілісності структури та фільтрація пошкодженого вмісту в окремому пакеті
            try:
                if not isinstance(packet, str):
                    raise TypeError("Вміст пакету має бути виключно текстом.")
                if len(packet.strip()) == 0:
                    raise ValueError("Порожній пакет не підлягає обробці.")
                    
                # Реєстрація успішного проходження валідації для поточного елемента
                report["details"].append(f"Пакет {index} успішно перевірено ({len(packet)} симв.).")
                report["processed"] += 1
                
            except (TypeError, ValueError) as error:
                # Перехоплення локальних помилок для запобігання аварійній зупинці всього потоку обробки
                report["details"].append(f"Пакет {index} заблоковано. Причина: {str(error)}")
                report["failed"] += 1
                
            index += 1  # Зміщення покажчика на наступний елемент черги даних
            
        self.history_logs.append(f"Оброблено пакетів: {report['processed']}, помилок: {report['failed']}")
        return report
#review