import pyttsx3
import speech_recognition as sr
from PIL import Image
from pytesseract import image_to_string
import pytesseract

# тессеракт нужно скачать и прописать путь в соответствии с тем, где вы разместите
# скачать можно здесь https://github.com/UB-Mannheim/tesseract/wiki
# вообще не всегда есть необходимость прописывать расположение
# в основном это в windows требуется, на mac и linux говорят такой необходимости не возникает
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# команды для разных языковых режимов и список изображений
RU_COMMANDS = {'записать текст': 'writer()', 'прочитать текст': 'reader()',
               'выбрать файл': 'choose_file()', 'выбрать картинку': 'choose_image()',
               'показать команды': 'show_commands()', 'список картинок':'show_images()'}
EN_COMMANDS = {'write text': 'writer()', 'read text': 'reader()',
               'choose file': 'choose_file()', 'choose image': 'choose_image()',
               'show commands': 'show_commands()', 'pictures list':'show_images()'}
IMAGES = ['ring', 'dungeon', 'game', 'date']

img, file, lang = None, None, 'ru-RU'
engine = pyttsx3.init() # объект для голоса компьютера
record = sr.Recognizer() # объект для распознования голоса

def say_to_me(talk):
    engine.say(talk)
    engine.runAndWait()

def voice_getter(): # функция для распознавания голосовых команд
    # try:
        with sr.Microphone(device_index=0) as source:
            if lang == 'en-EN':
                print('Speak...')
            elif lang == 'ru-RU':
                print('Говори...')
            audio = record.listen(source)
            result = record.recognize_google(audio, language=lang)
            print(result) # у меня иногда плохо распознает речь, возможно микрофон плохой,
                          # а может май инглиш из бэд
                          # поэтому вывожу результат обработки в консоль
            return result.lower()
    # except:
    #     return 'ничего'  # правильно тут наверное pass прописать и обработать его потом,
    #                      # но маленький костыль тут просто компактнее мне кажется

def writer():  # чтение текста с изображения и запись в файл
    try:
        tmp_file = f"files/{img}.txt"
        if img in ('dungeon', 'ring'): # если файлы с английским текстом - английский по умолчанию
            text = image_to_string(Image.open(f'images/{img}.PNG'))
        else:
            text = image_to_string(Image.open(f'images/{img}.PNG'), lang='rus') # иначе русский
        with open(tmp_file, mode='w') as f:
            f.write(text)
        if lang == 'en-EN':
            say_to_me(f'text written to file {tmp_file}')
        else:
            say_to_me(f'текст записан в файл {tmp_file}')
        global file
        file = tmp_file
    except:
        if lang == 'en-EN':
            say_to_me("picture not found or wasn't chosen")
        else:
            say_to_me('изображение не найдено или не выбрано')

def reader(): # для чтения файла и вывода в консоль
    try:
        with open(file, mode='r') as f:
            print(f.read())
    except:
        if lang == 'en-EN':
            say_to_me("file not found, or wasn't chosen")
        else:
            say_to_me('файл не найден, или не выбран')

def choose_file():  # выбор файла для чтения
    if lang == 'ru-RU':
        say_to_me('Содержимое какого файла вы хотите просмотреть?')
    else:
        say_to_me('What file do you want to view?')
    res = voice_getter()
    if any(x in res for x in IMAGES):
        global file
        file = f'files/{res.split(".")[0]}.txt'
    else:
        say_to_me('Не понимаю')

def choose_image():  # выбор картинки для считывания текста
    if lang == 'ru-RU':
        say_to_me("С какой картинки прочитать текст?")
    else:
        say_to_me("What picture's text write?")
    res = voice_getter()
    if any(x in res for x in IMAGES):
        global img
        img = f'{res.split(".")[0]}'
    else:
        say_to_me('Не понимаю')

def show_images():
    print(*map(lambda x: f'{x}.PNG', IMAGES), sep='\n')

def show_commands():
    if lang == 'en-EN':
        print(*EN_COMMANDS, sep='\n')
    else:
        print(*RU_COMMANDS, sep='\n')

def ru_version():  # для русской версии
    say_to_me('Чем я могу помочь?')
    res = voice_getter()
    if 'выход' in res:
        return True
    elif res in RU_COMMANDS:
        exec(RU_COMMANDS.get(res))
    else:
        say_to_me('не понимаю')

def en_version():  # и для английской
    say_to_me('How can I help?')
    res = voice_getter().lower()
    if 'exit' in res:
        return True
    elif res in EN_COMMANDS:
        exec(EN_COMMANDS.get(res))
    else:
        say_to_me('do not understand')


# цикл для выбора языка
say_to_me('Выберите язык')
flag = False
while not flag:
    res = voice_getter()
    try:
        if 'english' in res or 'английский' in res:
            lang = 'en-EN'
            flag = True
        elif 'russian' in res or 'русский' in res:
            lang = 'ru-RU'
            flag = True
        else:
            say_to_me('Повторите')
    except:
        say_to_me('Повторите')

# основной цикл
stop = None
while not stop:
    if lang == 'ru-RU':
        stop = ru_version()
    else:
        stop = en_version()













