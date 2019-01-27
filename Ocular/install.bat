@echo off

cmd /K "cd C:\"
mkdir Ocular
cd Ocular

bitsadmin /transfer myDownloadJob /download /priority normal https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe C:\Ocular\python37.zip
python37.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

del /f python37.exe

echo "Installation finished..."
echo.
set /p response1="Want to check the installation? Y/n "
if %response1%==Y echo Python-3.7.0 installed.

rem cmd /K "cd C:\Users\User\AppData\Local\Programs\Python\Python37"

pip install numpy
pip install pandas
pip install matplotlib
pip install scipy
pip install scikit-learn
pip install opencv-python

echo "Libraries installation finished..."
echo.
set /p response2="Want to check the installation? Y/n "
if %response2%==Y pip freeze
echo "WARNING: Do not close command window. Execution in process."
echo.
echo "Please wait..."
echo.

rem cmd /K "cd C:\Ocular"

rem bitsadmin /transfer myDownloadJob /download /priority normal <---python script link---> C:\Ocular\init.py
bitsadmin /transfer myDownloadJob /download /priority normal https://github.com/adi-797/Eye-BioAnalysis-OpenCV/blob/Srajan/Ocular/gui.py C:\Ocular\gui.py
bitsadmin /transfer myDownloadJob /download /priority normal https://github.com/adi-797/Eye-BioAnalysis-OpenCV/blob/Srajan/Ocular/log.py C:\Ocular\log.py
bitsadmin /transfer myDownloadJob /download /priority normal https://github.com/adi-797/Eye-BioAnalysis-OpenCV/blob/Srajan/Ocular/model.py C:\Ocular\model.py
bitsadmin /transfer myDownloadJob /download /priority normal https://github.com/adi-797/Eye-BioAnalysis-OpenCV/blob/Srajan/Ocular/logo.png C:\Ocular\logo.png
bitsadmin /transfer myDownloadJob /download /priority normal https://github.com/adi-797/Eye-BioAnalysis-OpenCV/blob/Srajan/Ocular/application.bat C:\Ocular\application.bat
bitsadmin /transfer myDownloadJob /download /priority normal https://github.com/adi-797/Eye-BioAnalysis-OpenCV/blob/Srajan/Ocular/Readme.txt C:\Ocular\readme.txt

set /p response3="Want to run the application now? Y/n "
if %response3%==Y (python application.py) else (readme.txt)

echo "Thank you for using Ocular."
echo.
echo "Kindly open readme.txt for future refrence. Or run application.bat for using the Ocular module."
echo.

pause
exit
