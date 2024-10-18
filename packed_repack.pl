#!/usr/bin/perl -w 
use Tk; 
my $mw = MainWindow->new; 

# The GUI only matches the book image when the Enlarge button is packed *before*
# the "Exit" button.
$mw->title("Good Window"); 
$mw->Label(-text => "This window looks much more organized, and less haphazard\n" . 
                        "because we used some options to make it look nice")->pack;
$mw->Button(-text => "Enlarge", -command => \&repack_kids)->pack(-side => 'bottom',
                                                                -anchor => 'center'); 
$mw->Button(-text => "Exit", 
            -command => sub { exit })->pack(-side => 'bottom', 
                                            -expand => 1, 
                                            -fill => 'x'); 
$mw->Checkbutton(-text => "I like it!")->pack(-side => 'left', -expand => 1); 
$mw->Checkbutton(-text => "I hate it!")->pack(-side => 'left', -expand => 1); 
$mw->Checkbutton(-text => "I don't care")->pack(-side => 'left', -expand => 1); 
                                                                
sub repack_kids { 
    my @kids = $mw->packSlaves; 
    foreach (@kids) { 
        $_->pack(-ipadx => 20, -ipady => 20); 
    }
}
MainLoop;