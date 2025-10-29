#3-8.sh
#!/bin/bash

echo "--- 1. 'DB' 폴더 확인 및 생성 ---"
mkdir -p "DB"
echo "'DB' 폴더가 준비되었습니다."
echo ""

echo "DB 폴더에 5개 파일 생성 중 (file1.txt ~ file5.txt)..."
for i in {1..5}
do
    echo "이것은 file${i}의 내용입니다." > "DB/file${i}.txt"
done

echo "DB 폴더 내에서 파일 압축 중 (db_files.tar.gz)..."
tar -czvf "DB/db_files.tar.gz" -C "DB" file1.txt file2.txt file3.txt file4.txt file5.txt
echo "압축 완료."
echo ""

echo "--- 3. 'train' 폴더 생성 및 5개 파일 링크 ---"
mkdir -p "train"

CURRENT_DIR=$(pwd)
echo "'train' 폴더에 5개 원본 파일의 심볼릭 링크 생성..."
for i in {1..5}
do
	local_target="$CURRENT_DIR/DB/file${i}.txt"
	local_link="train/link_file${i}.txt"
	ln -sf "$local_target" "$local_link"
done

echo "[DB 폴더 내용]"
ls -l DB
echo ""
echo "[train 폴더 내용]"
ls -l train
echo ""
echo "[링크된 파일 내용 확인 (예: link_file1.txt)]"
cat "train/link_file1.txt"
