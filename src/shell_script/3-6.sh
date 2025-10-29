#3-6.sh
#!/bin/bash

read -p "전달할 2개 이상의 인자를 입력: " -a input_array

count=${#input_array[@]}
if [ $count -lt 2 ]; then
    echo "error: 2개 이상의 인자가 필요."
    exit 1
fi

echo "[셸] Python(3-6.py)를 호출"
echo "[셸] Python에 전달할 인자: ${input_array[@]}"
python3 3-6.py "${input_array[@]}"

echo "--- [셸] 3-6.sh 종료 ---"
