#!/bin/bash

read -p "두 개의 숫자: " num1 num2
if [ -z "$num1" ] || [ -z "$num2" ]; then
    echo "error: 두 개의 숫자 입력."
    exit 1
fi

echo "입력: num1=$num1, num2=$num2"

#덧셈
sum=$(($num1 + $num2))
echo "$num1 + $num2 = $sum"

# 뺄셈
diff=$(($num1 - $num2))
echo "$num1 - $num2 = $diff"

# 곱셈
prod=$(($num1 * $num2))
echo "$num1 * $num2 = $prod"

if [ $num2 -eq 0 ]; then
    echo "$num1 / $num2 = 0, error:divide by zero"
else
    quot=$(($num1 / $num2))
    echo "$num1 / $num2 = $quot"
fi
