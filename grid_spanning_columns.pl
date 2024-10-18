#!/usr/bin/perl
use strict;
use warnings;
use Tk;

=head
The following bit of code creates three rows of Buttons. 
The first two rows are normal and, in the third, the second Button spans three columns.
Each "-" character adds one to the number of columns the Button uses, and the default is one. 
So the original column and two hyphens ("-","-") indicate that there are three columns to span. 
The -sticky option is necessary for the widgets to stick to the sides of the cells they span. 
If the -sticky option were left out, the Button would be centered across the three cells it spans. 
=cut
my $mw = MainWindow->new(-title => "Grid - column spanning");
$mw->Button(-text => "Button1", -command => sub { exit })->grid(
    $mw->Button(-text => "Button2", -command => sub { exit }), 
    $mw->Button(-text => "Button3", -command => sub { exit }), 
    $mw->Button(-text => "Button4", -command => sub { exit })); 
    $mw->Button(-text => "Button5", -command => sub { exit })->grid(
        $mw->Button(-text => "Button6", -command => sub { exit }), 
        $mw->Button(-text => "Button7", -command => sub { exit }), 
        $mw->Button(-text => "Button8", -command => sub { exit })); 
        $mw->Button(-text => "Button9", -command => sub { exit })->grid(
            $mw->Button(-text => "Button10",
                         -command => sub { exit }), "-", "-", 
                         -sticky => "nsew");
MainLoop;