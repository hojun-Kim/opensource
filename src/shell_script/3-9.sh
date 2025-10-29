#3-9.sh
#!/bin/bash

DB_FILE="DB.txt"
touch "$DB_FILE"

while true
do
    echo "==================="
    echo "1) 팀원 정보 추가"
    echo "2) 팀원과 한 일 기록"
    echo "3) 팀원 검색 (이름)"
    echo "4) 수행 내용 검색 (날짜/키워드)"
    echo "5) 종료"
    echo "==================="
    read -p "메뉴를 선택하세요 (1-5): " choice
    echo ""

    case $choice in
        1)
            echo "--- 1) 팀원 정보 추가 ---"
            read -p "추가할 팀원 이름: " name
            read -p "생일 또는 전화번호: " info

            echo "MEMBER | $name | $info" >> "$DB_FILE"
            echo "[$name] 님의 정보를 $DB_FILE 에 저장했습니다."
            ;;

        2)
            echo "--- 2) 팀원과 한 일 기록 ---"
            default_date=$(date +%Y-%m-%d)
            read -p "날짜 (기본값: $default_date): " log_date

            if [ -z "$log_date" ]; then
                log_date=$default_date
            fi

            read -p "수행한 일 내용: " activity

            echo "LOG | $log_date | $activity" >> "$DB_FILE"
            echo "[$log_date] 활동을 $DB_FILE 에 저장했습니다."
            ;;

        3)
            echo "--- 3) 팀원 검색 (이름) ---"
            read -p "검색할 팀원 이름: " search_name
            echo ""
            echo "[$search_name] (으)로 검색된 팀원 정보:"
            result=$(grep "^MEMBER" "$DB_FILE" | grep -i "$search_name")

            if [ -z "$result" ]; then
                echo "일치하는 팀원 정보가 없습니다."
            else
                echo "$result"
            fi
            ;;

        4)
            echo "--- 4) 수행 내용 검색 (날짜/키워드) ---"
            read -p "검색할 날짜(YYYY-MM-DD) 또는 키워드: " search_keyword
            echo ""
            echo "[$search_keyword] (으)로 검색된 수행 내용:"

            result=$(grep "^LOG" "$DB_FILE" | grep -i "$search_keyword")

            if [ -z "$result" ]; then
                echo "일치하는 수행 내용이 없습니다."
            else
                echo "$result"
            fi
            ;;

        5)
            echo "프로그램을 종료합니다."
            break
            ;;

        *)
            echo "잘못된 입력입니다. 1에서 5 사이의 숫자를 입력하세요."
            ;;
    esac

done
