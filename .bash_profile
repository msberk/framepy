export PATH=/home/pi/Dropbox-Uploader:$PATH

git -C ~/framepy pull --rebase
~/framepy/frame.py /path/to/frame/pictures/on/dropbox --randomize --timeout 30 --hori 1920 --vert 1080
# Docker config example
# docker-compose -f ~/framepy/docker-compose.yml --rm framepy /path/to/frame/pictures/on/dropbox --randomize --timeout 30 --hori 1920 --vert 1080
