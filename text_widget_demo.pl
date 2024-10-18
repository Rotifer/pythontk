#!/usr/bin/perl
use strict;
use warnings;
use Tk;

my $filename = '';
my $info = '';
my $mw = MainWindow->new;
# Create necessary widgets
my $f = $mw->Frame->pack(-side => 'top', -fill => 'x');
$f->Label(-text => "Filename:")->pack(-side => 'left', -anchor => 'w');
$f->Entry(-textvariable => \$filename)->pack(-side => 'left', 
   -anchor => 'w', -fill => 'x', -expand => 1);
$f->Button(-text => "Exit", -command => sub { exit; } )->
  pack(-side => 'right');
$f->Button(-text => "Save", -command => \&save_file)->
  pack(-side => 'right', -anchor => 'e');
$f->Button(-text => "Load", -command => \&load_file)->
  pack(-side => 'right', -anchor => 'e');
$mw->Label(-textvariable => \$info, -relief => 'ridge')->
  pack(-side => 'bottom', -fill => 'x');
my $t = $mw->Scrolled("Text")->pack(-side => 'bottom', 
  -fill => 'both', -expand => 1);

MainLoop;

# load_file checks to see what the filename is and loads it if possible
sub load_file {
  $info = "Loading file '$filename'...";
  $t->delete("1.0", "end");
  if (!open(FH, "$filename")) {
    $t->insert("end", "ERROR: Could not open $filename\n"); 
    return; 
  }
  while (<FH>) { $t->insert("end", $_); }
  close (FH);
  $info = "File '$filename' loaded";
}

# save_file saves the file using the filename in the Entry box.
sub save_file {
  $info = "Saving '$filename'";
  open (FH, ">$filename");
  print FH $t->get("1.0", "end");
  $info = "Saved.";
}