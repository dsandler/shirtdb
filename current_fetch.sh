#!/bin/sh

cd /home/dsandler/dsandler.org/tools/shirtdb/preview

if [ "$1" = "" ]; then
	wget --recursive --level=1 --accept=jpg --no-parent http://keepernotes.com/shirts/
	pushd keepernotes.com/shirts
	for x in *.jpg; do
		convert -geometry 200x200 $x ../../$x

		echo $x
	done
	
	python ../../../scaletrim.py 96x96 *.jpg
	rename -f 's/\.trim//' *.trim.jpg
	mv *.jpg ../../../thumb/

	popd
	rm -r keepernotes.com
else
	# just a few
	for URL in "$@"; do
		curl -O "$URL"
		fn=`basename "$URL"`
		mogrify -geometry 96x96 "$fn"
		echo "$fn"
	done
fi
