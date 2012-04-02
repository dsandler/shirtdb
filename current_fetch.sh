#!/bin/sh

#cd /home/dsandler/dsandler.org/tools/shirtdb/preview
SITEDIR=/home/dsandler/web/shirts
cd $SITEDIR/preview

if [ "$1" = "" ]; then
	wget --recursive --level=1 --accept=jpg --no-parent http://keepernotes.com/shirts/
	cd keepernotes.com/shirts
	# fixup
	test -f 2010.wiess-front.jpg \
		&& mv 2010.wiess-front.jpg 2010-wiess-front.jpg
	test -f 1998-back-front.jpg \
		&& mv 1998-back-front.jpg 1998-baker-front.jpg 

	for x in *.jpg; do
		convert -geometry 200x200 -quality 80 $x $SITEDIR/preview/$x
		convert -geometry 1024x1024 -quality 75 $x $SITEDIR/big/$x

		echo $x
	done
	
	python $SITEDIR/scaletrim.py 96x96 *.jpg
	rename -f 's/\.trim//' *.trim.jpg
	mv *.jpg $SITEDIR/thumb/

	cd $SITEDIR/preview
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
