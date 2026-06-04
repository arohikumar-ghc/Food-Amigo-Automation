@echo off
echo Syncing changes to repository...
cd "C:\Users\Arohi\Desktop\Food Amigo Automation"
git add .
git commit -m "Updated: %date% %time%"
git push
echo.
echo Done! Changes pushed to repository.
pause
