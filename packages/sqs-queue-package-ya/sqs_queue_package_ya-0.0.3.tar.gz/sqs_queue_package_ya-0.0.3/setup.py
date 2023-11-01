# Импорт недавно установленного пакета setuptools.
import setuptools

# Открытие README.md и присвоение его long_description.
with open("README.md", "r") as fh:
    long_description = fh.read()

# Определение requests как requirements для того, чтобы этот пакет работал. Зависимости проекта.
requirements = ["boto3", "python-dotenv"]

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup(
    # Имя дистрибутива пакета. Оно должно быть уникальным,
    # поэтому добавление вашего имени пользователя в конце является обычным делом.
    name="sqs_queue_package_ya",
    # Номер версии вашего пакета. Обычно используется семантическое управление версиями.
    version="0.0.3",
    # Имя автора.
    author="Nick Jaraf",
    # Его почта.
    author_email="savarety.dev@gmail.com",
    # Краткое описание, которое будет показано на странице PyPi.
    description="Sqs queue",
    # Длинное описание, которое будет отображаться на странице PyPi. Использует README.md репозитория для заполнения.
    long_description=long_description,
    # Определяет тип контента, используемый в long_description.
    long_description_content_type="text/markdown",
    # URL-адрес, представляющий домашнюю страницу проекта. Большинство проектов ссылаются на репозиторий.
    url="https://gitlab.com/savarety/sqs-queue/-/tree/test?ref_type=heads",
    # Находит все пакеты внутри проекта и объединяет их в дистрибутив.
    packages=setuptools.find_packages(),
    # requirements или dependencies, которые будут установлены вместе с пакетом,
    # когда пользователь установит его через pip.
    # install_requires=requirements,
    # предоставляет pip некоторые метаданные о пакете. Также отображается на странице PyPi.
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # Требуемая версия Python.
    python_requires='>=3.6',
)
