#!/usr/bin/perl
use strict;
use warnings;
use Tk;

=head 
The "x" character translates to "skip this space" and leaves a hole in the grid. 
We removed the line that created Button6 and replaced it with an "x" in the following code.
The cell is still there, it just doesn't contain a widget. 
=cut
my $mw = MainWindow->new(-title => "Grid - empty cells");
$mw->Button(-text => "Button1", -command => sub { exit })->grid(
    $mw->Button(-text => "Button2", -command => sub { exit }), 
    $mw->Button(-text => "Button3", -command => sub { exit }), 
    $mw->Button(-text => "Button4", -command => sub { exit })); 
    $mw->Button(-text => "Button5", -command => sub { exit })->grid (
        "x", $mw->Button(-text => "Button7", -command => sub { exit }), 
        $mw->Button(-text => "Button8", -command => sub { exit })); 
MainLoop;
