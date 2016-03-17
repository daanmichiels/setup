set fname=%date:~10,4%-%date:~4,2%-%date:~7,2%
xcopy "C:\Users\daan\thesis" "C:\Users\daan\Dropbox\thesis-backup\%fname%" /f /i /y

