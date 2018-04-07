import requests, os, bs4

url = 'https://pixabay.com' #основной url страницы
req = input('Что ищем?:').strip() #поисковый запрос

while True:  #получаем количество изобраджений - итераций
    try:
        number = int(input("Сколько изображений загрузить(1-16)?:\n"))
        break
    except ValueError:
        print ("Введите целое число.")

fullUrl = url + '/photos/?q=' + req #ссылка на результаты поиска по запросу
os.makedirs('images', exist_ok=True)  #создаем папку, не заменяем если уже есть

res = requests.get(fullUrl)  #получаем страницу с результатами
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'html.parser') #парсим хтмл страницы

i = 0

while i < number:
    imgSource = soup.select('div img')[i]
    imgUrl = imgSource.get('srcset')
    if imgUrl == None:  #проверка на то, если эелмент пуст
        print('Не удалось найти изображение')
        break
    else:
        secondUrl = imgUrl.split(',')[1][0:-3].strip() #вытаскиваем второй урл на изображение, очищаем от ненужного
        print('Загружается изображение %s...' % (os.path.basename(secondUrl)))
        res = requests.get(secondUrl)
        res.raise_for_status()
        imageFile = open(os.path.join('images', os.path.basename(secondUrl)), 'wb') #записываем файл в папку
        for chunk in res.iter_content(10000):
            imageFile.write(chunk)
        imageFile.close()
        i = i + 1

print('%s изображений загружено в папку images' % i)
