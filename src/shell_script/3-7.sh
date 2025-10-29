#3-7.sh
#!/bin/bash

while true
do
	echo "============================="
	echo "Linux 시스템 상태 확인"
	echo "============================="
	echo "1) 사용자 정보 (w)"
	echo "2) GPU / CPU 사용률 (nvidia-smi / top)"
	echo "3) 메모리 사용량 (free)"
	echo "4) 디스크 사용량 (df)"
	echo "5) 종료"
	echo "============================="

	read -p "메뉴를 선택하세요 (1-5): " choice
	echo ""

	case $choice in
        1)
            echo "--- 1) 사용자 정보 ---"
            echo "현재 시스템에 접속된 사용자 정보를 표시합니다."
            w
            ;;

        2)
            echo "--- 2) GPU / CPU 사용률 ---"
            if command -v nvidia-smi &> /dev/null
            then
                echo "[NVIDIA GPU 사용률]"
                nvidia-smi
            else
                echo "[CPU 사용률 (1회 실행)]"
                top -b -n 1 | grep "Cpu(s)"
            fi
            ;;

        3)
            echo "--- 3) 메모리 사용량 ---"
            echo "시스템의 전체, 사용 중, 여유 메모리 (MB/GB 단위)"
            free -h
            ;;

        4)
            echo "--- 4) 디스크 사용량 ---"
            echo "마운트된 파일 시스템별 디스크 사용량 (MB/GB 단위)"
            df -h
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
