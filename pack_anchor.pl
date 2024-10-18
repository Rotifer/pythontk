#!/usr/bin/perl -w 
use Tk; 

# Change anchor options to 'w' and observe the result.
my $mw = MainWindow->new; 
$mw->title("Pack Fill Demo");
$mw->Button(-text => "DONE1", -command => sub { exit }) ->pack(-side => 'left', 
                                                               -anchor => 'n');
$mw->Button(-text => "DONE2", -command => sub { exit }) ->pack(-side => 'left', 
                                                               -anchor => 'n');
$mw->Button(-text => "DONE3", -command => sub { exit }) ->pack(-side => 'left', 
                                                               -anchor => 'n');

MainLoop;