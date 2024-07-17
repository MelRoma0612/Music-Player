from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import speech_recognition as sr
from fuzzywuzzy import fuzz, process
from selenium.webdriver.chrome.service import Service as ChromeService

m=[]
m_copy_mas=[]
m_copy_usual=[]
m_copy_2=[]
m_copy=[]
m_name=[]
m_url=[]
m1=[]
arr=[]
cnt=0
number=0
chk=0
check=0
check_not=0
flag_1=0
b=''
k_url=[]
count_chk=0

def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        print("Say")
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        f=recognizer.recognize_google(audio, language='ru-RU')
        text = f.lower()
        print('Было сказано: ' + text)
        global arr
        arr.append(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
def speech_rec():
    r = sr.Recognizer()
    r.pause_threshold = 0.5
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source=source, duration=0.5)
        try:
            print('Говорите')
            audio = r.listen(source)
            text = r.recognize_google(audio, language='ru-RU')
            text = text.lower()
            print('Было сказано: ' + text)
            return text
        except sr.WaitTimeoutError:
            print('Таймаут: не удалось записать звук')
        except sr.UnknownValueError:
            print('Ошибка распознавания речи: не удалось распознать речь')
def scraper():
    ua = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0 (Edition Yx 05)"')
    options.add_argument("--headless")
    with webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install())) as browser:
        # open the target website
        with open('parser.html', 'r+') as f:
            f.truncate(0)
        browser.get("https://music.youtube.com/playlist?list=PL9Lu8MtYgbQp0wZSA3mHrR3Hv4ZMBp4po")
        #"https://music.youtube.com/playlist?list=PL9Lu8MtYgbQp0wZSA3mHrR3Hv4ZMBp4po"
        #"https://music.youtube.com/playlist?list=PLu9zG_eL_nmUd0GCN2gX9z459G7Iad4_1&si=y1x3BYNeqtd5gpVh"
        # implicitly wait for the page to load
        tag = browser.execute_script("return document.querySelector('#contents').offsetHeight")
        print(tag)
        browser.execute_script(f"window.scrollBy(0, {tag})")

        time.sleep(2)
        tag = browser.execute_script("return document.querySelector('#contents').offsetHeight")
        browser.execute_script(f"window.scrollBy(0, {tag})")
        print(tag)
        # extract the page's full HTML
        page_source = browser.page_source
        with open("parser.html", "w", encoding="utf-8") as file:
            file.write(page_source)

        # quit the driver
        browser.quit()
def start_playlist():
    with open("parser.html", "r", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    user_names = soup.find("ytmusic-section-list-renderer", class_="description scroller scroller-on-hover style-scope ytmusic-two-column-browse-results-renderer").find("div", id="contents").find_all("ytmusic-responsive-list-item-renderer", class_="style-scope ytmusic-playlist-shelf-renderer")
    with open('playlist.txt', 'r+') as f:
        f.truncate(0)
    for name in user_names:
        nm = name.find("div", class_="flex-columns style-scope ytmusic-responsive-list-item-renderer").find("div", class_="title-column style-scope ytmusic-responsive-list-item-renderer").find("a", class_="yt-simple-endpoint style-scope yt-formatted-string")
        if nm:
            name_url = nm.get("href")
            name = nm.text.strip()
            m1.append(name)
            m_name.append(name)
            m1.append(name_url)
            m_url.append(name_url)
            m.append(m1)
            m1 = []
    with open("playlist.txt", "w", encoding="utf-8") as file:
        file.write(str(m))
    m_copy = m
    random.shuffle(m_copy)
    print(m)
    print(len(m))
    search_1()
def obrab(search_word):
    search_word=search_word.replace('включи', '')
    search_word=search_word.strip().title()
    p = process.extract(search_word, m_name, scorer=fuzz.WRatio)
    search_url=''
    search_music = p[0][0]
    f=0
    for i in m_copy:
        for j in range(len(i)):
            if i[0]==search_music:
                search_url=i[1]
                f=1
                break
        if f==1:
            break
    print(search_music)
    print(search_url)
    url = "https://music.youtube.com/" + search_url
    return url
def obrab_word(search_word):
    search_word=search_word.replace('включи', '')
    search_word=search_word.strip().title()
    p = process.extract(search_word, m_name, scorer=fuzz.WRatio)
    y = process.extract(search_word, m_name, scorer=fuzz.WRatio)[0][1]
    search_url=''
    search_music = p[0][0]
    return search_music

def obrab_word_usual(search_word):
    search_word = search_word.replace('включи', '')
    search_word = search_word.strip().title()
    query: str = search_word
    result = YouTubeMusicAPI.Search(query)
    result = result['trackName']
    if result:
        print(result)
        return result
    else:
        print("No Result Found")
def obrab_url_usual(search_word):
    search_word = search_word.replace('включи', '')
    search_word = search_word.strip().title()
    query: str = search_word
    result = YouTubeMusicAPI.Search(query)
    result = result['trackUrl']
    if result:
        print(result)
        return result
    else:
        print("No Result Found")
def search_usual_music(result):
    global arr
    global number
    global m_copy_usual
    global k_url
    time_m=[]
    with open("pars.html", "r", encoding="utf-8") as file:
        src = file.read()
    ua = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0 (Edition Yx 05)"')
    options.add_argument("--headless")
    with webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install())) as browser:
        if 'https://' in result:
            t=k_url.index(result)
            res_obr_name = m_copy_usual[t]
            browser.get(result)
        else:
            res_obr_url = obrab_url_usual(result)
            res_obr_name = obrab_word_usual(result)
            browser.get(res_obr_url)
            if res_obr_name not in m_copy_usual:
                k_url.append(res_obr_url)
                m_copy_usual.append(res_obr_name)
        previous_status = None
        video = browser.find_element(By.ID, 'play-pause-button')
        video.click()
        time_info = browser.execute_script("return document.querySelector('.time-info').innerText;")
        print(time_info)
        print(time_info.split("/"))
        result = second(time_info)
        print(result)
        r = sr.Recognizer()
        m_ = sr.Microphone()
        with m_ as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        stop_listening = r.listen_in_background(m_, callback)
        b = ''
        flag = 1
        fl_res = 1
        fl_rev_res = 1
        fl_next = 1
        fl_playlist = 1
        fl_vihod = 1
        while True:
            player_status = browser.execute_script("return document.getElementById('movie_player').getPlayerState()")
            time_info = browser.execute_script("return document.querySelector('.time-info').innerText;")
            # print(time_info)
            cleaned_array = [time.strip() for time in time_info.split("/")]
            # print(cleaned_array)
            formatted_time_list = zero(cleaned_array)
            '''print(formatted_time_list)
            print(formatted_time_list[0])
            print(result[1])'''
            if arr and 'включи' in arr[-1]:
                stop_listening(wait_for_stop=False)
                b = arr[-1]
                flag = 0
                break
            elif arr and (arr[-1] in phrases.pause_phrases):
                arr.pop(-1)
                browser.execute_script("document.getElementById('movie_player').pauseVideo()")
            elif arr and (arr[-1] in phrases.play_phrases):
                arr.pop(-1)
                browser.execute_script("document.getElementById('movie_player').playVideo()")
            elif arr and (arr[-1] in phrases.next_track_phrases):
                stop_listening(wait_for_stop=False)
                fl_next = 0
                print(res_obr_name)
                print(m_copy_usual)
                break
            elif arr and (arr[-1] in phrases.previous_track_phrases):
                stop_listening(wait_for_stop=False)
                fl_rev_res = 0
                print(res_obr_name)
                print(m_copy_usual)
                break
            elif arr and "плейлист" in arr[-1] and ' ' not in arr[-1]:
                stop_listening(wait_for_stop=False)
                fl_playlist = 0
                break
            elif arr and (arr[-1] in phrases.go_home_phrases):
                stop_listening(wait_for_stop=False)
                fl_vihod = 0
                #print(m_copy_2)
                break
            elif arr and (arr[-1] in phrases.close_phrases):
                stop_listening(wait_for_stop=False)
                browser.quit()
                exit()
            elif player_status != previous_status:
                time_m.append(player_status)
                print(f"Статус трека: {time_m}")
                previous_status = player_status

            elif (time_m[-1] == 3 and time_m[-2] == 1) or time_m[-1] == 0:
                stop_listening(wait_for_stop=False)
                fl_res = 0
                break
            elif not arr:  # Check if s is None or empty
                continue
        browser.quit()
        if flag == 0:
            arr = []
            chk = 1
            flag = 1
            search_usual_music(b)
        if fl_res == 0:
            fl_res = 1
            main()
        if fl_next == 0:
            arr = []
            fl_next = 1
            num = m_copy_usual.index(res_obr_name)
            num += 1
            search_usual_music(k_url[num])
        if fl_rev_res == 0:
            if m_copy_usual[0] != res_obr_name:
                arr = []
                fl_rev_res = 1
                num = m_copy_usual.index(res_obr_name)
                print(num)
                num -= 1
                search_usual_music(k_url[num])
        if fl_playlist == 0:
            arr=[]
            fl_playlist = 1
            playlist()
        if fl_vihod==0:
            arr=[]
            fl_vihod = 1
            main()
def search(search_word):
    global m_copy_2
    global m_copy
    global arr
    global number
    global chk
    global m_copy_mas
    global count_chk
    time_m=[]
    with open("pars.html", "r", encoding="utf-8") as file:
        src = file.read()
    ua = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0 (Edition Yx 05)"')
    options.add_argument("--headless")
    with webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install())) as browser:
        # open the target website
        res_obr_url = obrab(search_word)
        res_obr_name = obrab_word(search_word)
        previous_status = None
        if res_obr_name not in m_copy_2:
            count_chk+=1
            m_copy_2.append(res_obr_name)
        browser.get(res_obr_url)

        '''k, j = obrab_word(search_word)
        print(k, j)
        if (k != obrab_word_usual(search_word)) or (k != obrab_word_usual(search_word) and j < 80):
            search_usual_music(search_word)'''
        p = m_copy.index([res_obr_name, res_obr_url[26:]])
        print("count_chk", count_chk)
        print(p)
        h = m_copy[0]
        print(m_copy)
        print(m_copy_2)
        print("len(m_copy)", len(m_copy))
        page_source = browser.page_source
        if res_obr_name not in m_copy_2:
            count_chk += 1
            m_copy_2.append(res_obr_name)
        with open("pars.html", "w", encoding="utf-8") as file:
            file.write(page_source)
        '''s=input()
        while True:
            if s=='f':
                break
            else:
                continue'''
        # implicitly wait for the page to load
        video = browser.find_element(By.ID, 'play-pause-button')
        video.click()
        time_info = browser.execute_script("return document.querySelector('.time-info').innerText;")
        print(time_info)
        print(time_info.split("/"))
        result = second(time_info)
        print(result)
        r = sr.Recognizer()
        r.pause_threshold = 0.5
        m_ = sr.Microphone()
        with m_ as source:
            r.adjust_for_ambient_noise(source=source, duration=0.5)

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        stop_listening = r.listen_in_background(m_, callback)
        b = ''
        flag = 1
        fl_res = 1
        fl_rev_res=1
        fl_next=1
        fl_vihod=1
        flag_perem=1
        flag_new=1
        while True:
            #print(arr)
            player_status = browser.execute_script("return document.getElementById('movie_player').getPlayerState()")
            '''time_info = browser.execute_script("return document.querySelector('.time-info').innerText;")
            # print(time_info)
            cleaned_array = [time.strip() for time in time_info.split("/")]
            # print(cleaned_array)
            formatted_time_list = zero(cleaned_array)'''

            '''print(formatted_time_list)
            print(formatted_time_list[0])
            print(result[1])'''

            if arr and 'включи' in arr[-1]:
                stop_listening(wait_for_stop=False)
                b = arr[-1]
                flag = 0
                print(m_copy_2)
                break
            elif arr and (arr[-1] in phrases.shuffle_phrases):
                stop_listening(wait_for_stop=False)
                b = arr[-1]
                flag_perem = 0
                print(m_copy_2)
                break
            elif arr and (arr[-1] in phrases.pause_phrases):
                arr.pop(-1)
                browser.execute_script("document.getElementById('movie_player').pauseVideo()")
            elif arr and (arr[-1] in phrases.play_phrases):
                arr.pop(-1)
                browser.execute_script("document.getElementById('movie_player').playVideo()")
            elif arr and (arr[-1] in phrases.next_track_phrases):
                if count_chk == len(m_copy):
                    arr=[]
                    print("Этот трек последний")
                else:
                    stop_listening(wait_for_stop=False)
                    fl_next = 0
                    print(m_copy_2)
                    break
            elif arr and (arr[-1] in phrases.go_home_phrases):
                stop_listening(wait_for_stop=False)
                fl_vihod = 0
                print(m_copy_2)
                break
            elif arr and (arr[-1] in phrases.close_phrases):
                stop_listening(wait_for_stop=False)
                browser.quit()
                exit()
            elif arr and (arr[-1] in phrases.previous_track_phrases):
                if number == 0 and m_copy_2[0]==res_obr_name:
                    arr = []
                    print("Этот трек первый")
                else:
                    stop_listening(wait_for_stop=False)
                    fl_rev_res = 0
                    print(m_copy_2)
                    break
            if player_status != previous_status:
                time_m.append(player_status)
                print(f"Статус трека: {time_m}")
                previous_status = player_status

            if (time_m[-1] == 3 and time_m[-2] == 1) or time_m[-1] == 0:
                stop_listening(wait_for_stop=False)
                fl_res = 0
                break
            elif not arr:  # Check if s is None or empty
                continue

        browser.quit()
        if flag_perem==0:
            arr = []
            number = 0
            random.shuffle(m_copy)
            print(m_copy)
            m_copy_2 = []
            count_chk = 0
            search(m_copy[0][0])
        if flag_new == 0:
            arr = []
            number = 0
            m_copy = m
            search(m_copy[0][0])
        if flag == 0:
            if arr and arr[-1] == 'включи оригинальный плейлист':
                arr = []
                number = 0
                m_copy_2=[]
                m_copy = m_copy_mas
                count_chk=0
                print(count_chk)
                search(m_copy[0][0])
            else:
                print("count_chk", count_chk)
                arr = []
                chk = 1
                search(b)
        if fl_res == 0:
            if count_chk==len(m_copy):
                arr = []
                print("Плейлист окончен")
                m_copy_2 = []
                number = 0
                num = 0
                count_chk=0
                main()
            elif m_copy_2[-1] == res_obr_name:
                arr = []
                number = number + 1
                print(number)
                search(m_copy[number][0])
            else:
                arr=[]
                num = m_copy_2.index(res_obr_name)
                num += 1
                search(m_copy_2[num])
        if fl_next==0:
            if m_copy_2[-1]==res_obr_name:
                arr = []
                number = number + 1
                print(number)
                search(m_copy[number][0])
            else:
                arr=[]
                num=m_copy_2.index(res_obr_name)
                num+=1
                search(m_copy_2[num])
        if fl_rev_res == 0:
            if m_copy_2[0] == res_obr_name:
                arr = []
                number = number - 1
                search(m_copy[number][0])
            else:
                arr=[]
                num = m_copy_2.index(res_obr_name)
                print(num)
                num -= 1
                search(m_copy_2[num])
        if fl_vihod==0:
            arr=[]
            m_copy_2 = []
            number = 0
            num = 0
            count_chk = 0
            main()
def second(time_info):
    m = [time.strip() for time in time_info.split("/")]
    min_sec = m[1].split(":")
    print(min_sec)
    if len(min_sec) == 2:
        min_ = int(min_sec[0])
        sec_ = int(min_sec[1])
        time_2 = timedelta(hours=00, minutes=min_, seconds=sec_)
        tm = (time_2 - timedelta(seconds=2))
        res = str(tm).split(":")[1:]
        res1 = ":".join(res)
        print(res1)
    return res1
def zero(time_list):
    formatted_time_list = []
    for time_str in time_list:
        minutes, seconds = map(int, time_str.split(":"))
        formatted_time_list.append(f"{minutes:02}:{seconds:02}")  # Исправлено форматирование
    return formatted_time_list

def search_1():
    global number
    global m_copy
    global m_copy_2
    global arr
    global chk
    global m
    global count_chk
    global m_copy_mas
    time_m=[]
    with open("pars.html", "r", encoding="utf-8") as file:
        src = file.read()
    while True:
        search_word = speech_rec()
        if not search_word:  # Check if search_word is None or empty
            continue
        elif 'включи' in search_word.split() and 'оригинальный' in search_word.split() and 'плейлист' in search_word.split():
            m_copy=m_copy_mas
            count_chk=1
            search_word = m_copy[0][0]
            break
        elif 'включи' in search_word.split() and len(search_word.split())>1:
            count_chk = 1
            break
        elif 'перемешай' in search_word.split():
            random.shuffle(m_copy)
            print(m_copy)
            continue
        elif 'включи' in search_word.split() and len(search_word.split())==1:
            search_word = m_copy[0][0]
            count_chk = 1
            break
        else:
            continue
    ua = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0 (Edition Yx 05)"')
    options.add_argument("--headless")
    with webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install())) as browser:
        # open the target website
        res_obr_url = obrab(search_word)
        res_obr_name = obrab_word(search_word)
        previous_status = None
        if res_obr_name not in m_copy_2:
            m_copy_2.append(res_obr_name)
        browser.get(res_obr_url)
        '''k, j = obrab_word(search_word)
        print(k, j)
        if (k!=obrab_word_usual(search_word)) or (k!=obrab_word_usual(search_word) and j<80):
            search_usual_music(search_word)'''
        p = m_copy.index([res_obr_name, res_obr_url[26:]])
        h = m_copy[0]
        m_copy = m_copy[p:]+m_copy[:p]
        '''m_copy[0] = m_copy[p]
        m_copy[p] = h'''
        page_source = browser.page_source
        with open("pars.html", "w", encoding="utf-8") as file:
            file.write(page_source)
        '''s=input()
        while True:
            if s=='f':
                break
            else:
                continue'''
        # implicitly wait for the page to load
        video = browser.find_element(By.ID, 'play-pause-button')
        video.click()
        time_info = browser.execute_script("return document.querySelector('.time-info').innerText;")
        #print(time_info)
        #print(time_info.split("/"))
        result = second(time_info)
        #print(result)
        r = sr.Recognizer()
        r.pause_threshold = 0.5
        m_ = sr.Microphone()
        with m_ as source:
            r.adjust_for_ambient_noise(source=source, duration=0.5)

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        stop_listening = r.listen_in_background(m_, callback)
        b=''
        flag=1
        fl_res=1
        fl_next=1
        fl_vihod=1
        flag_new=1
        flag_perem=1
        while True:
            #print(arr)
            player_status = browser.execute_script("return document.getElementById('movie_player').getPlayerState()")
            time_info = browser.execute_script("return document.querySelector('.time-info').innerText;")
            # print(time_info)
            cleaned_array = [time.strip() for time in time_info.split("/")]
            # print(cleaned_array)
            formatted_time_list = zero(cleaned_array)
            '''print(formatted_time_list)
            print(formatted_time_list[0])
            print(result[1])'''

            if arr and 'включи' in arr[-1]:
                stop_listening(wait_for_stop=False)
                b = arr[-1]
                flag = 0
                print(m_copy_2)
                break
            elif arr and (arr[-1] in phrases.shuffle_phrases):
                stop_listening(wait_for_stop=False)
                b = arr[-1]
                flag_perem = 0
                print(m_copy_2)
                break
            elif arr and (arr[-1] in phrases.pause_phrases):
                arr.pop(-1)
                browser.execute_script("document.getElementById('movie_player').pauseVideo()")
            elif arr and (arr[-1] in phrases.play_phrases):
                arr.pop(-1)
                browser.execute_script("document.getElementById('movie_player').playVideo()")
            elif arr and (arr[-1] in phrases.next_track_phrases):
                if count_chk == len(m_copy):
                    arr = []
                    print("Этот трек последний")
                else:
                    stop_listening(wait_for_stop=False)
                    fl_next = 0
                    print(m_copy_2)
                    break
            elif arr and (arr[-1] in phrases.go_home_phrases):
                stop_listening(wait_for_stop=False)
                fl_vihod = 0
                print(m_copy_2)
                break
            elif arr and (arr[-1] in phrases.close_phrases):
                stop_listening(wait_for_stop=False)
                browser.quit()
                exit()
            elif arr and (arr[-1] in phrases.previous_track_phrases):
                if number == 0 and m_copy_2[0] == res_obr_name:
                    arr = []
                    print("Этот трек первый")
                else:
                    stop_listening(wait_for_stop=False)
                    fl_rev_res = 0
                    print(m_copy_2)
                    break
                    # Добавляем статус в список, только если он изменился
            elif player_status != previous_status:
                time_m.append(player_status)
                print(f"Статус трека: {time_m}")
                previous_status = player_status

            elif (time_m[-1] == 3 and time_m[-2] == 1) or time_m[-1] == 0:
                stop_listening(wait_for_stop=False)
                print("lala")
                fl_res=0
                break
            elif not arr:  # Check if s is None or empty
                continue
        browser.quit()
        if flag == 0:
            if arr and arr[-1]=='включи оригинальный плейлист':
                arr = []
                number = 0
                m_copy = m_copy_mas
                count_chk=0
                print(count_chk)
                search(m_copy[0][0])
            elif res_obr_name not in m_copy_2:
                count_chk+=1
                print(count_chk)
                arr = []
                chk = 1
                search(b)
            else:
                arr = []
                chk = 1
                search(b)
        if fl_res == 0:
            print("count_chk", count_chk)
            print(len(m_copy))
            if count_chk == len(m_copy):
                arr = []
                print("Плейлист окончен")
                m_copy_2 = []
                number = 0
                num = 0
                count_chk=0
                main()
            else:
                arr=[]
                number = number + 1
                search(m_copy[number][0])
        if fl_next==0:
            print(m_copy_2)
            if m_copy_2[-1]==res_obr_name:
                arr = []
                number = number + 1
                print(count_chk)
                search(m_copy[number][0])
                print(number)
            else:
                arr=[]
                num=m_copy_2.index(res_obr_name)
                num+=1
                search(m_copy_2[num])
        if fl_vihod==0:
            arr=[]
            m_copy_2 = []
            number = 0
            num = 0
            count_chk = 0
            main()
        if flag_perem==0:
            arr = []
            number = 0
            random.shuffle(m_copy)
            print(m_copy)
            count_chk=0
            search(m_copy[0][0])
# run the function
def playlist():
    check=0
    print("Обновить очередь?")
    while True:
        f = speech_rec()
        if not f:  # Check if search_word is None or empty
            continue
        elif "Да" in f.split() or "да" in f.split():
            scraper()
            start_playlist()
        elif "Нет" in f.split() or "нет" in f.split():
            start_playlist()
def main():
    print("Что бы Вы хотели?")
    global check
    global check_not
    global flag_1
    b = ''
    global m1
    global m
    global m_copy
    global m_copy_mas
    while True:
        if check == 1:
            check = 0
            break
        elif check_not == 1:
            check_not = 0
            break
        f = speech_rec()
        if not f:  # Check if search_word is None or empty
            continue
        elif (("включи" in f.split() or "включай" in f.split()) and "плейлист" in f.split()) or "плейлист" in f.split():
            print("Обновить список треков?")
            while True:
                f = speech_rec()
                if not f:  # Check if search_word is None or empty
                    continue
                elif "Да" in f.split() or "да" in f.split():
                    scraper()
                    check = 1
                    break
                elif "Нет" in f.split() or "нет" in f.split():
                    check_not = 1
                    break
        elif f and ('включи' in f or "включай" in f):
            b = f
            search_usual_music(b)
        elif f and ('закрыть' in f and ' ' not in f):
            exit()
        elif check == 1 or check_not == 1:
            return
    if flag_1==1:
        flag_1=0
        search_usual_music(b)
    with open("parser.html", "r", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    user_names = soup.find("ytmusic-section-list-renderer", class_="description scroller scroller-on-hover style-scope ytmusic-two-column-browse-results-renderer").find("div", id="contents").find_all("ytmusic-responsive-list-item-renderer", class_="style-scope ytmusic-playlist-shelf-renderer")
    with open('playlist.txt', 'r+') as f:
        f.truncate(0)
    for name in user_names:
        nm=name.find("div", class_="flex-columns style-scope ytmusic-responsive-list-item-renderer").find("div", class_="title-column style-scope ytmusic-responsive-list-item-renderer").find("a", class_="yt-simple-endpoint style-scope yt-formatted-string")
        if nm:
            name_url = nm.get("href")
            name = nm.text.strip()
            m1.append(name)
            m_name.append(name)
            m1.append(name_url)
            m_url.append(name_url)
            m.append(m1)
            m1 = []
    with open("playlist.txt", "w", encoding="utf-8") as file:
        file.write(str(m))
    m_copy=m.copy()
    m_copy_mas=m.copy()
    random.shuffle(m_copy)
    print(m_copy)
    print(len(m))
    m=[]
    search_1()
main()
