#!/usr/bin/perl
use strict;
use warnings;
use Tk;

=head 
n this example, the -ipady and -ipadx options are applied to the top row of Buttons and 
not the bottom row:
=cut
my $mw = MainWindow->new(-title => "Grid - spanning rows and columns explicitly");
my $fr_first = $mw->Frame;
$fr_first->pack;

$fr_first->Button(-text => "Button1", 
                  -command => sub { exit })->grid(
                    $mw->Button(-text => "Button2", 
                                -command => sub { exit }),
                    $mw->Button(-text => "Button3", 
                                -command => sub { exit }), 
                    $mw->Button(-text => "Button4", 
                                -command => sub { exit }), 
                   -sticky => "nsew", 
                   -ipadx => 10, 
                   -ipady => 10);
my $fr_second = $mw->Frame;
$fr_second->pack;                                
$fr_second->Button(-text => "Button5", 
                   -command => sub { exit })->grid(
                        $fr_second->Button(-text => "Button6", 
                                            -command => sub { exit }), 
                        $fr_second->Button(-text => "Button7", 
                                             -command => sub { exit }), 
                        $fr_second->Button(-text => "Button8", 
                                            -command => sub { exit }), 
                    -sticky => "nsew");
MainLoop;