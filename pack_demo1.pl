#!/usr/bin/perl
use strict;
use warnings;
use Tk; 
require Tk::BrowseEntry; 

# Here are three little programs that let you experiment with the packing 
#  options of an unspecified number of widgets.
my $numWidgets = 0;
if ($#ARGV >= 0) { 
        $numWidgets = $ARGV[0]; 
    } else { 
        $numWidgets = 4; 
} 
my $mw = MainWindow->new(-title => "Play w/pack"); 
my $f = $mw->Frame(-borderwidth => 2, -relief => 'groove')->pack(-side => 'top', 
                                                                  -fill => 'x');
my (@packdirs) = ( ); 
my $i = 0; 
foreach (0..$numWidgets) { 
    $packdirs[$_] = 'top'; 
    my $be = $f->BrowseEntry(-label => "Widget $_:", 
                             -choices => ["right", "left", "top", "bottom"], 
                             -variable => \$packdirs[$_], 
                             -browsecmd => \&repack)->pack(-ipady => 5);
 } 
$f->Button(-text => "Repack", -command => \&repack )->pack(-anchor => 'center'); 
# use a separate window so we can see what the output # looks like without clutter. 
my $top = $mw->Toplevel(-title => "output window"); 
my $c; 
foreach (@packdirs) { 
    my $b = $top->Button(-text => $c++ . ": $_", 
                         -font => "Courier 20 bold")->pack(-side => $_, 
                                                           -fill => 'both', 
                                                           -expand => 1);
} 
MainLoop; 

sub repack { 
    my @w = $top->packSlaves; 
    foreach (@w) { $_->packForget; } 
        my $e = 0; 
        foreach (@w) { 
            $_->configure(-text => "$e: $packdirs[$e]"); 
            $_->pack(-side => $packdirs[$e++], -fill => 'both', 
                                               -expand => 1) ;
    } 
}