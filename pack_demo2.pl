#!/usr/bin/perl
use strict;
use warnings;
use Tk; 
require Tk::BrowseEntry; 

my $numWidgets;
if ($#ARGV >= 0) { 
    $numWidgets = $ARGV[0]; 
} else { 
    $numWidgets = 1; 
} 
my $mw = MainWindow->new(-title => "Play w/pack"); 
my $f = $mw->Frame(-borderwidth => 2, 
                   -relief => 'groove')->pack(-side => 'top',
                                              -fill => 'x'); 
# Initialize the variables 
# Populating this list fixes the uninitialised variables warning for line 30.
my @packdirs = (0..$numWidgets); 
my @anchordirs; 
my @fill;
my @expand; 
my $i = 0; 
my $top = $mw->Toplevel(-title => "output window"); 
my $addbutton = $f->Button(-text => "Add Widget", 
                           -command => \&addwidget )->pack(-anchor => 'center'); 
foreach (0..$numWidgets) { 
    # This line throws a warning about an unitialised variable 
    #  that is fixed by initialising @packdirs on line 18.
    my $b = $top->Button(-text => $_ . ": $packdirs[$_]")->pack;
    #my %pinfo = $b->packInfo; # %pinfo isn't used anywhere
    $b->packForget; 
    &addwidget($_);
} 
MainLoop;


sub repack { 
    print "Repacking..."; 
    my @w = $top->packSlaves; 
    foreach (@w) { $_->packForget; } 
    my $e = 0; 
    foreach (@w) { 
        $_->configure(-text => "$e: $packdirs[$e]"); 
        print "Expand is : " . $expand[$e]. "\n"; 
        $_->pack(-side => $packdirs[$e], 
                 -fill => $fill[$e], 
                 -expand => $expand[$e], 
                 -anchor => $anchordirs[$e]); 
        $e++; 
    } 
} 

sub addwidget { 
    my $count = shift; 
    print "COUNT $count\n"; 
    if (! defined $count) { 
        $numWidgets ++; 
        $count = $numWidgets ; 
    } 
    $packdirs[$count] = 'top'; 
    $anchordirs[$count] = 'center'; 
    $fill[$count] = 'none'; 
    $expand[$count] = 0; 
    my $f1 = $f->Frame->pack(-side => 'top', 
                             -expand => 1, 
                             -fill =>'y', 
                             -before => $addbutton); 
    my $be = $f1->BrowseEntry(-label => "Widget $count:", 
                              -choices => ["right", "left", "top", "bottom"], 
                              -variable => \$packdirs[$count], 
                              -browsecmd => \&repack) ->pack(-ipady => 5, 
                                                             -side => 'left'); 
    $f1->BrowseEntry(-label => "-anchor", 
                     -choices => [qw/center n s e w ne se nw sw/], 
                     -variable => \$anchordirs[$count], 
                     -browsecmd => \&repack)->pack(-ipady => 5, 
                                                   -side => 'left'); 
    $f1->BrowseEntry(-label => "-fill", 
                     -choices => [qw/none x y both/], 
                     -variable => \$fill[$count], 
                     -browsecmd => \&repack)->pack(-ipady => 5, 
                                                   -side => 'left'); 
    $f1->Checkbutton(-text => "-expand", 
                     -onvalue => 1, 
                     -offvalue => 0, 
                     -variable => \$expand[$count], 
                     -command => \&repack)->pack(-ipady => 5, 
                                                 -side => 'left'); 
    $top->Button(-text => $count . ": $packdirs[$count]", 
                 -font => "Courier 20 bold")->pack(-side => $packdirs[$count], 
                                                   -fill => $fill[$count], 
                                                   -expand => $expand[$count]); 
}