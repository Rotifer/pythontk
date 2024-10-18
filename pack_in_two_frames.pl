#!/usr/bin/perl -w 
use Tk; 

# Not in book.
# Try changing the -fill, -expand and -anchors of the containing frames

my $mw = MainWindow->new;
$mw->title("Pack Fill Demo");

my $frm1 = $mw->Frame()->pack();
my $frm2 = $mw->Frame()->pack();
$frm1->Button(-text => "DONE1", -command => sub { exit }) ->pack(-side => 'left', 
                                                               -anchor => 'n');
$frm1->Button(-text => "DONE2", -command => sub { exit }) ->pack(-side => 'left', 
                                                               -anchor => 'n');
$frm1->Button(-text => "DONE3", -command => sub { exit }) ->pack(-side => 'left', 
                                                               -anchor => 'n');
$frm2->Button(-text => "DONE4", -command => sub { exit }) ->pack(-side => 'top', 
                                                               -anchor => 'w');
$frm2->Button(-text => "DONE5", -command => sub { exit }) ->pack(-side => 'top', 
                                                               -anchor => 'w');
$frm2->Button(-text => "DONE6", -command => sub { exit }) ->pack(-side => 'top', 
                                                               -anchor => 'w');
MainLoop;