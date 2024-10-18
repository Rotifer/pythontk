#!/usr/bin/perl
use strict;
use warnings;
use Tk;

=head
import tkinter as tk

colours = ['red','green','orange','white','yellow','blue']

r = 0
for c in colours:
    tk.Label(text=c, relief=tk.RIDGE, width=15).grid(row=r,column=0)
    tk.Entry(bg=c, relief=tk.SUNKEN, width=10).grid(row=r,column=1)
    r = r + 1

tk.mainloop()
=cut

my $mw = MainWindow->new(-title => "Grid - Python Example");
my @colours = qw(red green orange white yellow blue);

my $r = 0;
foreach my $c (@colours) {
    $mw->Label(-text => $c, -relief => 'ridge', -width => 15)->grid(-row => $r,-column => 0);
    $mw->Entry(-bg => $c, -relief => 'sunken', -width => 10)->grid(-row => $r, -column => 1);
    $r++;
}
MainLoop;