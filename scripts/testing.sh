#! /bin/bash

# Скрипт копирует всю девелопмент базу данных в тестовую. 
# Должен запускаться перед прохоном тестов.

TEST_DB_NAME='lr_test'
DEV_DB_NAME='lr_dev'

PYLINT_PATH='reports/pylint'
COVERAGE_PATH='reports/coverage'
NOSE_FILE='reports/nose.xml'

SUCCESS='\033[32m'
WARNING='\033[33m'
ERROR='\033[31m'
INFO='\033[36m'
RESET='\033[0m'


cd ../
source env/bin/activate
find .* -name "*.pyc" | xargs rm  1>/dev/null 2>/dev/null
find .* -name ".coverage" | xargs rm  1>/dev/null 2>/dev/null

rm -rf $PYLINT_PATH
rm -rf $COVERAGE_PATH
rm $NOSE_FILE

mongodump --db $DEV_DB_NAME -o 'tmp_dump/' 1>/dev/null
mongorestore --db $TEST_DB_NAME --drop 'tmp_dump/'$DEV_DB_NAME'/'  1>/dev/null 2>/dev/null
rm -rf 'tmp_dump'

echo -en $SUCCESS'Копирование девелопмент базы данных в тестовую выполнено успешно. '$RESET'
'$INFO'Коллекции:'$RESET'
'

mongo $TEST_DB_NAME --eval 'printjson(db.getCollectionNames())' 

echo -en '
'$INFO'Выполняем тесты:'$RESET'
'

coverage erase
nosetests --with-coverage --with-xunit --xunit-file $NOSE_FILE
coverage html

pylint_create_report ()
{
    echo -en $1'...  '
    pylint $1 1> $PYLINT_PATH'/'$1'.html'
}


while getopts ":p" opt; do
  case $opt in
    p)
        mkdir $PYLINT_PATH
        echo -en $INFO'Создание отчётов по коду: 
        '

        pylint_create_report 'server.py'
        pylint_create_report 'forms'
        pylint_create_report 'models'
        pylint_create_report 'handlers'
        pylint_create_report 'units'
        pylint server.py forms/*.py models/*.py handlers/*.py units/*.py 1> $PYLINT_PATH'/result.html'

        echo -en $SUCCESS' выполнено.'$RESET'
        '
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done



echo -en $INFO'Создание отчётов по профилированию...
'$RESET
./scripts/profiling_create_rep.py
echo -en $SUCCESS' выполнено.'$RESET'
'