pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade

pip install akshare --upgrade -i https://pypi.org/simple

python update_position.py
python track_market_value.py
echo %d% %t%
set t=%time:~0,8%
echo %d% %t% > ./batch_time_stamp.txt