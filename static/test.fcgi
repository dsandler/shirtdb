#!/usr/bin/perl

#-----------------------
#  CODE THAT RUNS ONCE
#-----------------------
     $counter=0;

#---------------------------------
#  CODE THAT RUNS EVERY TIME
#---------------------------------

use FCGI;
while ( FCGI::accept() >= 0 ) {
      print "Content-type:text/html\n\n";
	  $counter++;
      print "I have run $counter times.";
}
