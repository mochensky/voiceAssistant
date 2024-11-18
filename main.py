import speech_recognition as sr
import webbrowser
import subprocess
import asyncio
import re
import sympy
import pyttsx3

engine = pyttsx3.init()

social_networks = {
    "Telegram": "https://web.telegram.org/",
    "Google": "https://www.google.com/",
    "Yandex": "https://www.yandex.ru/",
    "Яндекс": "https://www.yandex.ru/",
    "YouTube": "https://www.youtube.com/",
    "Discord": "https://discord.com/app",
    "Roblox": "https://www.roblox.com/",
    "Роблокс": "https://www.roblox.com/",
    "Дискорд": "https://discord.com/app",
    "Википедия": "https://ru.wikipedia.org/",
    "Переводчик": "https://translate.yandex.ru/"
}

async def calculate_expression(expression):
    try:
        expression = expression.replace(" ", "").replace("х", "*").replace("X", "*").replace(".", "").replace(",", ".")
        if not re.match(r'^[\d\.\+\-\*\/]+$', expression):
            return "Некорректное математическое выражение"

        result = sympy.sympify(expression).evalf()

        result_str = f"{result:.16g}"
        result = float(result_str)

        return f"{result}"
    except Exception as e:
        return f"Ошибка при вычислении: {e}"

async def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.listen(source)

        try:
            text = await asyncio.to_thread(r.recognize_google, audio, language='ru-RU')
            print(f"Вы сказали: {text}")

            if "ассистент" in text.lower() or "асистент" in text.lower():
                if "открой браузер" in text.lower():
                    try:
                        search_query = text.split("браузер ")[1]
                        for network, url in social_networks.items():
                            if network.lower() in search_query.lower():
                                try:
                                    if network.lower() == "википедия":
                                        search = text.lower().split("википедия ")[1]
                                        print(search)
                                        webbrowser.open(f"https://ru.wikipedia.org/wiki/{search}")
                                        return
                                except:
                                    pass

                                try:
                                    if network.lower() == "youtube":
                                        search = text.lower().split("youtube ")[1]
                                        print(search)
                                        webbrowser.open(f"https://www.youtube.com/results?search_query={search}")
                                        return
                                except:
                                    pass
                                webbrowser.open(url)
                                print(f"Открываю {network}")
                                return
                    except:
                        pass
                    try:
                        search_query = text.split("браузер ")[1]
                        webbrowser.open(f"https://www.yandex.ru/search/?text={search_query}")
                        print(f"Открываю браузер с запросом: {search_query}")
                    except:
                        webbrowser.open(f"https://www.yandex.ru")
                        print(f"Открываю браузер")
                elif "сколько будет" in text.lower():
                    try:
                        expression = text.lower().split("сколько будет ")[1]
                        result = await calculate_expression(expression)
                        print(result)
                        engine.say(result)
                        engine.runAndWait()
                    except:
                        print("Ошибка")
                elif "открой калькулятор" in text.lower():
                    subprocess.Popen(['calc'])
                    print("Открываю калькулятор")
                elif "открой блокнот" in text.lower():
                    subprocess.Popen(['notepad'])
                    print("Открываю блокнот")
                elif "открой спотифай" in text.lower() or "открой spotify" in text.lower():
                    try:
                        subprocess.Popen(["C:\\Users\\User\\AppData\\Roaming\\Spotify\\Spotify.exe"])
                        print("Запускаю Spotify")
                    except FileNotFoundError:
                        print("Spotify не найден")
                elif "открой дискорд" in text.lower() or "открой discord" in text.lower():
                    subprocess.Popen(['C:\\Users\\User\\AppData\\Local\\Discord\\app-1.0.9164\\Discord.exe'])
                    print("Открываю Discord")
                elif "открой проводник" in text.lower():
                    subprocess.Popen('explorer')
                    print("Открываю проводник")
                else:
                    print("Команда не распознана")
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания: {e}")

async def main():
    while True:
        await recognize_speech()

asyncio.run(main())