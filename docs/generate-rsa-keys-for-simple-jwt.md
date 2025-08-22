## 🔑 JWT Авторизация (RS256)

#### На Linux (Ubuntu/Debian/WSL)

```bash
sudo apt update
sudo apt install openssl -y
```

#### На macOS

Обычно `openssl` есть, но если вдруг нет:

```bash
brew install openssl
```

#### На Windows

1. Установи **Git for Windows** или **WSL** (Windows Subsystem for Linux).

   * В WSL уже можно поставить как в Ubuntu: `sudo apt install openssl -y`.
2. Или скачай бинарники OpenSSL отсюда: [slproweb.com/products/Win32OpenSSL.html](https://slproweb.com/products/Win32OpenSSL.html).

---

Проект использует асимметричное шифрование (RS256) для генерации и проверки JWT-токенов.  
Для работы нужны два ключа в папке `security/`:

- `private_key.pem` — приватный ключ (используется для подписи токенов).
- `public_key.pem` — публичный ключ (используется для проверки токенов).

### Генерация ключей
Выполните в корне проекта:

```bash
# Создать приватный ключ (2048 бит)
openssl genrsa -out security/private_key.pem 2048

# Создать публичный ключ на основе приватного
openssl rsa -in security/private_key.pem -pubout -out security/public_key.pem
```


### 🚀 Альтернатива (генерация ключей прямо Python-скриптом)

Если не хочешь возиться с установкой OpenSSL, можно сгенерировать ключи чисто на Python через библиотеку `cryptography`:

```bash
pip install cryptography
```

```python
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pathlib import Path

# Генерация приватного ключа
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Сохраняем приватный ключ
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption(),
)
Path("security/private_key.pem").write_bytes(private_pem)

# Создаём публичный ключ
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)
Path("security/public_key.pem").write_bytes(public_pem)

print("✅ Ключи сгенерированы в папке security/")
```

После запуска появятся `security/private_key.pem` и `security/public_key.pem`.

---

#### Настройка в Django

**Файлы подгружаются в settings.py автоматически:**

```py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "security" / "private_key.pem") as f:
    PRIVATE_KEY = f.read()

with open(BASE_DIR / "security" / "public_key.pem") as f:
    PUBLIC_KEY = f.read()

SIMPLE_JWT = {
    "ALGORITHM": "RS256",
    "SIGNING_KEY": PRIVATE_KEY,
    "VERIFYING_KEY": PUBLIC_KEY,
    ...
}
```
**Важно**

 - Не коммить папку security/ с приватным ключом в GitHub — добавьте её в .gitignore.

 - private_key.pem храните только на сервере.

 - public_key.pem можно раздавать сервисам, которые должны проверять токены.