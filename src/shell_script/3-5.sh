#3-5.sh
#!/bin/bash

run_ls_with_options() {
	local command_to_run="ls $@"

	echo "--- eval로 실행될 명령어 문자열 ---"
    	echo "$command_to_run"

	eval $command_to_run
}

echo "스크립트에 전달된 인자: $@"
echo ""

run_ls_with_options "$@"
