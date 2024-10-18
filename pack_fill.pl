#!/usr/bin/perl -w 
use Tk; 

# If we switch the Button we create first, we get a different result
my $mw = MainWindow->new; 
$mw->title("Pack Fill Demo");
$mw->Button(-text => "TOP", -command => sub { exit }) ->pack(-side => 'top', 
                                                             -fill => 'both');
$mw->Button(-text => "BOTTOM", -command => sub { exit }) ->pack(-side => 'bottom', 
                                                               -fill => 'both');
$mw->Button(-text => "RIGHT", -command => sub { exit }) ->pack(-side => 'right', 
                                                               -fill => 'both');
$mw->Button(-text => "LEFT", -command => sub { exit }) ->pack(-side => 'left', 
                                                              -fill => 'both');
MainLoop;