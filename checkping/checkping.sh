#!/bin/bash



# Этот скрипт был написан в результате покупки свистка (адаптера wi-fi) «Tp-Link TL-WN722N»,
# который я так и не смог заставить нормально держать связь.
# Довольно долго изголялся - но всё-таки продал. Задолбал!!!

# Добавляем этот скрипт в cron, запускаем, например, каждую минуту.

# Что пингуем
IP1=192.168.0.1

# Переменная для результатов проверки
RES1=0

ping -q -c 1 $IP1 > /dev/null && RES1=1

# Если адрес не ответил - перезапускаем интерфейс eth0
if [ $RES1 = 0 ]
then
    sudo /etc/init.d/net.wlp0s20u3 restart
    echo "Сеть перезапускалась - `date '+%A %m/%d/%y : %H:%M:%S'`" >> ~/count_restart
fi
