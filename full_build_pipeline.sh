./build.sh -s ~/.ssh/id_rsa -n "Docker_LolBetStats" -e "r@spberry.com"
docker save -o lolbetstats.armv7.tar lolbetstats:latest
scp lolbetstats.armv7.tar 192.168.0.12:/media/Romain/
