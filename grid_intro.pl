#!/usr/bin/perl
use strict;
use warnings;
use Tk;

# Pay careful attention, because the second, third, and fourth calls to Button 
#  are inside the call to grid. 
# All four of the Buttons will be placed in the first row. 
# If we execute the same command again, the new widgets are placed in the next row. 
my $mw = MainWindow->new(-title => "Grid - nested");
$mw->Button(-text => 'Button1', -command => sub {$mw->destroy;})->grid( 
    $mw->Button(-text => 'Button2', -command => sub {$mw->destroy;}), 
    $mw->Button(-text => 'Button3', -command => sub {$mw->destroy;}), 
    $mw->Button(-text => 'Button4', -command => sub {$mw->destroy;}));
MainLoop;