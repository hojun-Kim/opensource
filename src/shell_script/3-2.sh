#3-2.sh
#!/bin/bash

read -p "두 개 이상의 숫자 입력: " -a x_array

count=${#x_array[@]} # 배열의 총 개수
if [ $count -lt 2 ]; then
    echo "error: 두 개 이상의 숫자를 입."
    exit 1
fi

echo "y=1/2*x^2"

for x in "${x_array[@]}"
do
	y=$(echo "scale=4; 0.5 * $x * $x" | bc)

	echo "x = $x => y = $y"
done
