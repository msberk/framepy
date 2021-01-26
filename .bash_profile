export PATH=/home/pi/Dropbox-Uploader:$PATH

echo "Sleeping 10 seconds to allow network to come up..."
sleep 10
git -C ~/framepy pull --rebase
~/framepy/frame.py /path/to/frame/pictures/on/dropbox --randomize --timeout 30
# Docker config
# export UID=$(id -u)
# export GID=$(id -g)
# docker-compose -f ~/framepy/docker-compose.yml --rm framepy /path/to/frame/pictures/on/dropbox --randomize --timeout 30
