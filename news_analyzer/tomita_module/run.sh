cd ~/tomita-parser/src/bin
cp -r -f ~/Tomita_sync/* ~/tomita-parser/build/bin
./tomita-parser config.proto
cp -f ~/tomita-parser/build/bin/pretty.html ~/Tomita_sync/