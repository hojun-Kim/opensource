#3-4.sh
#!/bin/bash

scores=()

calculate_average() {
    count=${#scores[@]}

    if [ $count -eq 0 ]; then
        echo "error: 입력된 점수가 없음."
        return 1 # 실패 반환
    fi

    total_sum=0
    for s in "${scores[@]}"; do
        total_sum=$(($total_sum + $s))
    done

    avg_score=$(($total_sum / $count))

    return 0
}

while true
do
    # --- 1. 메뉴 출력 ---
    echo "==================="
    echo "1) 과목 성적 추가"
    echo "2) 입력된 모든 점수 보기"
    echo "3) 평균 점수 확인"
    echo "4) 평균 등급 (A/B) 변환"
    echo "5) 종료"
    echo "==================="

    read -p "메뉴를 선택하세요 (1-5): " choice
    echo ""

    case $choice in
	    1)
	    echo "--- 1) 과목 성적 추가 ---"
            read -p "추가할 점수를 입력하세요 (0-100): " new_score

	    if ! [[ "$new_score" =~ ^[0-9]+$ ]] || [ $new_score -lt 0 ] || [ $new_score -gt 100 ]; then
                echo "오류: '$new_score' - 점수는 0에서 100 사이의 정수여야 합니다."
            else
		    scores+=($new_score)
                echo "$new_score 점이 성공적으로 추가되었습니다."
            fi
	    ;;
    2)
	    echo "--- 2) 입력된 모든 점수 보기 ---"
            count=${#scores[@]}
            if [ $count -eq 0 ]; then
                echo "입력된 점수가 없습니다."
            else
                # ${scores[@]} : 배열의 모든 요소를 출력
                echo "총 ${count}개 점수: ${scores[@]}"
            fi
	    ;;
    3)
	    echo "--- 3) 평균 점수 확인 ---"
            # 헬퍼 함수 호출, 'if'로 성공(0) 여부 확인
            if calculate_average; then
                echo "총점: $total_sum"
                echo "과목 수: $count"
                echo "평균 점수 (정수): $avg_score"
            fi
	    ;;
    4)
	    echo "--- 4) 평균 등급 (A/B) 변환 ---"
            if calculate_average; then
                if [ $avg_score -ge 90 ]; then
                    avg_grade="A"
                else
                    avg_grade="B"
                fi
                echo "평균 점수 $avg_score 는 등급으로 '$avg_grade' 입니다."
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

	echo ""
done
