# Программа для катигоризации доходов и расходов

Рабочий вариант  - https://t.me/shliambwall_bot
Бот бесплатный и им можно пользоваться, я пользуюсь.

Телеграмм бот, который принимает информацию о расходах, доходах в наличность, пластиковые карты и крипту. Что то вроде электронной бухгалтерии. Доходу и расходу присваивается категория при помощи машинного обучения. Управлять можно через меню или командами. Так же предусмотрен вывод графиков статистики за месяц, год. 

Программа помогает анализировать объемы расходов по категориям и контролировать общий банк.

## Безопасность:

 Ни кто не хочет давать информацию о доходе и расходе в сеть или приложению, да и вообще ни кому и ни куда - это нормально и похвально. Но все же, давайте проясним:

 - Не публикуйте свою настоящую фамилию, а если и публикуете, то хотя бы не публикуйте отчество, хотя бы.
 - Закрывайте видимость в телеграмм своего номера телефона.
 - Информация подаваемая вами, несет абстрактный формат, без адреса и местоположения.
 - Тем кому нужно, они найдут о вас все что нужно и без моего приложения, оно в их списке явно не стоит. Банки сами все сольют, они обязаны по закону.
 - Если у вас есть хоть какое то сомнение хоть в чем то, не используйте мое приложение.
 - Я постарался сохранить безопастность данных и абстрактность.
 - Я ни кому не сливаю ни каких данных, хотя бы потому, что я не знаю кто вы, у меня хранятся на сервере данные в базе данных PostgreSQL запущенные в докере, к тому же, они обезличеные. Сервер на данный момент личный, находиться на моем рабочем столе.
 - При построении лубого графика, после передачи его вам в телеграмм, он тут же удаляется на сервере. Код программы открыт, вы можете проверить это сами.
 

 ## Использование: 

 - Есть меню, через которое можно внести, вывести или перенести деньги. Перенос денег из одного места в другое, не учитывается при построении статистики.
 - Так же, можно просто ввести текстом : добавить, убрать, перенести, перемещение, настройки, баланс и получить соотвествующий слову вариант взаимодействия с программой.
 - Как мнести деньги: Нажимаем в меню - "Приход", выбираем куда будем вносить, набираем на клавиатуре сумму, набираем на клавиатуре примерно источник или комментарий, программа выберит соотвествующую категорию сама, по аналогии остальные возможности.


## Frontend приложения

Я попробую сделать два варианта не зависимых друг от друга и работающих с одной базой. 

1. Конечно Телеграмм бот - самый простой и легкий способ адаптации. +
2. Попробую сделать приложение для десктопа и телефонов, но позже.


## Backend приложения

Сервер, скорее всего на первое время свой, возможно задеплою на сервер, посмотрим. В целом python, alembic, postgresql, CountVectorizer, MLPClassifier .. По окончанию, скорее всего опишу все.


## Комерция проекта

0,0 - не вижу ни одной возможности и необходимости комерциализировать это, ну только если это не станет слишком дорогим в поддержании сервера с большой базой.


## Цель проекта

Моя цель, сделать максимально простое приложение, которое не отпугнет, меня самого, потратить 2 секунды вбить + или - сумму. Для системного человека - это большая подмога для организации и подведения итогов месяца.

Лично мне, очень удобно делать в конце месяца выводы, результаты, анализировать и пересматривать статьи расхода и усиливать удачные варианты дохода. В приложении cбeр есть, что то похожее и там предусмотренно дописывать доход/расход в нале. Но я не думаю, что есть психи которые добровольно это сделают. Возможно, что то подобное есть для телефона. Все что я нашел или платное или слишком примитивное или наоборот довольно затратно в изучении функционала.

Внешний вид и примеры графиков:

<img src="https://raw.githubusercontent.com/shliamb/My-Wallet-Bot/main/img/2.png" att="My Wallet" width="auto" height="auto" align="top">


<img src="https://raw.githubusercontent.com/shliamb/My-Wallet-Bot/main/img/1.png" att="My Wallet" width="auto" height="auto" align="top">


<img src="https://raw.githubusercontent.com/shliamb/My-Wallet-Bot/main/img/3.png" att="My Wallet" width="auto" height="auto" align="top">


<img src="https://raw.githubusercontent.com/shliamb/My-Wallet-Bot/main/img/4.png" att="My Wallet" width="auto" height="auto" align="top">