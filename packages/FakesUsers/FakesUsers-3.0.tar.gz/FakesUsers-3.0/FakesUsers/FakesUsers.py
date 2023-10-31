import random

class Fu:
    def __init__(self):
        self.name_m_ru = ['Андрей','Афанасий','Абдул','Антон','Архип','Анатолий','Александр','Алексей','Альберт','Аксен',
                        'Богдан','Борис','Бронислав','Буклаг',
                        'Вадим','Владислав','Виктор','Валерий','Валентин','Василий','Виталий','Всеволод',
                        'Давид','Давыд','Даниель','Данил','Даниил','Дмитрий','Доброслав',
                        'Евгений','Евсений','Ефрем','Епифан','Егор',
                        'Жан',
                        'Завид','Захар',
                        'Иван','Игнат','Игорь','Иосиф','Изяслав','Илья','Ильнар',
                        'Кирилл','Казимир','Кузьма',
                        'Ладислав',
                        'Мазай','Макар','Максим','Марат', 'Мурат', 'Матвей','Марк', 'Мирослав',
                        'Никита','Нифёд','Николай','Назар',
                        'Олимп','Олег',
                        'Павел','Пётр',
                        'Роман','Родим','Радислав','Руслан','Рюрик',
                        'Савелий','Савва','Семён','Станислав','Спартак',
                        'Фёдор','Филипп','Федот',
                        'Эдвард','Эльдар','Эдгар','Эрик',
                        'Юрий','Юлий',
                        'Якив','Яков','Ян','Ярополк','Ярослав',]
        
        self.name_m_en = ['Aaron','Abraham','Adam','Adrian','Aidan','Alan','Albert','Alejandro','Alex','Alexander','Alfred','Angel','Anthony','Austin',
                          'Benjamin','Bernard','Blake','Brandon','Brian','Bruce','Bryan',
                          'Carl','Christopher','Christian','Cody','Connor',
                          'Daniel','Diego','Devin','Dennis',
                          'Edward','Ethan','Evan','Eric'
                          'Francis','Fred',
                          'Gabriel','Gavin','George','Gilbert','Gerld',
                          'Harry','Harold','Henry','Hunter','Howard',
                          'Ian','Isaac','Isaiah',
                          'Jack','Jackson','Jacob','Jason','Jake','Jordan','Jonathan','John','Justin','Joseph',
                          'Kevin','Kyle',
                          'Lucas','Louis','Logan','Lewis',
                          'Martin','Mason','Michael','Morgan',
                          'Norman','Neil','Nathaniel','Nathan',
                          'Oscar','Oliver','Owen',
                          'Patrick','Peter','Philip',
                          'Ralph','Raymond','Reginald','Richard','Robert','Ryan','Ronald',
                          'Samuel','Stanley','Steven','Seth','Sebastian',
                          'Thomas','Timothy','Tyler',
                          'Wallace','Walter','William','Wyatt',
                          'Xavier',
                          'Zachary',]
        
        self.surname_m_ru = ['Аношкин','Апатов','Апятов','Александров','Авлипов','Анатошкин','Аримченко','Абаранов','Адамов','Авличекко',
                        'Бытряков','Битряков','Борисов','Балипин','Базякин','Бурятов','Батурин',
                        'Ветров','Ветряков','Вадмиран','Вичатов','Викрович','Взаров','Версталин','Вокупин',
                        'Демитров','Донской','Денистарин','Дуров','Дамиченко','Доброградов','Далинин',
                        'Ермаков','Ефмеич','Егоров','Екатин',
                        'Жаровцев','Жирин','Жостченко','Жипин','Жилин',
                        'Задоров','Затриков','Зосин','Зазарин','Захаров','Захаев',
                        'Ильбанов','Инитаров','Известин','Итмирин','Изаченко','Избанов','Иоритов',
                        'Кристалин','Крост','Кисмисов',
                        'Лебедев','Литартасов','Ликрасов','Лесуч','Лобиченко',
                        'Митин','Матросов','Миклин','Меривич', 'Муратов', 'Матвеев','Мустин','Маслеников',
                        'Надурин','Нифёдов','Назаров','Николаев',
                        'Останткин','Остмов',
                        'Петроградов','Подушкин','Пирин','Пиров',
                        'Рокосовский','Радимов','Рютриков','Русланов','Ралин',
                        'Сантропов','Семёнов','Семечкин','Стасин','Спартаков',
                        'Фёдоров','Филиморов','Филатов',
                        'Хитров','Хитбаров','Хабарин',
                        'Шевцов','Шитрин','Шитин',
                        'Эдринский','Эшинский','Эпченко','Эрикс',
                        'Ютропов','Юлиев',
                        'Ярков','Яковлев','Ялубин','Явилин','Яшин',]
        
        self.surname_m_en = ['Akins','Alameda','Absher','Abramson','Alexandre','Alldredge','Alvarado','Amado',
                             'Barksdale','Barnard','Barney','Barrientos','Bartholomew','Bateman','Beckmann','Behm',
                             'Caballero','Caban','Canizales','Caplinger','Cardwell','Carleton','Cashman','Caudle',
                             'Daw',]
        
        self.name_f_ru = [ 'Аглая','Арина','Арина','Анна','Августина','Аделина','Ангелина','Анжела','Анфиса','Ася', 'Анастасия', 'Александра',
                        'Валентина','Владислава','Ваннеса','Виктория','Вероника','Вера',
                        'Галина',
                        'Дария','Диана','Дора',
                        'Елена','Евгения','Ева','Екатерина','Елизавета',
                        'Жанна',
                        'Зарина','Зоя',
                        'Инна','Ива','Ирина',
                        'Калина','Кира', 'Кристина',
                        'Лариса','Любовь','Лина',
                        'Майя','Марина','Мария','Марьяна',
                        'Ника','Надежда',
                        'Олеся','Оксана','Ольга',
                        'Полина',
                        'Рая','Раиса','Роза','Рита',
                        'Сабина','София','Стефания',
                        'Таисия','Татьяна',
                        'Эля','Эльга',
                        'Яна','Ярина',]
        
        self.name_f_en = ['Ann','Adelina','Amelia','Avery','Ada',
                          'Bailey','Barbara',
                          'Chloe','Cecilia','Catherine',
                          'Daisy','Danielle','Delia','Dorothy',
                          'Elizabeth','Ella','Erin',
                          'Freda','Fiona','Faith',
                          'Gloria','Grace',
                          'Helen','Hannah','Haley','Hailey',
                          'Isabel','Isabella',
                          'Jane','Jada','Julia','Joyce',
                          'Katherine','Kayla','Kylie','Katelyn','Kaitlyn',
                          'Lucy','Luccile','Lorna','Lily','Leslie','Lillian',
                          'Maria','Madeline','Mabel','Monica','Molly','Michelle','Mia',
                          'Nancy','Natalie','Nora',
                          'Olivia',
                          'Priscilla','Penelope','Pauline','Pamela',
                          'Rita','Riley','Rachel','Rose',
                          'Sandra','Sara','Sylvia','Shirley',
                          'Trinity','Vanessa','Victoria','Violet','Virginia',
                          'Winifred',
                          'Yvonne',
                          'Zoe',]
        
        self.surname_f_ru = ['Алианна','Альяна','Атрасова','Апяткова','Авиолова','Анатошкина','Адианова','Асокина','Асотина','Алимарова',
                        'Бистибюлина','Бистинова','Бильбина','Балина','Базякина','Бурова','Батросова',
                        'Виталина','Верченко','Вистибюлина','Волчанова','Васюткина','Взирова','Ветрова','Вилина',
                        'Добровая','Дианнова','Деченко','Дякина','Дасимова','Добрич','Долинина',
                        'Етиспатова','Еровенич','Есушкина','Едурина',
                        'Жилинна','Жигулич','Житрипевич','Жигина','Жорина',
                        'Зимаидова','Зимина','Зосина','Зарецская','Замитрова','Зюсина',
                        'Ильнасова','Ирибинко','Истучева','Исшенко','Ипритова','Илизова','Иоритова',
                        'Кристальная','Кристинова','Космович',
                        'Ликрасова','Литрасова','Лобина','Логина','Лосинова',
                        'Миликанова','Мутулина','Марошина','Мертеич', 'Муратова', 'Матвеева','Мулина','Мастович',
                        'Никитова','Неримова','Настюшина','Николаева',
                        'Осенняя','Отмирова',
                        'Петрокамчатская','Полинина','Пирова','Пасутина',
                        'Роловинина','Ракусина','Рюрович','Руслаченко','Ралина','Родова',
                        'Сандалина','Семикрасова','Сачкова','Салтыкова','Спорина',
                        'Фёдорова','Филиморова','Филатова',
                        'Хирипова','Хиширина','Хочубина',
                        'Шевцова','Шитина','Шитрина',
                        'Эдолинова','Эльдарова','Эпченко','Эпистатова',
                        'Ютропова','Юлиева',
                        'Яркова','Яковлева','Ялубина','Явилина','Яшина',]
        
        self.surname_f_en = ['Butler','Bishop','Blare','Bladshaw','Brooks','Bush','Babcook',
                             'Gray',
                             'Red',]
        
        self.num_part1_ru = ['001','002','003','004','005','006','007','008','009',]

        self.num_part2_ru = ['2415537','4636643','6438943','0077543','6536673','3564575','3513355','0006559',
                       '9997590','8654581','1010853','6695888','4256343','6476754','1215467','53674367',]
        
        self.email = ['rei793h','AlexHyIO','PORAMT1K','lsui1994','4345g2aw24y',
                      'georagl:wedmak','neomeo228','fifynya','930ip42','4444ererer4444',
                      'uow54io','xxxkeepmedownxxx','tytyr1n3','fil4rok','0101hh0101','QQooyyuurrnnIIwwqqxxzzQQ','popyt1k','tyrn1k','776',
                      'heroesRusich2007','igrikoh93w','3232lisabonka3232','youtubeTheBest','goverment_the_RCX','le4ko',
                      'tribasyakin_nikoplay','godEX55','beebag','3432','botik_shotik','joj1sus','LXCVWERSI',
                      'boris_ermakov75','barbara33','poplin_goblin','leeasaANDvanesa','so2H2O',
                      'yorik1900','kidsfam78','jackPreston89','l0lGRENDY']
        
        self.email_index = ['@example.ru','@outlook.qq','@mcrs.com','@python-test.pyt',]

        self.faddres = ['Грибоедова','Ленина','Жаргонская','Сосоновая','Еловая',
                  'Пугачева','Комунистическая','Социалистическая','Дектярёва','Гагарина',
                  'Черная','Победителей','Мира','Малеева','Захарова', '20 октября']
        
    def genRegion(self, region):
        reg = 'ru'
        self.reg = region

    def fakename_male(self):
        gn = self.reg
        if gn == 'ru':
            fakenmru = random.randint(0, len(self.name_m_ru) -1)
            fakesmru = random.randint(0, len(self.surname_m_ru) -1)
            return(f'{self.name_m_ru[fakenmru]} {self.surname_m_ru[fakesmru]}')
        elif gn == 'en':
            fakenmen = random.randint(0, len(self.name_m_en) -1)
            fakesmen = random.randint(0, len(self.surname_m_en) -1)
            return(f'{self.name_m_en[fakenmen]} {self.surname_m_en[fakesmen]}')
    
    def fakename_female(self):
        gn = self.reg
        if gn == 'ru':
            fakenfru = random.randint(0, len(self.name_f_ru) -1)
            fakesfru = random.randint(0, len(self.name_f_ru) -1)
            return(f'{self.name_f_ru[fakenfru]} {self.surname_f_ru[fakesfru]}')
        elif gn == 'en':
            fakenfen = random.randint(0, len(self.name_f_en) -1)
            fakesfen = random.randint(0, len(self.surname_f_en) -1)
            return(f'{self.name_f_en[fakenfen]} {self.surname_f_en[fakesfen]}')

    def fake_number(self):
        gn = self.reg
        if gn == 'ru':
            fakenum1ru = random.randint(0, len(self.num_part1_ru) -1)
            fakenum2ru = random.randint(0, len(self.num_part2_ru) -1)
            return(f'+7{self.num_part1_ru[fakenum1ru]}{self.num_part2_ru[fakenum2ru]}')
        elif gn == 'en':
            fakenum1en = random.randint(0, len(self.num_part1_ru) -1)
            fakenum2en = random.randint(0, len(self.num_part2_ru) -1)
            return(f'+1{self.num_part1_ru[fakenum1en]}{self.num_part2_ru[fakenum2en]}')
    
    def fake_addres(self):
        fakeaddres = random.randint(0, len(self.faddres) -1)
        return(f'ул. {self.faddres[fakeaddres]} {random.randint(1, 120)}')
    
    def fake_email(self):
        fakeei = random.randint(0, len(self.email_index) -1)
        fakee = random.randint(0, len(self.email) -1)
        return(f'{self.email[fakee]}{self.email_index[fakeei]}')
    
if __name__ == '__main__':
    fu = Fu()