export PATH=/home/pi/Dropbox-Uploader:$PATH

echo "Sleeping 10 seconds to allow network to come up..."
sleep 10
git -C ~/framepy pull --rebase
chmod +x ~/framepy/*
~/framepy/frame.py
