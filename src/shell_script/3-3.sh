#3-3.sh
#!/bin/bash

read -p "점수 입력 : " -a score_array

count=${#score_array[@]}
if [ $count -lt 2 ]; then
    echo "error: 두 개 이상의 점수를 입력."
    exit 1
fi

total_sum=0

echo "각각 등급"

for score in "${score_array[@]}"
do
	if ! [[ "$score" =~ ^[0-9]+$ ]] || [ $score -lt 0 ] || [ $score -gt 100 ]; then
        echo "error: '$score' - 0<= score <=100"
        exit 1
    fi

    if [ $score -ge 90 ]; then
        grade="A"
    else
        grade="B"
    fi

    echo "점수: $score  =>  등급: $grade"
    total_sum=$(($total_sum + $score))
done

echo "평균 등급"
avg_score=$(($total_sum / $count))

echo "총점: $total_sum"
echo "과목 수: $count"
echo "평균 점수: $avg_score"
if [ $avg_score -ge 90 ]; then
    avg_grade="A"
else
    avg_grade="B"
fi

echo "평균 등급: $avg_grade"

