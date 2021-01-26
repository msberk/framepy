# Requirements
all must be on your path
- fbi
- dropbox_uploader (with access token)
- imagemagick
- exiftran

# RPi Steps

1. Image with new Raspberry Pi OS
1. Activate ssh and an initial wi-fi config by making a file named ssh and a `wpa_supplicant.conf` on `/boot` while mounted to the imaging computer
1. Boot up and log into pi (`username: pi`, `password: raspberry`)
1. Change password (`passwd`)
1. Open `sudo raspi-config`
    1. Set nice hostname (e.g. `myframe`)
    1. Set timezone to your timezone
    1. Set auto-login enabled
    1. Set wait for network at boot
1. Add a cronjob to reboot nightly
    ```bash
    sudo crontab -e

    # m h  dom mon dow   command
      0 3  *   *   *     shutdown -r now
    ```
1. Install dependencies:
    ```bash
    sudo apt-get install fbi imagemagick exiftran
    git clone https://github.com/andreafabrizi/Dropbox-Uploader.git ~/Dropbox-Uploader
    ```
1. Run initial setup and follow instructions to link to Dropbox account.
    ```bash
    dropbox_uploader.sh link
    ```
1. Clone this repository onto the device
    ```bash
    git clone https://github.com/whataberk/framepy.git ~/framepy
    ```
1. Set up .bash_profile according to example

# Docker
After some work, I don't really recommend Docker for this.
This is pretty much a one-trick-pony pi setup and it'd probably make more sense to codify the above as a setup shell script than tax a Pi with running Docker.
If you do want to use Docker, though, then if you are using default 'pi' user just copy `.env-example` to `.env` and hopefully it should work as expected.