#!/usr/bin/perl
use strict;
use warnings;
use Tk;

=head 
This code will assign the -weight of 1 to every single row and column in the grid, 
no matter what size the grid is. 
Of course, this example works only if you want to assign the same size to each row and each column, 
but you get the idea.
Watch what happens when you re-size!
Here is an example of how the -weight option works:
=cut
my $mw = MainWindow->new(-title => "Grid - weight");
$mw->Button(-text => "Button1", -command => sub { exit })->grid(
    $mw->Button(-text => "Button2", -command => sub { exit }), 
    $mw->Button(-text => "Button3", -command => sub { exit }),
    $mw->Button(-text => "Button4", -command => sub { exit }), -sticky => "nsew"); 
    $mw->Button(-text => "Button5", -command => sub { exit })->grid (
        "x", $mw->Button(-text => "Button7", -command => sub { exit }), 
        $mw->Button(-text => "Button8", -command => sub { exit }), -sticky => "nsew"); 

$mw->gridColumnconfigure(1, -weight => 1); 
$mw->gridRowconfigure(1, -weight => 1);
MainLoop;