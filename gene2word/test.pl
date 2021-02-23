#!/usr/bin/env perl

use warnings;
use strict;
use File::Spec;

print "hi!\n\n\n";
print( (File::Spec->splitpath(File::Spec->rel2abs(__FILE__)))[1] . "\n");
print "\n\n\nbye!\n";
