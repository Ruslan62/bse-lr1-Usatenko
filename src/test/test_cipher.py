import pytest
from src.main.cipher_configuration import CipherConfiguration

# ТЕСТУВАННЯ КОНСТРУКТОРА __init__ 

def test_init_aes_128_success():
    # Техніка: EP (Позитивний)
    
    # Arrange 
    algorithm = "AES"
    key_size = 128

    # Act 
    config = CipherConfiguration(algorithm, key_size)

    # Assert 
    assert config.algorithm == "AES"
    assert config.key_size == 128


def test_init_unsupported_algo():
    # Техніка: EP (Негативний)
    
    # Arrange 
    algorithm = "UNKNOWN"
    key_size = 128

    # Act & Assert 
    with pytest.raises(ValueError):
        CipherConfiguration(algorithm, key_size)


def test_init_invalid_key_size():
    # Техніка: BVA (Негативний)
    
    # Arrange 
    algorithm = "AES"
    key_size = 100

    # Act & Assert 
    with pytest.raises(ValueError):
        CipherConfiguration(algorithm, key_size)


# ТЕСТУВАННЯ МЕТОДУ generate_key 

def test_generate_key_128():
    # Техніка: EP (Позитивний)
    
    # Arrange 
    config = CipherConfiguration("AES", 128)
    seed_phrase = "password"

    # Act 
    result = config.generate_key(seed_phrase)

    # Assert 
    assert result == "PAS7-PAS14"


def test_generate_key_alt():
    # Техніка: EP (Позитивний)
    
    # Arrange 
    config = CipherConfiguration("AES", 128)
    seed_phrase = "alternative"

    # Act 
    result = config.generate_key(seed_phrase)

    # Assert 
    assert result == "ALT7-ALT14"


def test_generate_key_short_seed():
    # Техніка: BVA (Негативний)
    
    # Arrange 
    config = CipherConfiguration("AES", 128)
    seed_phrase = "12"

    # Act & Assert 
    with pytest.raises(ValueError):
        config.generate_key(seed_phrase)


# ТЕСТУВАННЯ МЕТОДУ process_batch_data 

def test_process_batch_success():
    # Техніка: EP (Позитивний)
    
    # Arrange
    config = CipherConfiguration("AES", 128)
    data_packets = ["packet1", "packet2"]

    # Act 
    report = config.process_batch_data(data_packets)

    # Assert 
    assert report["processed"] == 2
    assert report["failed"] == 0


def test_process_batch_empty_list():
    # Техніка: BVA (Позитивний)
    
    # Arrange 
    config = CipherConfiguration("AES", 128)
    data_packets = []

    # Act 
    report = config.process_batch_data(data_packets)

    # Assert 
    assert report["processed"] == 0
    assert report["failed"] == 0


def test_process_batch_single_item():
    # Техніка: BVA (Позитивний)
    
    # Arrange
    config = CipherConfiguration("AES", 128)
    data_packets = ["only_one"]

    # Act
    report = config.process_batch_data(data_packets)

    # Assert
    assert report["processed"] == 1
    assert report["failed"] == 0


def test_process_batch_alphanumeric():
    # Техніка: EP (Позитивний)
    
    # Arrange
    config = CipherConfiguration("AES", 128)
    data_packets = ["pass123", "crypt56"]

    # Act
    report = config.process_batch_data(data_packets)

    # Assert
    assert report["processed"] == 2
    assert report["failed"] == 0