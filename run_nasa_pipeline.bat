@echo off
cd C:\Users\peace\DE
where python
python --version
python pipeline.py
echo Done! >> pipeline_log.txt
pause
