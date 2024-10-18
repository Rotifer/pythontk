# Notes

A Frame is a container that can also contain other widgets. It is usually invisible and is used just to arrange the widgets as desired. docstore.mik.ua/orelly/perl3/tk/ch01_03.htm

Creating a widget isn't the same as displaying it in Perl/Tk. You need to use two separate commands to create a widget and display it, although sometimes they are combined into the same line and look like a single command. In the examples so far, we've used the Button method to create the Button, but nothing is displayed by using that method alone. Instead you have to use a geometry manager to cause the widget to be displayed in its parent widget or in another widget. The most commonly used geometry manager is pack. docstore.mik.ua/orelly/perl3/tk/ch01_03.htm

perl -MTk -e 'MainWindow->new->Label(-text => "Hello, Perl/Tk")->pack; MainLoop'

In Perl/Tk, the event loop is initiated by calling a routine called MainLoop. Anything prior to this statement is just setting up the interface. Any code after this call will not execute until after the GUI has exited using $mw->destroy docstore.mik.ua/orelly/perl3/tk/ch01_03.htm

Finally, the last item of concern is the MainLoop command. This starts the event loop in motion, and from then on the application will do only what we have told it to do: if the user clicks on the Button, the application will exit. Anything else the user does—minimizing, resizing, changing to other applications—will be processed by the window manager and ignored by our application. docstore.mik.ua/orelly/perl3/tk/ch01_04.htm

A GUI often makes the application look much more polished and purposeful than a command-line interface does, but it's easy to go overboard with a GUI and end up with something ugly, clunky, and impossible to navigate. So here are some things to consider when deciding how the GUI should look: 
Every widget should have a purpose that is intuitive and informative. 
Think about the way a user will use an application and design accordingly. 
Don't try to cram everything your application does into one window. 
Don't always try to separate everything into different windows. Sometimes the application is so simple that one window is all you need. 
Colors are great, but there are a lot of color-blind people out there. The same applies to fonts: many folks cannot read very small fonts. If you insist on using color and particular fonts, allow them to be customized via the resource database, through a file, or through the application itself. 
Some widgets do their jobs better than others. Use the proper widget for the job. docstore.mik.ua/orelly/perl3/tk/ch01_05.htm

To display widgets on the screen, they must be passed to a geometry manager. The geometry manager controls the position and size of the widgets in the display window. Several geometry managers are available with Perl/Tk: pack, place, grid, and form. All the geometry managers are invoked as methods on the widget, but they all have their own methodologies and arguments to change where and how the widgets are put on the screen docstore.mik.ua/orelly/perl3/tk/ch02_01.htm

When you organize the widgets in your window, it is often necessary to separate groups of widgets to get a certain look and feel. For instance, when you use pack, it is difficult to have widgets stacked both horizontally and vertically without grouping them in some fashion. We use a Frame widget or another window (a Toplevel widget) to group widgets inside a window. docstore.mik.ua/orelly/perl3/tk/ch02_01.htm

The order in which you pack your widgets is very important because it directly affects what you see on the screen. Each Frame or Toplevel maintains a list of items that are displayed within it. This list has an order to it: if widget A is packed before widget B, then widget A will get preference if space becomes scarce. docstore.mik.ua/orelly/perl3/tk/ch02_01.htm

Using pack allows you to control the:

- Position in the window relative to the window or Frame edges
- Size of widgets, relative to other widgets or absolute Spacing between widgets 
- Position in the window's or Frame's widget list


2.1.1. Options for pack 

This list shows all the options available when you call pack (the default values are shown in bold):
- -side => 'left' | 'right' | 'top' | 'bottom Puts the widget against the specified side of the window or Frame
- -fill => 'none' | 'x' | 'y'| 'both' Causes the widget to fill the allocation rectangle in the specified direction
- -expand => 1 | 0 Causes the allocation rectangle to fill the remaining space available in the window or Frame
- -anchor => 'n' | 'ne' | 'e' | 'se' | 's' | 'sw' | 'w' | 'nw' | 'center' Anchors the widget inside the allocation rectangle
- -after => $otherwidget Puts $widget after $otherwidget in packing order
- -before => $otherwidget Puts $widget before $otherwidget in packing order
- -in => $otherwindow Packs $widget inside of $otherwindow rather than the parent of $widget, which is the default
- -ipadx => amount Increases the size of the widget horizontally by amount
- -ipady => amount Increases the size of the widget vertically by amount
- -padx => amount Places padding on the left and right of the widget
- -pady => amount Places padding on the top and bottom of the widget 

If we create a Button with the text "Done" and one with the text "Done, Finished, That's it," the second Button is going to be much wider than the first. When these two Buttons are placed up against either the right or left side of the window, the second Button has a wider allocation rectangle than the first. If we place those same two Buttons against the top and the bottom, the allocation rectangles are the same height and width, because the window, not the widget, determines the width. After the size of the allocation rectangle is determined, the widget is placed within the allocation rectangle according to other options passed and/or the default values of those options. We will go over those options and how they can affect the allocation rectangle later. Once the first widget has been placed in the window, the amount of area available for subsequent allocation rectangles is smaller, because the first allocation rectangle has used some of the space.

Filling the Allocation Rectangle Normally, the widget is left at the default size, which is usually smaller than the allocation rectangle created for it. If the -fill option is used, the widget will resize itself to fill the allocation rectangle according to the value given. The possible values are: 
-fill => 'none' | 'x' | 'y' | 'both' 
Using the value 'x' will resize the widget in the x direction. Likewise, 'y' will cause the widget to resize in the y direction. Using -fill => 'both' is a good way to see exactly what size and placement was given to the allocation rectangle, because 'both' resizes the widget in both x and y directions. Using our four-Button example again, we'll specify -fill => 'both': 

## Expanding the Allocation Rectangle

 The -expand option manipulates the allocation rectangle and not the widget inside it. The value associated with -expand is a Boolean value

### . Anchoring a Widget in Its Allocation Rectangle 

The -anchor option manipulates the widget inside the allocation rectangle by anchoring it to the place indicated by the value passed in. It uses the points of a compass as references.

The default for -anchor is 'center', which keeps the widget in the center of its allocation rectangle. Unless the -expand option is set to a true value, this won't seem to change much of anything in the window.

Sometimes when -side and -anchor are used together, the results don't seem to be what you would expect at first glance. Always keep in mind that invisible allocation rectangle and how it affects what you see on the screen.

### 

Widget Order in the Window Each window into which widgets are packed keeps track of those widgets in an ordered list. The order of this list is determined by the order in which the widgets were packed; the last item packed is the last item in the list. Using the -after option, you can change the default order by specifying which widget should be placed after your new widget. On the opposite end, if you use the -before option, you can put the new widget before a previously packed widget: -after => $otherwidget -before => $otherwidget

### Padding the Size of the Widget 

The final way to force pack to size the widget is to use the padding options. The first set of padding options affects the widget itself by adding to its default size. Different amounts can be added in the x and y directions, or they can be the same. To specify how much padding should occur in the x direction, use the -ipadx option: -ipadx => amount Specify padding for the y direction like this: -ipady => amount The amount is a number that is a valid screen distance. 

The other kind of padding is inserted between the edge of the widget and the edge of the allocation rectangle and is done with the -padx and -pady options 

To unpack a widget from a window or Frame, use the packForget method: $widget->packForget( ); 

To return a list containing all the pack configuration information about a widget, use packInfo: @list = $widget->packInfo( );

### Disabling and enabling automatic resizing 

Unless you've set a preferred window size via the geometry method explicitly, when you put a widget inside a window, the window (or Frame) will resize itself to accommodate the widget. If you are placing widgets inside your window dynamically while the program is running, the window will appear to bounce from size to size. You can turn this behavior off by using packPropagate on the Frame or Toplevel widget: $widget->packPropagate(0);

## The grid Geometry Manager 

The grid geometry manager divides the window into a grid composed of columns and rows starting at (0, 0) in the upper-left corner.

For greater control, you can specify explicit -row and -column options for each widget in the window. We'll cover these options later. 
When additional options are not specified, the following assumptions are made: 

- The first widget in the row (e.g., $widget1 in the preceding example) invokes the grid command. 
- All remaining widgets for that row will be specified as arguments to the grid command. 
- Each additional call to grid will add another row to the display. 
- Special characters can be used to change the -columnspan and -rowspan of the widget without using -columnspan or -rowspan explicitly.

### Grid options

- -column => n Sets the column to place the widget in (n >= 0).
- -row => m Sets the row to place the widget in (m >= 0).
- -columnspan => n Sets the number of columns for the widget to span beginning with -column
- -rowspan => m Sets the number of rows for the widget to span beginning with -row.
- -sticky => string Sticks the widget to string sides. String contains characters n, s, e, or w.
- -in => $otherwindow Indicates the widget is gridded inside $otherwindow instead the parent of $widget.
- -ipadx => amount $widget becomes larger in x direction by amount.
- -ipady => amount $widget becomes larger in y direction by amount.
- -padx => amount Places buffer space equal to amount to the left and right of the widget.
- -pady => amount Places buffer space equal to amount on the top and bottom of the widget.

### Specifying Rows and Columns Explicitly

Rather than letting grid make assumptions, it is sometimes necessary to explicitly state the row and column in which the widget should be placed. This is done by using the -row and -column options. Each option takes a nonnegative integer as an argument: -column => n, -row => m 
When you use -row and -column, it is not necessary to build or grid the widgets in any sort of logical order (except for your own sanity when you are debugging). You could place your first widget in column 10 and row 5 if you like. All the other cells with lower row and column values will remain empty.

### Spanning Rows and Columns Explicitly 

It is also possible to indicate explicitly that a widget (or widgets) should span some columns or rows. The option to span columns is -columnspan. For spanning rows, the option is -rowspan. Both options take an integer that is 1 or greater. The value indicates how many rows or columns should be spanned, including the row or column in which the widget is placed. For this example, we use the easy way to place widgets in columns and rows by not explicitly specifying the -row and -column options. Note that the second grid command applies to two Button widgets, so the single -columnspan option applies to both Buttons created there.

### Forcing a Widget to Fill a Cell 

When you use the pack command, it is necessary to indicate both -fill and -expand options to get the widget to resize inside its allocation rectangle. The grid command doesn't have an allocation rectangle to fill, but it does have the cell within the grid. Using the -sticky option with grid is similar to using -fill and -expand with pack. The value associated with -sticky is a string containing the compass points to which the widget should "stick." If the widget should always "stick" to the top of the cell, you would use -sticky => "n". To force the widget to fill the cell completely, use -sticky => "nsew". To make the widget as tall as the cell but only as wide as it needs to be, use -sticky => "ns". The string value can contain commas and whitespace, but they will be ignored. These two statements are equivalent: -sticky => "nsew" -sticky => "n, s, e, w" # Same thing If you use -sticky with your widgets and then resize the window, you'll notice that the widgets don't resize as you would expect. This is because resizing of the cells and the widgets in them is taken care of with the gridColumnconfigure and gridRowconfigure methods, which are discussed later in this chapter.

### Padding the Widget 

grid also accepts these four options: -ipadx, -ipady, -padx, and -pady. They work exactly the same as they do in pack, but instead of affecting the size of the allocation rectangle, they affect the size of the cell in which the widget is placed.

### Configuring Columns and Rows 

As with any of the geometry managers, grid has a few methods associated with it. Each method is invoked via a widget that has been placed on the screen by using grid. Sometimes it is necessary to change the options of the group of cells that makes up your grid. You can control resizing and the minimum size of a cell with the gridColumnconfigure and gridRowconfigure methods. Each takes a column or a row number as its first argument and then takes some optional arguments that will change the configuration of that column or row. Both gridColumnconfigure and gridRowconfigure work similarly to the configure method used with widgets; however, the options you can specify with gridColumnconfigure and gridRowconfigure cannot be used with the grid command. The options you can use with gridColumnconfigure and gridRowconfigure are -weight, -minsize, and -pad.

If you send only a row or column number, a list of key/value pairs is returned with the current options and their values for that method: 

```perl
@column_configs = $mw->gridColumnconfigure(0); 
@row_configs = $mw->gridRowconfigure(0); 
```

Depending on your sensibilities, you may want to store the results in a hash: 

```perl
%column_configs = $mw->gridColumnconfigure(0); 
%row_configs = $mw->gridRowconfigure(0); 
```

In this example, we are getting the options and their values for the first column and the first row. The results of using the default values would look like this: 
-minsize 0 -pad 0 -weight 0 -minsize 0 -pad 0 -weight 0 
You can get the value of only one of the options by sending that option as the second argument: 
```perl
print $mw->gridColumnconfigure(0, -weight), "\n"; 
print $mw->gridRowconfigure(0, -weight), "\n";
```

The results would be: 0 0 To change the value of the option, use the option followed immediately by the value you want associated with it. For example: 

```perl
$mw->gridColumnconfigure(0, -weight => 1); 
$mw->gridRowconfigure(0, -weight => 1); 
```

You can also specify multiple options in one call: 

```
$mw->gridColumnconfigure(0, -weight => 1, -pad => 10); 
$mw->gridRowconfigure(0, -weight => 1, -pad => 10); 
```

Now that we know how to call gridColumnconfigure and gridRowconfigure, we need to know what the three different options do.

### Weight 

The -weight option sets the amount of space allocated to the column or row when the window is divided into cells. Remember to use -sticky => "nsew" in your grid command if you want the widget to resize when the cell does. The default -weight is 0, which causes the column width or row height to be dictated by the largest widget in the column. Each -weight value has a relationship to the other -weight s in the rows or columns. If a column or row has a -weight of 2, it is twice as big as a column or row that has a -weight of 1. Columns or rows of -weight 0 don't get resized at all. If you want all your widgets to resize in proportion to the size of the window, add this to your code before you call MainLoop: 

```perl
($columns, $rows) = $mw->gridSize( ); 
for ($i = 0; $i < $columns; $i++) {
    $mw->gridColumnconfigure($i, -weight => 1);
}
for ($i = 0; $i < $rows; $i++) { 
    $mw->gridRowconfigure($i, -weight => 1);
} 
```

This code will assign the -weight of 1 to every single row and column in the grid, no matter what size the grid is. Of course, this example works only if you want to assign the same size to each row and each column, but you get the idea. 

### Minimum cell size 

The option -minsize sets the smallest width for the column or the smallest height for each row. The -minsize option takes a valid screen distance as a value. In this example, the minimum size of the cells in row 0 and column 0 is set to 10 pixels: $mw->gridColumnconfigure(0, -minsize => 10); $mw->gridRowconfigure(0, -minsize => 10); If the column or row was normally less than 10 pixels wide, it would be forced to be at least that large. 2.2.8.3. Padding You can add padding around the widget and to the widget by using the -padx/y and -ipadx/y options. You can also add a similar type of padding by using the -pad option with the gridColumnconfigure and gridRowconfigure methods. This padding is added around the widget, not to the widget itself. When you call gridColumnconfigure, the -pad option will add padding to the left and right of the widget. Calling gridRowconfigure with -pad will add padding to the top and bottom of the widget. Here are two examples:

```perl
$mw->gridColumnconfigure(0, -pad => 10); 
$mw->gridRowconfigure(0, -pad => 10); 
```

### Bounding box 

To find out how large a cell is, you can use the gridBbox method: 

```perl
($xoffset, $yoffset, $width, $height) = $master->gridBbox(0, 2); 
```

This example gets the bounding box for column 0 and row 2. All the values returned are in pixels. The bounding box will change as you resize the window. The four values returned represent the x offset, the y offset, the cell width, and the cell height (offsets are relative to the window or Frame where the widget is gridded). The bounding box dimensions include any and all padding specified by the -padx, -pady, -ipadx, and -ipady options.

### Removing a Widget

Like packForget, gridForget removes widgets from view on the screen. This may or may not cause the window to resize itself; it depends on the size of $widget and where it was on the window. Here are some examples:

```perl
$mw->gridForget( ); # Nothing happens 
$widget->gridForget( ); # $widget goes away 
$widget->gridForget($widget1); # $widget and $widget1 go away 
$widget->gridForget($w1, $w3); # $widget, $w1, $w3 go away 
```

The widgets are undrawn from the screen, but the cells remain logically filled.

### Getting Information 
The gridInfo method returns information about the $widget in a list format. Just as with packInfo, the first two elements indicate where the widget was placed: 

```perl 
@list = $widget->gridInfo( ); # Easier to print 
%gridInfo = $widget->gridInfo( );
```

Here are some sample results from gridInfo: 

-in Tk::Frame=HASH(0x81abc44) -column 0 -row 0 -columnspan 1 -rowspan 2 -ipadx 0 -ipady 0 -padx 0 -pady 0 -sticky nesw 

### Widget Location 

The gridLocation method returns the column and row of the widget nearest the given (x, y) coordinates, relative to the master: 

```perl
($column, $row) = $master->gridLocation($x, $y); 
```

Both $x and $y are in screen units relative to the master window (in our examples, $mw). For locations above or to the left of the grid, -1 is returned. When given the arguments (0, 0), our application returns this: 0 0 This indicates that the cell is at column 0 and row 0. 

### Propagation 

There is a gridPropagate method that is similar to packPropagate: 

```perl
$master->gridPropagate( 0 ); 
```

When given a false value, gridPropagate turns off geometry propagation, meaning size information is not sent upward to the parent of $master. By default, propagation is turned on. If gridPropagate is not given an argument, the current value is returned. 

### How Many Columns and Rows? 

To find out how large the grid has become after placing numerous widgets in it, you can use gridSize on the container widget to get back the number of columns and the number of rows: 

```perl
($columns, $rows) = $master->gridSize( ); 
```

The list returned contains the number of columns followed by the number of rows. In many of the earlier examples, we had a grid size that was four columns by two rows. 

```perl
($c, $r) = $f->gridSize( ); #$c = 4, $r = 2 
```

It is not necessary for a widget to be placed in a column/row for it to be considered a valid column/row. If you place a widget in column 4 and row 5 by using -row=>5, -column=>4 and the only other widget is in row 0 and column 0, then gridSize will return 5 and 6. 

### gridSlaves 

There are two ways to find out which widgets have been put in a window or Frame:  use gridSlaves without any arguments to get the full list, or specify a row and column. Here are examples of both:
 
```perl
@slaves = $mw->gridSlaves( ); 
print "@slaves\n"; 
```

The preceding code might have printed this: Tk::Button=HASH(0x81b6fb8) Tk::Button=HASH(0x81ba454) Tk::Button=HASH(0x81ba4cc) Tk:: Button=HASH(0x81ba538) Tk::Button=HASH(0x81b6fa0) Tk::Button=HASH(0x81ba5e0) Tk:: Button=HASH(0x81ba6dc) Tk::Button=HASH(0x81ba748) We could have specified the widget in column 0, row 0: 

```perl
$widget = $mw->gridSlaves( -row => 0, -column => 0 ); 
print "$widget\n"; # Might print this: Tk::Button=HASH(0x81b6fb8)
```

If you specify only the -row option, you'll get a list containing only the widgets in that row. The same goes for specifying only -column; your list will contain only the widgets in that column.