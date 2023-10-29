from tkinter import Canvas


def rounded_rectangle(size, radius, fill):
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius, fill)
    return img


poly = """
# poly.tcl

proc poly_round {win outline fill args} {
    if {[llength $args] % 3 != 0 || [llength $args] < 9} {
        error "wrong # args: should be \"poly_round\
                win outline fill x1 y1 d1 x2 y2 d2 x3 y3 d3 ?...?\""
    }

    # Determine the tag to use.
    if {![info exists ::poly_next_id]} {
        set ::poly_next_id 1
    }
    set tag poly#$::poly_next_id
    incr ::poly_next_id

    # Filter out illegal circles and collinear points.
    set pts [list]
    lassign [lrange $args 0 4] Ux Uy d Vx Vy
    foreach {d Wx Wy} [concat [lrange $args 5 end] [lrange $args 0 4]] {
        set test [expr {$Ux * ($Vy - $Wy) - $Vx * ($Uy - $Wy) +
                $Wx * ($Uy - $Vy)}]
        if {($d > 0) && $test != 0} {
            lappend pts $Vx $Vy $d $test
            lassign [list $Wx $Wy $Vx $Vy] Vx Vy Ux Uy
        } else {
            lassign [list $Wx $Wy] Vx Vy
        }
    }

    # V    C    T   W
    #  *---*----*-+-*-- Given: U, V, W, d
    #  |\ /    /|_|     Find:  S, E, T
    #  | *B   / |
    #  |/ \  /  |       The length of ES and ET each is d.
    # A*   \/   |
    #  |   /\   |       VB bisects angle UVW.  SE _|_ VU; TE _|_ VW.
    #  |  /  \  |       B is halfway between A and C.
    #  | /    \ |       Angles UVW and SET are not necessarily right.
    #  |/      \|       The length of AV and CV each is 1.
    # S*-+------*E
    #  |_|       \      The new polygon is along USTW.
    # U*          \     The new arc has center E, radius d, and angle SET, and
    #  |           \    it is tangential to VU at S and VW at T.

    # Calculate new polygon vertices and create arcs.
    set coords [list]
    lassign [lrange $pts 0 5] Ux Uy d test Vx Vy
    foreach {d test Wx Wy} [concat [lrange $pts 6 end] [lrange $pts 0 5]] {
        # Find A and C.
        foreach {pt x y} [list A $Ux $Uy C $Wx $Wy] {
            set      k [expr {sqrt(($Vx - $x) ** 2 + ($Vy - $y) ** 2)}]
            set ${pt}x [expr {($x - $Vx) / $k + $Vx}]
            set ${pt}y [expr {($y - $Vy) / $k + $Vy}]
        }

        # Find B.
        set Bx [expr {($Ax + $Cx) / 2.0}]
        set By [expr {($Ay + $Cy) / 2.0}]

        # Find the parameters for lines VB and VW.
        foreach {pt x y} [list B $Bx $By W $Wx $Wy] {
            set       k [expr {sqrt(($Vx - $x) ** 2 + ($Vy - $y) ** 2)}]
            set V${pt}a [expr {+($Vy - $y) / $k}]
            set V${pt}b [expr {-($Vx - $x) / $k}]
            set V${pt}c [expr {($Vx * $y - $Vy * $x) / $k}]
        }

        # Find point E.
        set sign [expr {$test < 0 ? -1 : +1}]
        set  k [expr {$VWa * $VBb - $VWb * $VBa}]
        set Ex [expr {(+$VWb * $VBc - ($VWc - $d * $sign) * $VBb) / $k}]
        set Ey [expr {(-$VWa * $VBc + ($VWc - $d * $sign) * $VBa) / $k}]

        # Find tangent points S and T.
        foreach {pt x y} [list S $Ux $Uy T $Wx $Wy] {
            set      k [expr {($Vx - $x) ** 2 + ($Vy - $y) ** 2}]
            set ${pt}x [expr {($Ex * ($Vx - $x) ** 2 + ($Vy - $y) *
                              ($Ey * ($Vx - $x) - $Vx * $y + $Vy * $x)) / $k}]
            set ${pt}y [expr {($Ex * ($Vx - $x) * ($Vy - $y) +
                              ($Ey * ($Vy - $y) ** 2 + ($Vx - $x) *
                              ($Vx * $y - $Vy * $x))) / $k}]
        }

        # Find directions for lines ES and ET.
        foreach {pt x y} [list S $Sx $Sy T $Tx $Ty] {
            set E${pt}d [expr {atan2($Ey - $y, $x - $Ex)}]
        }

        # Find start and extent directions.
        if {$ESd < 0 && $ETd > 0} {
            set start  [expr {180 / acos(-1) * $ETd}]
            set extent [expr {180 / acos(-1) * ($ESd - $ETd)}]
            if {$sign > 0} {
                set extent [expr {$extent + 360}]
            }
        } else {
            set start  [expr {180 / acos(-1) * $ESd}]
            set extent [expr {180 / acos(-1) * ($ETd - $ESd)}]
            if {$sign < 0 && $ESd > 0 && $ETd < 0} {
                set extent [expr {$extent + 360}]
            }
        }

        # Draw arc.
        set opts [list                             \
                [expr {$Ex - $d}] [expr {$Ey - $d}]\
                [expr {$Ex + $d}] [expr {$Ey + $d}]\
                -start $start -extent $extent]
        $win create arc {*}$opts -style pie -tags [list $tag pie]
        $win create arc {*}$opts -style arc -tags [list $tag arc]

        # Draw border line.
        if {[info exists prevx]} {
            $win create line $prevx $prevy $Sx $Sy -tags [list $tag line]
        } else {
            lassign [list $Sx $Sy] firstx firsty
        }
        lassign [list $Tx $Ty] prevx prevy

        # Remember coordinates for polygon.
        lappend coords $Sx $Sy $Tx $Ty

        # Rotate vertices.
        lassign [list $Wx $Wy $Vx $Vy] Vx Vy Ux Uy
    }

    # Draw final border line.
    $win create line $prevx $prevy $firstx $firsty -tags [list $tag line]

    # Draw fill polygon.
    $win create polygon {*}$coords -tags [list $tag poly]

    # Configure colors.
    $win itemconfigure $tag&&(poly||pie) -fill $fill
    $win itemconfigure $tag&&pie         -outline ""
    $win itemconfigure $tag&&line        -fill $outline -capstyle round
    $win itemconfigure $tag&&arc         -outline $outline

    # Set proper stacking order.
    $win raise $tag&&poly
    $win raise $tag&&pie
    $win raise $tag&&(line||arc)

    return $tag
}
       """

poly2 = """
 #----------------------------------------------------------------------
 #
 # RoundPoly -- Draw a polygon with rounded corners in the canvas, based
 # off of ideas and code from "Drawing rounded rectangles"
 #
 # Parameters:
 #       w - Path name of the canvas
 #       xy - list of coordinates of the vertices of the polygon
 #       radii - list of radius of the bend each each vertex
 #       args - Other args suitable to a 'polygon' item on the canvas
 #
 # Results:
 #       Returns the canvas item number of the rounded polygon.
 #
 # Side effects:
 #       Creates a rounded polygon in the canvas.
 #
 #----------------------------------------------------------------------
 
 proc RoundPoly {w xy radii args} {
    set lenXY [llength $xy]
    set lenR [llength $radii]
    if {$lenXY != 2 * $lenR} {
        error "wrong number of vertices and radii"
    }
 
    # Walk down vertices keeping previous, current and next
    lassign [lrange $xy end-1 end] x0 y0
    lassign $xy x1 y1
    eval lappend xy [lrange $xy 0 1]
    set knots {}                                ;# These are the control points
 
    for {set i 0} {$i < $lenXY} {incr i 2} {
        set radius [lindex $radii [expr {$i/2}]]
        set r [winfo pixels $w $radius]
 
        lassign [lrange $xy [expr {$i + 2}] [expr {$i + 3}]] x2 y2
        set z [_RoundPoly2 $x0 $y0 $x1 $y1 $x2 $y2 $r]
        eval lappend knots $z
 
        lassign [list $x1 $y1] x0 y0           ;# Current becomes previous
        lassign [list $x2 $y2] x1 y1           ;# Next becomes current
    }
    set n [eval $w create polygon $knots -smooth 1 $args]
    return $n
 }
 proc _RoundPoly2 {x0 y0 x1 y1 x2 y2 radius} {
    set d [expr { 2 * $radius }]
    set maxr 0.75
 
    set v1x [expr {$x0 - $x1}]
    set v1y [expr {$y0 - $y1}]
    set v2x [expr {$x2 - $x1}]
    set v2y [expr {$y2 - $y1}]
 
    set vlen1 [expr {sqrt($v1x*$v1x + $v1y*$v1y)}]
    set vlen2 [expr {sqrt($v2x*$v2x + $v2y*$v2y)}]
    if {$d > $maxr * $vlen1} {
        set d [expr {$maxr * $vlen1}]
    }
    if {$d > $maxr * $vlen2} {
        set d [expr {$maxr * $vlen2}]
    }
 
    lappend xy [expr {$x1 + $d * $v1x/$vlen1}] [expr {$y1 + $d * $v1y/$vlen1}]
    lappend xy $x1 $y1
    lappend xy [expr {$x1 + $d * $v2x/$vlen2}] [expr {$y1 + $d * $v2y/$vlen2}]
 
    return $xy
 }

"""

ARC = "arc"
CENTRAL = "central"
VERTICAL = "vertical"
HORIZONTAL = "horizontal"
CIRCULAR = "circular"


class AdwDrawEngine(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def win32_high_dpi(self):
        """
        windows平台高DPI启用
        """
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(2)

    def rgb_to_num(self, rgb):
        return int(rgb[1:3], 16), int(rgb[3:5], 16), int(rgb[5:], 16)

    def num_to_rgb(self, hexs: tuple):
        co = '#'
        for i in hexs:
            co += str(hex(i))[2:]
        return co

    def get_color_change(self, color1, color2, num=26):
        colors = []
        a1, a2, a3 = self.rgb_to_num(color1)
        b1, b2, b3 = self.rgb_to_num(color2)
        r, g, b = (b1 - a1), (b2 - a2), (b3 - a3)
        for i in range(num):
            t = i / num-1
            rgb = (int(a1 + r * t), int(a2 + g * t), int(a3 + b * t))
            colors.append(self.num_to_rgb(rgb))
        return colors

    def gradient_init(self):
        """
        初始化渐变引擎
        """
        self.tk.eval("""
        # Create color gradients of various shapes and sizes on a canvas.
#   Usage:
#       gradient draw    <canvas> <tags> <x> <y> <width> <height> <vertical|horizontal|circular|central|arc> <color1> <color2>  ?-animate? ?option? ...
#       gradient redraw  <canvas> <tags> <x> <y> <width> <height> <vertical|horizontal|circular|central|arc> <color1> <color2>  ?-animate? ?option? ...
#       gradient resize  <canvas> <tags> <x> <y> <width> <height>
#       gradient recolor <canvas> <tags> <color1> <color2>

namespace eval gradient {
    namespace ensemble create -subcommands {
        draw
        redraw
        recolor
        resize
        demo
    }

    # Create a gradient on a canvas. The gradient will be placed at the top of the display list.
    proc draw {canvas tags x y width height orient color1 color2 args} {
        # Ensure valid colors are provided while also converting to lists of 16-bit RGB values.
        if { [catch {winfo rgb . $color1} rgb1] } {
            error "invalid color: $color1"
        }
        if { [catch {winfo rgb . $color2} rgb2] } {
            error "invalid color: $color2"
        }
        
        # Delete the gradient if it already exists.
        $canvas delete [join $tags &&]
        
        # Create a hidden canvas item to store meta data about this gradient.
        set meta_data [list x $x  y $y  width $width  height $height  orient $orient  color1 $color1  color2 $color2  args $args]
        $canvas create line $x $y $x $y  -state hidden  -tags [list {*}$tags meta [list gradient: {*}$meta_data]]
        
        # Intercept the -animate option.
        if { "-animate" in $args} {
            set index [lsearch $args "-animate"]
            set args  [lreplace $args $index $index]
            set animate 1
        } else {
            set animate 0
        }
        
        # Draw the gradient.
        if { $orient eq "central" } {
            # Create the canvas rectangle items.
            foreach {x1 y1 x2 y2 color} [get_rects $x $y $width $height $rgb1 $rgb2] {
                $canvas create rectangle $x1 $y1 $x2 $y2  -outline $color  -width 2  -tags $tags  {*}$args
                if {$animate} {update}
            }
        } elseif { $orient eq "circular" } {
            # Create the canvas oval items.
            foreach {x1 y1 x2 y2 color} [get_rects $x $y $width $height $rgb1 $rgb2] {
                $canvas create oval $x1 $y1 $x2 $y2  -outline $color  -width 2  -tags $tags  {*}$args
                if {$animate} {update}
            }
        } elseif { $orient eq "arc" } {
            # Create the canvas arc items.
            foreach {x1 y1 x2 y2 color} [get_rects $x $y $width $height $rgb1 $rgb2] {
                $canvas create arc $x1 $y1 $x2 $y2  -outline $color  -width 2  -tags $tags  -style arc  {*}$args
                if {$animate} {update}
            }
        } elseif { $orient in [list "vertical" "horizontal"] } {        
            # Create the canvas line items.
            foreach {x1 y1 x2 y2 color} [get_lines $x $y $width $height $orient $rgb1 $rgb2] {
                $canvas create line $x1 $y1 $x2 $y2  -fill $color  -tags $tags  -capstyle projecting  {*}$args
                if {$animate} {update}
            }
        } else {
            # Delete the meta data and throw an error.
            $canvas delete [join $tags &&]
            error "invalid orientation: $orient; must be: vertical, horizontal, circular, central, or arc"
        }
        
        return
    }
    
    # Same as draw, but if the gradient already exists then it will retain its position in the canvas's display list after being redrawn.
    proc redraw {canvas tags x y width height orient color1 color2 args} {
        # If the gradient already exists, remember its location in the display list.
        set item_above [$canvas find above [join $tags &&]]
        
        # Draw the gradient.
        draw $canvas $tags $x $y $width $height $orient $color1 $color2 {*}$args
        
        # Move the gradient to its previous location in the display list, if any.
        if { $item_above ne "" } {
            $canvas lower [join $tags &&] $item_above
        }
        
        return
    }
    
    # Shortcut procedure to change the colors of the gradient. Same as redraw but introspectively determines some meta data. 
    # This will use the gradient's x/y location when it was last drawn.
    proc recolor {canvas tags color1 color2} {
        # Retrieve the gradient's meta data.
        set meta [get_meta_data $canvas $tags]
        set meta [dict remove $meta color1 color2]
        dict with meta {}
        
        # Redraw the gradient with the new colors.
        redraw $canvas $tags $x $y $width $height $orient $color1 $color2 {*}$args
        return     
    }
    
    # Shortcut procedure to resize and reposition a gradient. Same as redraw but introspectively determines some meta data. 
    proc resize {canvas tags x y width height} {
        # Retrieve the gradient's meta data.
        set meta [get_meta_data $canvas $tags]
        set meta [dict remove $meta x y width height]
        dict with meta {}
        
        # Recreate the canvas lines with the new dimensions.
        redraw $canvas $tags $x $y $width $height $orient $color1 $color2 {*}$args
        return
    }
    
    # Retrieve meta information on a gradient.
    proc get_meta_data {canvas tags} {
        if { [string is integer -strict $tags] } {
            # This is supposedly a canvas item ID instead of a list of tags describing a gradient. Avoid introducing subtle logic errors.
            error "cannot provide canvas item ID in lieu of gradient tags: $tags"
        }
        # This is a list of tags for a gradient. Find the hidden meta item for this gradient.
        set all_tags [$canvas gettags "meta&&[join $tags &&]"]
        set meta_data [lrange [lsearch -inline -index 0 $all_tags "gradient:"] 1 end]
        if { [llength $meta_data] == 0 } {
            error "cannot find meta data for gradient with tags: $tags"
        }
        return $meta_data
    }
    
    # For a canvas item ID, return all tags that are not gradient meta tags.
    proc get_non_meta_tags {canvas id} {
        set tags [$canvas gettags $id]
        set index [lsearch $tags "meta"]
        set tags [lreplace $tags $index $index]
        set index [lsearch -index 0 $tags "gradient:"]
        set tags [lreplace $tags $index $index]
        return $tags
    }

    # Calculate a list of center-to-outward colored rectangles suitable for [canvas create rectangle] or [canvas create oval].
    proc get_rects {x y width height rgb1 rgb2} {
        set rects [list]
        set x1 [expr {int($x)+1}]
        set y1 [expr {int($y)+1}]
        set x2 [expr {$x1+$width-1}]
        set y2 [expr {$y1+$height-1}]
        
        # Calculate each rectangle.
        if { $width > $height } {
            # Decrement X by one pixel in both directions. Decrement Y by a fraction in both directions.
            # The Y axis will be more heavily concentrated.
            set ratio  [expr { 1.0*$height/$width }]
            set length [expr { $width/2 }]
            while { $x2 > $x1 } {
                lappend rects $x1 $y1 $x2 $y2 [get_color $rgb1 $rgb2 $length [expr { ($x2-$x1)/2 }]]
                set x1 [expr { $x1+1 }]
                set x2 [expr { $x2-1 }]
                set y1 [expr { $y1+$ratio }]
                set y2 [expr { $y2-$ratio }]
            }
        } else {
            # Decrement Y by one pixel in both directions. Decrement X by a fraction in both directions.
            # The X axis will be more heavily concentrated (unless width==height).
            set ratio  [expr { 1.0*$width/$height }]
            set length [expr { $height/2 }]
            while { $y2 > $y1 } {
                lappend rects $x1 $y1 $x2 $y2 [get_color $rgb1 $rgb2 $length [expr { ($y2-$y1)/2 }]]
                set x1 [expr { $x1+$ratio }]
                set x2 [expr { $x2-$ratio }]
                set y1 [expr { $y1+1 }]
                set y2 [expr { $y2-1 }]
            }
        }
        return $rects
    }

    # Calculate a list of left-to-right or top-to-bottom colored lines suitable for [canvas create line].
    proc get_lines {x1 y1 width height orient rgb1 rgb2} {
        set lines [list]
        set x1 [expr {int($x1)}]
        set y1 [expr {int($y1)}]
        set x2 [expr {$x1+$width}]
        set y2 [expr {$y1+$height}]
        if { $orient eq "vertical" } {
            # Calculate the color for each horizontal line.
            for {set y $y1} {$y < $y2} {incr y} {
                lappend lines $x1 $y $x2 $y [get_color $rgb1 $rgb2 $height [expr {$y-$y1}]]
            }
        } elseif { $orient eq "horizontal" } {
            # Calculate the color for each vertical column.
            for {set x $x1} {$x < $x2} {incr x} {
                lappend lines $x $y1 $x $y2 [get_color $rgb1 $rgb2 $width [expr {$x-$x1}]]
            }
        } else {
            error "invalid orientation: $orient; must be: vertical or horizontal"
        }
        
        return $lines
    }

    # Calculates the color at the specified index between rgb1 and rgb2 where rgb1 and rgb2 are the specified length apart.
    proc get_color {rgb1 rgb2 length index} {
        # Throw an error if the index is out of bounds.
        if { $index < 0  ||  $index >= $length } {
            error "index $index is out of bounds for length $length"
        }
        
        lassign $rgb1 r1 g1 b1
        lassign $rgb2 r2 g2 b2
        
        # Determine the ratio between each starting component color and ending component color.
        set r_ratio [expr { 1.00*($r2-$r1+1)/$length }]
        set g_ratio [expr { 1.00*($g2-$g1+1)/$length }]
        set b_ratio [expr { 1.00*($b2-$b1+1)/$length }]

        # Calculate the new component colors at the given index. 
        set r [expr { int($r_ratio*$index+$r1) }]
        set g [expr { int($g_ratio*$index+$g1) }]
        set b [expr { int($b_ratio*$index+$b1) }]

        # A hacky workaround to make up for a lack of precision (or faulty math?).
        # The final pixel of the gradient should exactly match the color of rgb2
        if { $index == [expr {$length-1}] } {
            lassign $rgb2 r g b
        }

        # Convert the integer RGB values to a hex color.
        return [rgb_to_hex [list $r $g $b]]
    }
    
    # Convert a list of 16-bit RGB values to an 8-bit hex color. Using 8-bit hex colors instead of 16-bit
    # speeds up drawing of images two-fold (I haven't benchmarked this for canvases).
    proc rgb_to_hex {rgb} {
        lassign $rgb r g b
        set r [format %02x [expr {$r/256}]]
        set g [format %02x [expr {$g/256}]]
        set b [format %02x [expr {$b/256}]]
        return #$r$g$b
    }
    
    # Converts 8-bit RGB values to 16-bit RGB values.
    proc rgb_8_to_16_bit {rgb} {
        lassign $rgb r g b
        return [list [expr {$r*256}] [expr {$g*256}] [expr {$b*256}]]
    }
    
    # Returns a random 8-bit hex color.
    proc random_color {} {
        return [rgb_to_hex "[expr {int(rand()*65536)}] [expr {int(rand()*65536)}] [expr {int(rand()*65536)}]"]
    }

    # Redraw all gradients with random colors
    proc randomize_all_gradient_colors {canvas} {
        foreach id [$canvas find withtag meta] {
            set tags [get_non_meta_tags $canvas $id]
            recolor $canvas $tags [random_color] [random_color]
        }
      return
    }
    
    # Randomize colors for all canvas items.
    proc randomize_all_canvas_item_colors {canvas} {
        foreach id [$canvas find withtag all] {
            if { [$canvas type $id] in {window} } {
                continue
            }
            $canvas itemconfigure $id -fill [random_color]
            if { [$canvas type $id] in {rectangle arc oval} } {
                 $canvas itemconfigure $id -outline [random_color]
            }
        }
        return
    }
    
    # Run a demonstration.
    proc demo {} {
        # Create a toplevel window with a canvas filling the contents.
        set win .gradients
        if { [winfo exists $win] } {
            destroy $win
        }
        toplevel $win
        set cvs [canvas $win.cvs -highlightthickness 0]
        pack $cvs -fill both -expand yes
        wm geometry $win 800x600
        raise $win

        # Fill the bottom of the screen with a striped green fade.
        gradient draw $cvs footer 0 0 10 10 vertical white darkgreen -dash {3 1}
        bind $cvs <Configure> {
            gradient resize %W footer 0 [expr {%h-300}] %w 300
        }
        
        # Draw a strip of rainbow.
        set width  100
        set colors {white red orange yellow green blue purple violet white}
        for {set i 1} {$i < [llength $colors]} {incr i} {
            set c1 [lindex $colors $i-1]
            set c2 [lindex $colors $i]
            gradient draw $cvs "wave $i" [expr {$width*($i-1)}] 0 $width 50 horizontal $c1 $c2
        }
        
        # Draw some balls with diameters of 100.
        set colors {green red yellow blue orange white}
        for {set i 0} {$i < 6} {incr i} {
            gradient draw $cvs "beachball $i" 0 55 100 100 arc [lindex $colors $i] #333 -start [expr {$i*60}] -extent 60
        }
        set colors {cyan pink orange firebrick}
        for {set i 0} {$i < [llength $colors]} {incr i} {
            gradient draw $cvs "quadball $i" 110 55 100 100 arc [lindex $colors $i] #eee -start [expr {$i*90}] -extent 90
        }
        gradient draw $cvs ball1    220 55 100 100 circular #bbbbbb white
        gradient draw $cvs ball2    330 55 100 100 circular #888 #eee
        gradient draw $cvs ball3    440 55 100 100 circular black grey
        gradient draw $cvs ball4    550 55 100 100 circular black #555
        gradient draw $cvs ball5    660 55 100 100 circular cyan black
        
        # Draw some boxes.
        gradient draw $cvs box1   0 160 150 100 horizontal white firebrick
        gradient draw $cvs box2 150 160 200 100 central    black firebrick
        gradient draw $cvs box3 350 160 100 100 horizontal firebrick black
        gradient draw $cvs box4 450 160 200 100 central    firebrick black
        gradient draw $cvs box5 650 160 150 100 horizontal black white
        
        # Display some control buttons.
        frame $cvs.f
        button $cvs.f.b1 -text "Redraw with random gradient colors" -command [list [namespace current]::randomize_all_gradient_colors $cvs]
        button $cvs.f.b2 -text "Relaunch demo with default colors" -command [list [namespace current]::demo]
        button $cvs.f.b3 -text "Chaos" -command [list [namespace current]::randomize_all_canvas_item_colors $cvs]
        pack $cvs.f.b1 $cvs.f.b2 $cvs.f.b3 -fill x
        $cvs create window 400 400 -window $cvs.f

        return
    }
}
        """)

    def gradient_demo(self):
        """
        启动渐变引擎示例
        """
        self.gradient_init()
        self.tk.call("gradient", "demo")

    def gradient_resize(self, tags: str, x: int, y: int, width: int, height: int):
        """
        修改渐变图形的大小位置
        """
        self.gradient_init()
        self.tk.call("gradient", "resize", self._w, tags, x, y, width, height)

    def gradient_recolor(self, tags: str, x: int, y: int, color1, color2):
        """
        修改渐变组件的颜色
        """
        self.gradient_init()
        self.tk.call("gradient", "color", self._w, tags, color1, color2)

    def gradient_draw(self, tags: str, x: int, y: int, width: int, height: int, orient, color1, color2, *args,
                      **kwargs):
        """
        绘制渐变图形
        """
        self.gradient_init()
        id = self.tk.call("gradient", "draw", self._w, tags, x, y, width, height, orient, color1, color2)
        self.itemconfigure(tags, *args, **kwargs)
        return id

    def gradient_redraw(self, *args, **kwargs):
        """
        同gradient_draw
        """
        self.gradient_draw(*args, **kwargs)

    def create_gradient_v_rectangle(self, x, y, width, height, tags, color1, color2, *args, **kwargs):
        """
        创建水平渐变矩形

        :param x: 图形x位置
        :param y: 图形y位置
        :param width: 图形宽度
        :param height: 图形高度
        :param tags: 标签名
        :param color1: 渐变颜色1
        :param color2: 渐变颜色2
        :return:
        """
        return self.gradient_draw(tags=tags, x=x, y=y, width=width, height=height, color1=color1, color2=color2,
                                  orient=VERTICAL, *args, **kwargs)

    def create_gradient_h_rectangle(self, x, y, width, height, tags, color1, color2, *args, **kwargs):
        """
        创建垂直渐变矩形

        :param x: 图形x位置
        :param y: 图形y位置
        :param width: 图形宽度
        :param height: 图形高度
        :param tags: 标签名
        :param color1: 渐变颜色1
        :param color2: 渐变颜色2
        :return:
        """
        return self.gradient_draw(tags=tags, x=x, y=y, width=width, height=height, color1=color1, color2=color2,
                                  orient=HORIZONTAL, *args, **kwargs)

    def create_gradient_circular(self, x, y, width, height, tags, color1, color2, *args, **kwargs):
        """
        创建垂直渐变圆形

        :param x: 图形x位置
        :param y: 图形y位置
        :param width: 图形宽度
        :param height: 图形高度
        :param tags: 标签名
        :param color1: 渐变颜色1
        :param color2: 渐变颜色2
        :return:
        """
        return self.gradient_draw(tags=tags, x=x, y=y, width=width, height=height, color1=color1, color2=color2,
                                  orient=CIRCULAR, *args, **kwargs)

    def draw_gradient(self, color1, color2, type="x"):
        self.tk.eval("""
  proc + {n1 n2} {
    expr {$n1 + $n2}
  }
  proc - {n1 n2} {
    expr {$n1 - $n2}
  }
  proc * {n1 n2} {
    expr {$n1 * $n2}
  }
  proc / {n1 n2} {
    expr {$n1 / $n2}
  }
  proc toInt {n} {
    expr int($n)
  }
  
  proc drawGradient {win type col1Str col2Str} {
    $win delete gradient
    
    set width [winfo width $win]
    set height [winfo height $win]
    
    lassign [winfo rgb $win $col1Str] r1 g1 b1
    lassign  [winfo rgb $win $col2Str] r2 g2 b2
    set rRange [- $r2.0 $r1]
    set gRange [- $g2.0 $g1]
    set bRange [- $b2.0 $b1]
  
    if {$type == "x"} {
      set rRatio [/ $rRange $width]
      set gRatio [/ $gRange $width]
      set bRatio [/ $bRange $width]
    
      for {set x 0} {$x < $width} {incr x} {
        set nR [toInt [+ $r1 [* $rRatio $x]]]
        set nG [toInt [+ $g1 [* $gRatio $x]]]
        set nB [toInt [+ $b1 [* $bRatio $x]]]
  
        set col [format {%4.4x} $nR]
        append col [format {%4.4x} $nG]
        append col [format {%4.4x} $nB]
        $win create line $x 0 $x $height -tags gradient -fill #${col}
      }
    } else {
      set rRatio [/ $rRange $height]
      set gRatio [/ $gRange $height]
      set bRatio [/ $bRange $height]
  
      for {set y 0} {$y < $height} {incr y} {
        set nR [toInt [+ $r1 [* $rRatio $y]]]
        set nG [toInt [+ $g1 [* $gRatio $y]]]
        set nB [toInt [+ $b1 [* $bRatio $y]]]
  
        set col [format {%4.4x} $nR]
        append col [format {%4.4x} $nG]
        append col [format {%4.4x} $nB]
        $win create line 0 $y $width $y -tags gradient -fill #${col}
      }
    }
    return $win
  }
        """)

        self.tk.call("drawGradient", self._w, type, color1, color2)

    def create_round_rectangle(self, x1, y1, x2, y2, radius: float = 5, width=2, fill="white", outline="black"):
        """
        创建圆角矩形 ： 自绘版
        """
        # 自研
        _radius = radius * 2
        nw = self.create_arc(x1, y1, x1 + _radius, y1 + _radius, start=90, extent=90, width=width, fill=fill,
                             outline=outline)  # ⌜ north | west
        sw = self.create_arc(x1, y2, x1 + _radius, y2 - _radius, start=180, extent=90, width=width, fill=fill,
                             outline=outline)  # ⌞ south | wast
        ne = self.create_arc(x2 - _radius, y1, x2, y1 + _radius, start=0, extent=90, width=width, fill=fill,
                             outline=outline)  # ⌝ north | east
        se = self.create_arc(x2 - _radius, y2, x2, y2 - _radius, start=270, extent=90, width=width, fill=fill,
                             outline=outline)  # ⌟ south | east

        w = self.create_line(x1, y1 + _radius / 2, x1, y2 - _radius / 2, width=width, fill=outline)  # | left
        n = self.create_line(x1 + _radius / 2, y1, x2 - _radius / 2, y1, width=width, fill=outline)  # —— up
        e = self.create_line(x2, y1 + _radius / 2, x2, y2 - _radius / 2, width=width, fill=outline)  # | right
        s = self.create_line(x1 + _radius / 2, y2, x2 - _radius / 2, y2, width=width, fill=outline)  # —— down

        top = self.create_rectangle(x1 + _radius / 2 - width, y1 + width / 2, x2 - _radius / 2 + width,
                                    y1 + _radius / 2, fill=fill,
                                    width=0)  # ▭ top

        center = self.create_rectangle(x1 + width / 2, y1 + _radius / 2 - width, x2 - width / 2,
                                       y2 - _radius / 2 + width, fill=fill,
                                       width=0)  # ▭ center

        bottom = self.create_rectangle(x1 + _radius / 2 - width, y2 - _radius / 2, x2 - _radius / 2 + width,
                                       y2 - width / 2, fill=fill,
                                       width=0)  # ▭ bottom

        return {
            "nw": nw, "sw": sw, "ne": ne, "se": se, "w": w, "n": n, "e": e, "s": s,
            "top": top, "center": center, "bottom": bottom
        }

    create_round_rect = create_round_rectangle

    def create_round_rectangle2(self, x0, y0, x3, y3, radius, *args, **kwargs):
        """
        创建圆角矩形 ： 其他开发者制作 ： 边框有问题（不推荐）
        """
        # wiki上
        self.tk.eval("""
#----------------------------------------------------------------------
#
# roundRect --
#
#       Draw a rounded rectangle in the canvas.
#
# Parameters:
#       w - Path name of the canvas
#       x0, y0 - Co-ordinates of the upper left corner, in pixels
#       x3, y3 - Co-ordinates of the lower right corner, in pixels
#       radius - Radius of the bend at the corners, in any form
#                acceptable to Tk_GetPixels
#       args - Other args suitable to a 'polygon' item on the canvas
#
# Results:
#       Returns the canvas item number of the rounded rectangle.
#
# Side effects:
#       Creates a rounded rectangle as a smooth polygon in the canvas.
#
#----------------------------------------------------------------------

proc roundRect { w x0 y0 x3 y3 radius args } {

set r [winfo pixels $w $radius]
set d [expr { 2 * $r }]

# Make sure that the radius of the curve is less than 3/8
# size of the box!

set maxr 0.75

if { $d > $maxr * ( $x3 - $x0 ) } {
    set d [expr { $maxr * ( $x3 - $x0 ) }]
}
if { $d > $maxr * ( $y3 - $y0 ) } {
    set d [expr { $maxr * ( $y3 - $y0 ) }]
}

set x1 [expr { $x0 + $d }]
set x2 [expr { $x3 - $d }]
set y1 [expr { $y0 + $d }]
set y2 [expr { $y3 - $d }]

set cmd [list $w create polygon]
lappend cmd $x0 $y0
lappend cmd $x1 $y0
lappend cmd $x2 $y0
lappend cmd $x3 $y0
lappend cmd $x3 $y1
lappend cmd $x3 $y2
lappend cmd $x3 $y3
lappend cmd $x2 $y3
lappend cmd $x1 $y3
lappend cmd $x0 $y3
lappend cmd $x0 $y2
lappend cmd $x0 $y1
lappend cmd -smooth 1
return [eval $cmd $args]
}
        """)
        rect = self.tk.call("roundRect", self._w, x0, y0, x3, y3, radius)
        self.itemconfig(rect, *args, **kwargs)
        return rect

    create_round_rect2 = create_round_rectangle2

    def create_round_rectangle3(self, tag, x, y, width, height, radius, fill: str = "black", outline: str = "black",
                                *args, **kwargs):
        """
        创建圆角矩形 ： 其他开发者制作 ： 圆角看起来更舒服
        """
        # wiki上 圆角看起来更舒服
        self.tk.eval("""
proc roundRect2 {w L T Rad width height fill outline tag} {

  $w create oval $L $T [expr $L + $Rad] [expr $T + $Rad] -fill $fill -outline $outline -tag $tag
  $w create oval [expr $width-$Rad] $T $width [expr $T + $Rad] -fill $fill -outline $outline -tag $tag
  $w create oval $L [expr $height-$Rad] [expr $L+$Rad] $height -fill $fill -outline $outline -tag $tag
  $w create oval [expr $width-$Rad] [expr $height-$Rad] [expr $width] $height -fill $fill -outline $outline -tag $tag
  $w create rectangle [expr $L + ($Rad/2.0)] $T [expr $width-($Rad/2.0)] $height -fill $fill -outline $outline -tag $tag
  $w create rectangle $L [expr $T + ($Rad/2.0)] $width [expr $height-($Rad/2.0)] -fill $fill -outline $outline -tag $tag
}
            """)
        _rect = self.tk.call("roundRect2", self._w, x, y, radius, width, height, fill, outline, tag)
        self.itemconfig(_rect, *args, **kwargs)
        return _rect

    create_round_rect3 = create_round_rectangle3

    def create_round_rectangle4(self, x1, y1, x2, y2, radius, **kwargs):
        """
        创建圆角矩形 ： 其他开发者制作
        """
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        _poly = self.create_polygon(points, **kwargs, smooth=True)

        return _poly

    create_round_rect4 = create_round_rectangle4

    def polygon_round(self, win, outline="black", fill="black", *args, **kwargs):
        self.tk.eval(poly)
        _poly = self.tk.eval(f"poly_round {win} {outline} {fill}")
        self.itemconfig(_poly, *args, **kwargs)
        return _poly

    poly_round = polygon_round

    def demo_polygon_round(self):
        demo = """
 package require Tcl 8.5
 package require Tk

 proc draw {win} {
     global demo

     set sharp_pts [list]
     set round_pts [list]
     for {set id 0} {$id < $demo(num_pts)} {incr id} {
         set x [expr {([lindex [$win coords vtx#$id] 0] +
                       [lindex [$win coords vtx#$id] 2]) / 2}]
         set y [expr {([lindex [$win coords vtx#$id] 1] +
                       [lindex [$win coords vtx#$id] 3]) / 2}]
         lappend sharp_pts $x $y
         lappend round_pts $x $y $demo(radius)
     }

     .c delete sharp_poly
     .c create polygon {*}$sharp_pts -outline gray50 -fill ""\
             -dash {6 5} -tags {sharp_poly}

     if {[info exists demo(tag)]} {
         .c delete $demo(tag)
     }
     set demo(tag) [poly_round .c $demo(outline) $demo(fill) {*}$round_pts]
     .c itemconfigure $demo(tag) -width $demo(thickness)

     .c raise vtx
 }

 proc down {win x y} {
     global demo

     $win dtag selected
     $win addtag selected withtag current
     $win raise current
     set demo(last_x) $x
     set demo(last_y) $y
 }
 
 proc move {win x y} {
     global demo

     if {[info exists demo(last_x)]} {
         $win move selected\
                 [expr {$x - $demo(last_x)}]\
                 [expr {$y - $demo(last_y)}]
         set demo(last_x) $x
         set demo(last_y) $y

         draw $win
     }
 }

 proc main {args} {
     global demo

     array set demo {
         num_pts 3       radius 20      thickness 1
         outline black   fill   white   background gray
         width   400     height 400
     }
     foreach {option value} $args {
         set option [regsub {^-} $option ""]
         if {![info exists demo($option)]} {
             puts "Options: -[join [array names demo] " -"]"
             exit
         } else {
             set demo([regsub {^-} $option ""]) $value
         }
     }

     canvas .c -width $demo(width) -height $demo(height) -highlightthickness 0\
             -background $demo(background)
     pack .c
     wm title . "Round Polygon Demo"
     wm resizable . 0 0

     set 2pi [expr {2 * acos(-1)}]
     set cx [expr {$demo(width)  / 2}]; set sx [expr {$demo(width)  * 3 / 8}]
     set cy [expr {$demo(height) / 2}]; set sy [expr {$demo(height) * 3 / 8}]
     for {set id 0} {$id < $demo(num_pts)} {incr id} {
         set x [expr {$cx + $sx * cos(($id + 0.5) * $2pi / $demo(num_pts))}]
         set y [expr {$cy - $sy * sin(($id + 0.5) * $2pi / $demo(num_pts))}]
         .c create oval [expr {$x - 3}] [expr {$y - 3}]\
                        [expr {$x + 3}] [expr {$y + 3}]\
                        -tags [list vtx vtx#$id] -fill brown
     }

     .c bind vtx <Any-Enter> {.c itemconfigure current -fill red}
     .c bind vtx <Any-Leave> {.c itemconfigure current -fill brown}
     .c bind vtx <ButtonPress-1> {down .c %x %y}
     .c bind vtx <ButtonRelease-1> {.c dtag selected}
     bind .c <B1-Motion> {move .c %x %y}

     focus .c
     draw .c
 }

 main

        """

        self.tk.eval(poly)
        self.tk.eval(demo)

    def create_svg_image(self, x, y, content: str, **kwargs):
        from tempfile import mkstemp
        from tksvg import SvgImage

        _, file = mkstemp(suffix=".svg")
        print(file)
        with open(file, "w") as f:
            f.write(content)
            f.close()
        image = SvgImage(file=file)

        i = self.create_image(x, y, image=image, **kwargs)

        return i

    def draw_copy_icon(self, __x, __y, size=10, padding=10, radius=18):
        _1 = self.create_round_rect4(__x, __y, __x + size * 5, __y + size * 5, radius)
        _2 = self.create_round_rect4(__x + padding, __y + padding, __x + size * 5 - padding, __y + size * 5 - padding,
                                     radius / 2, fill="white")
        _3 = self.create_round_rect4(__x + size * 2, __y + size * 2, __x + size * 7, __y + size * 7, radius)
        _4 = self.create_round_rect4(__x + size * 2 + padding, __y + size * 2 + padding, __x + size * 7 - padding,
                                     __y + size * 7 - padding, radius / 2, fill="white")
        return _1, _2, _3, _4

    def create_round_rectangle5(self, __x, __y, __width, __height, fill="black", radius=16, *args, **kwargs):
        from PIL import ImageTk
        img = rounded_rectangle((__width, __height), radius, fill, *args, **kwargs)
        photo = ImageTk.PhotoImage(img)

        return self.create_image(__x, __y, image=photo, anchor='nw')


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    canvas = AdwDrawEngine()

    # canvas.create_round_rect3(10, 15, 15, 150, 150, 50)
    # canvas.gradient_demo()
    # canvas.bind("<Configure>", lambda event: canvas.draw_gradient("#87e9bb", "#d3a6f5", "x"))

    canvas.gradient_demo()
    canvas.pack(fill="both", expand="yes")

    root.mainloop()
