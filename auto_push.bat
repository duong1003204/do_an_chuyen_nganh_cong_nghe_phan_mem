@echo off
echo ==== AUTO GIT PUSH START ====
cd /d "C:\Users\duong\OneDrive\Desktop\DACNCNPM"
git add .
git commit -m "Auto update %date% %time%"
git push origin main
echo ==== DONE ====
pause
