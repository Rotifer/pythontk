
#!/usr/bin/perl
use strict;
use warnings;
use Tk;

=head 
For this example, we use the easy way to place widgets in columns and rows by not explicitly 
specifying the -row and -column options. Note that the second grid command applies to two 
Button widgets, so the single -columnspan option applies to both Buttons created there. 
=cut
my $mw = MainWindow->new(-title => "Grid - spanning rows and columns explicitly");
my $fr_colspan = $mw->Frame();
$fr_colspan->pack;
$fr_colspan->Button(-text => "Button1", -command => sub { exit })->grid(
    $fr_colspan->Button(-text => "Button2", -command => sub { exit }), 
    $fr_colspan->Button(-text => "Button3", -command => sub { exit }), 
    $fr_colspan->Button(-text => "Button4", -command => sub { exit }), 
                                    -sticky => "nsew"); 

# Button5 will span Columns 0-1 and Button6 will span 2-3 
$fr_colspan->Button(-text => "Button5", -command => sub { exit })->grid(
    $fr_colspan->Button(-text => "Button6", 
                -command => sub { exit }), 
                -sticky => "nsew", 
                -columnspan => 2);

my $fr_rowspan = $mw->Frame;
$fr_rowspan->pack;
$fr_rowspan->Button(-text => "Button1", 
                    -command => sub { exit })->grid(-row => 0, 
                                                    -column => 0, 
                                                    -rowspan => 2, 
                                                    -sticky => 'nsew'); 
$fr_rowspan->Button(-text => "Button2", 
                    -command => sub { exit })->grid(-row => 0, 
                                                    -column => 1); 
$fr_rowspan->Button(-text => "Button3", 
                    -command => sub { exit })->grid(-row => 0, 
                                                    -column => 2); 
$fr_rowspan->Button(-text => "Button4", 
                    -command => sub { exit })->grid(-row => 0, 
                                                    -column => 3); 
$fr_rowspan->Button(-text => "Button5", 
                    -command => sub { exit })->grid(-row => 1, 
                                                    -column => 1); 
$fr_rowspan->Button(-text => "Button6", 
                    -command => sub { exit })-> grid(-row => 1, 
                                                     -column => 2); 
$fr_rowspan->Button(-text => "Button7", 
                    -command => sub { exit })-> grid(-row => 1, 
                                                   -column => 3);
MainLoop;