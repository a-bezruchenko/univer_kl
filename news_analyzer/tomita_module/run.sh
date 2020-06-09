cd ~/tomita-parser/build/bin
rsync -auv ~/Tomita_sync/ ~/tomita-parser/build/bin/
./tomita-parser config.proto
cp -f ~/tomita-parser/build/bin/pretty.html ~/Tomita_sync/
cp -f ~/tomita-parser/build/bin/facts.txt ~/Tomita_sync/