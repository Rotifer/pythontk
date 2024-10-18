#!/usr/bin/perl -w 
use Tk; 
my $mw = MainWindow->new; 
$mw->title("Bad Window"); 
$mw->Label(-text => "This is an example of a window that looks bad\nwhen you don't send any options to pack")->pack; 
$mw->Checkbutton(-text => "I like it!")->pack; 
$mw->Checkbutton(-text => "I hate it!")->
pack; $mw->Checkbutton(-text => "I don't care")->pack; 
$mw->Button(-text => "Exit", -command => sub { exit })->pack; 
MainLoop;
