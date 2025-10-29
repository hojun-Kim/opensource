# 3-0.sh
#!/bin/bash

grep -qFx 'export MYENV="Hello Shell"' ~/.bashrc || echo 'export MYENV="Hello Shell"' >> ~/.bashrc

source ~/.bashrc
bash -c 'echo $MYENV'

sed -i '\#export MYENV="Hello Shell"#d' ~/.bashrc
unset MYENV
bash -c 'echo $MYENV'
