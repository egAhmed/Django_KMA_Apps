@ECHO OFF

start cmd.exe /k "activate djenv && D: && cd D:\Django_Project\Projects\Django_KMA_Apps\ && python manage.py runserver 0.0.0.0:8010"

# start C:\"Program Files (x86)"\Google\Chrome\Application\chrome.exe "http://localhost:8010/"

start C:\"Program Files (x86)"\Opera\launcher.exe "http://localhost:8010/"