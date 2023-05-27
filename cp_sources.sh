#rshell --port /dev/ttyACM0 --buffer-size 32 --editor nano rsync -m sources /pyboard
rshell --port /dev/ttyACM0 --editor nano cp sources/run_demo.py /pyboard
rshell --port /dev/ttyACM0 --editor nano cp sources/hw.py /pyboard