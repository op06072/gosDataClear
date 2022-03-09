zip -9 ~/PycharmProjects/gosDataClear/gos.zip ~/PycharmProjects/gosDataClear -x '*.*i*'
cd ~/PycharmProjects/gosDataClear
git add ./gos.zip
git add ./dataclear.py
git add ./make.sh
git commit -m "made with script"
git push origin master
cd ~/PycharmProjects
