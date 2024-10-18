#!/usr/bin/perl -w 
use Tk; 
my $mw = MainWindow->new; 
$mw->title("Pack Demo"); 
$mw->Button(-text => "TOP", -command => sub { exit }) ->pack(-side => 'top'); 
$mw->Button(-text => "BOTTOM", -command => sub { exit }) ->pack(-side => 'bottom'); 
$mw->Button(-text => "RIGHT", -command => sub { exit }) ->pack(-side => 'right'); 
$mw->Button(-text => "LEFT", -command => sub { exit }) ->pack(-side => 'left'); 
MainLoop;