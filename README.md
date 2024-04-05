_... проект не брошен, просто отложен, сейчас работаю над скрапером на Airbnb._

# Простая программа для записи доходов и расходов и последующего анализа и выводов.


На данный момент, я просто накидываю сюда мысли, аспекты и решения, особенности, по окончанию приложения, я структурирую все это и зафинализирую, а там как выйдет..


## Безопасность:
 Ни кто не хочет давать информацию о доходе и расходе в сеть или приложению, да и вообще ни кому и ни куда - это нормально и похвально. Но все же, давайте проясним:

 - Не публикуйте свою настоящую фамилию, а если и публикуете, то хотя бы не публикуйте отчество хотя бы.
 - Закрывайте видимость в телеграмм своего номера телефона.
 - Информация подаваемая вами, несет абстрактный формат, без адреса и местоположения.
 - Тем кому нужно, они найдут о вас все что нужно и без моего приложения, оно в их списке явно не стоит. Банки сами все сольют, они обязаны по закону.
 - Если у вас есть хоть какое то сомнение хоть в чем то, не используйте мое приложение.
 - Я постарался сохранить безопастность данных и абстрактность.
 - Я ни кому не сливаю ни каких данных, хотя бы потому, что я не знаю кто вы, у меня хранятся на сервере данные в базе данных PostgreSQL запущенные в докере, к тому же, они обезличеные.


 ## Использование: 
 - "+ 100, налик, веернул Колян долг" - программа внесет 100 рублей, автоматически, по средствам обученной модели, присвоит доход к категории, определенной по вашему описанию.
 - "- 100, карта, одолжил Коляну"  - программа отнимет из общей суммы 100 рублей и присвоит автоматически категорию.
 - Вызвав меню, можно настроить валюту, отредактировать сумму в кошельке и др. настройки. Так же можно вывести статистику и расход по категориям или доход за месяц.


## Frontend приложения
Я попробую сделать два варианта не зависимых друг от друга и работающих с одной базой. 

1. Конечно Телеграмм бот - самый простой и легкий способ адаптации.
2. Попробую сделать приложение для десктопа и телефонов, но позже.


## Backend приложения
Сервер, скорее всего на первое время свой, возможно задеплою на сервер, посмотрим. В целов python, alembic, postgresql, CountVectorizer, MLPClassifier .. По окончанию, скорее всего опишу все.


## Комерция проекта
0,0 - не вижу ни одной возможности и необходимости комерциализировать это, ну только если это не станет слишком дорогим в поддержании сервера с большой базой.


## Цель проекта
1. Мне нужна такая программа. Я старый, многое не помню.. тоже поймите меня..
2. Просто кодить.

Моя цель, сделать максимально простое приложение, которое не отпугнет, меня самого, потратить 2 секунды вбить + или - сумму. Для системного человека - это большая подмога для организации и подведения итогов месяца.

Лично мне, очень удобно делать в конце месяца выводы, результаты, анализировать и пересматривать статьи расхода и усиливать удачные варианты дохода. В приложении cбeр есть, что то похожее и там предусмотренно дописывать доход/расход в нале. Но я не думаю, что есть психи которые добровольно это сделают. Возможно, что то подобное есть для телефона. Все что я нашел или платное или слишком примитивное или наоборот довольно затратно в изучении функционала.

В общем, погнали, посмотрим что выйдет..