#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'CFigure' ]

#------------------------------------------------------------------
# Import from ...
#  
from pyConics.constants import const
from pyConics.errors import CValueError
from matplotlib import pyplot as plt
from pyConics.plotting.axes import CAxes

#------------------------------------------------------------------
# Import from...
# We use here TYPE_CHECKING constant to avoid circular import  
# exceptions.
#
from typing import TYPE_CHECKING
if TYPE_CHECKING:
   ... # Do nothing here, because there are no pyConics modules
       # here to be imported.    

#------------------------------------------------------------------
# Import as ...
#  
import pyautogui as gui
import matplotlib as mpl
import numpy as np

#------------------------------------------------------------------
# Class CFigure.
#  
class CFigure:
    def __init__( self, size: tuple[ float, float ] = ( 0.0, 0.0 ), unit: str = '' ) -> None:
        self._axes: list[ CAxes ] = []

        w, h = size
        if ( size == ( 0.0, 0.0 ) ):
            self._fig = plt.figure( layout = 'constrained' )
        elif ( unit == 'inche' ):
            if ( w == 0.0 ):
                w = h
            elif ( h == 0.0 ):
                h = w
            self._fig = plt.figure( figsize = ( w, h ), layout = 'constrained' )
        elif ( unit == '' ):
            if ( ( abs( w ) > 1.0 ) or ( abs( h ) > 1.0 ) ):
                raise CValueError( self.__class__.__name__,
                                  'when unit=\'\', size argument must not be greater than 1.' )
            if ( w == 0.0 ):
                w = h
            elif ( h == 0.0 ):
                h = w
            width, height = gui.size()
            dpi = mpl.rcParams[ 'figure.dpi' ]
            w = round( w * ( width / dpi ), 1 )
            h = round( h * ( height / dpi ), 1 )
            self._fig = plt.figure( figsize = ( w, h ), layout = 'constrained' )
        else:
            raise CValueError( self.__class__.__name__,
                              'unit argument must be either an empty string or \'inche\'.' )

    def __repr__( self ) -> str:
        l = len( self._axes )
        return f'{self.__class__.__name__} class with {l} CAxes classes.'

    @staticmethod
    def show( blocking: bool = True ) -> None:
        plt.show( block = blocking )

    def get_pyplot_figure( self ) -> plt.Figure: #type: ignore
        return self._fig

    def get_pyplot_axes( self ) -> list[ plt.Axes ]: #type: ignore
        return self._fig.get_axes()

    @property
    def axes( self ) -> tuple[ CAxes, ... ]:
        return tuple( self._axes )

    @staticmethod
    def ion() -> None:
        plt.ion()
    
    @staticmethod
    def ioff() -> None:
        plt.ioff()
    
    @staticmethod
    def is_interactive() -> bool:
        return plt.isinteractive()

    def create_axes( self, n_axes: tuple[ int, int ] = ( 1, 1 ) ):
        self._fig.subplots( n_axes[ 0 ], n_axes[ 1 ] )

        for ax in self._fig.axes:
            # Set some properties of the axes.
            ax.grid( visible = True, which = 'both', axis = 'both' )
            ax.axis( 'scaled' ) # it works better than 'equal'.
            ax.set_xlim( ( 0.0, 1.0 ) )
            ax.set_ylim( ( 0.0, 1.0 ) )
            ax.set_xticks( np.round( np.linspace( 0, 1, 11 ), 1 ) )
            ax.set_yticks( np.round( np.linspace( 0, 1, 11 ), 1 ) )
            ax.tick_params( axis = 'x', labelsize = const.tickssize )
            ax.tick_params( axis = 'y', labelsize = const.tickssize )
            ax.set_xlabel( 'x-axis', fontsize = const.labelsize )
            ax.set_ylabel( 'y-axis', fontsize = const.labelsize )
            ax.set_title( 'axes title', fontsize = const.titlesize )

            # Create a CAxes class for each axes.
            self._axes.append( CAxes( ax ) )

    def update_canvas( self ) -> None:
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()

    def save( self, fname: str ):
        self._fig.savefig( fname )

#------------------------------------------------------------------
# For development and test.
#  
if ( __name__  == '__main__' ):
    from pyConics import CPoint, CLine

    # Set interative mode.
    # Activate this mode so that it is not necessary to call the show() function.
    CFigure.ion()

    width = 0.35
    f2 = CFigure( (width, 16.0 / 9.0 * width ) )

    # Get the pyPlot's Figure class.
    pp_fig2 = f2.get_pyplot_figure()

    # Create the axes from f2.
    f2.create_axes( ( 2, 2 ) )
    print( f2 )

    # Get a list of CAxes class.
    axes = f2.axes
    # print( axes )
    for ax in axes:
        print( ax )
        # print( ax.get_pyplot_axes() )

    # Change the x- and y-axis limits of axes[ 0 ].
    axes[ 0 ].xlim = ( 0, 2 )
    axes[ 0 ].ylim = ( -1, 1 )

    # Redraw all figure to update its canvas.
    if ( CFigure.is_interactive() ):
        # f2.update_canvas()
        input( 'Press any key to continue...' )

    # Change the x- and y-ticks of axes[ 0 ].
    xtick = np.linspace( 0, 2, 11 )
    ytick = np.linspace( -1, 1, 11 )
    axes[ 0 ].xticks = xtick
    axes[ 0 ].yticks = ytick

    # Redraw all figure to update its canvas.
    if ( CFigure.is_interactive() ):
        # f2.update_canvas()
        input( 'Press any key to continue...' )

    # Plot a point and a line on axes[ 0 ].
    x = 1.0
    y = 0.0
    axes[ 0 ].plot( x, y, 'ob', markersize = 12 )
    x = np.linspace( 0, 2, 11 )
    y = -x + 1
    axes[ 0 ].plot( x, y, 'r-', linewidth = 0.5 )

    # Redraw all figure to update its canvas.
    if ( CFigure.is_interactive() ):
        # f2.update_canvas()
        input( 'Press any key to continue...' )

    # Plot a line on axes[ 3 ].
    x = np.linspace( 0.0, 1.0, 11 )
    y = x
    axes[ 3 ].plot( x, y, 'sr-', linewidth = 2, markersize = 8 )

    # Redraw all figure to update its canvas.
    if ( CFigure.is_interactive() ):
        # f2.update_canvas()
        input( 'Press any key to continue...' )
    
    # Plot a line on axes[ 1 ] using a matrix as parameter.
    x = np.linspace( 0.0, 1.0, 11 )
    x = x[np.newaxis].T # transform an 1D array into a 2D array and get its transpose.
    y = 1.2 * x
    YY = np.block( [ [ x, y ] ] )
    axes[ 1 ].plot( x, YY, 'b-', linewidth = 1 ) # must use x and y parameters.

    # Redraw all figure to update its canvas.
    if ( CFigure.is_interactive() ):
        # f2.update_canvas()
        input( 'Press any key to continue...' )
    
    # Plot CPoint objects on axes[ 2 ].
    p1 = CPoint( ( 0.5, 0.6 ), 'p1' )
    p2 = CPoint( ( 0.5, 0.7 ), 'p2' )
    axes[ 2 ].plot( p1, '^g', p2, 'om', markersize = 6 )

    # Redraw all figure to update its canvas.
    if ( CFigure.is_interactive() ):
        # f2.update_canvas()
        input( 'Press any key to continue...' )

    # Plot CLine object on axes[ 2 ].
    l1 = CLine( ( -4.0, -4.0, 4.0 ), 'l1' )
    # p2 = CPoint( ( 0.5, 0.6 ), 'p2' )
    axes[ 2 ].plot( l1, 'oy-', linewidth = 1, clinesamples = 21, markersize = 4 )

    # Redraw all figure to update its canvas.
    if ( CFigure.is_interactive() ):
        # f2.update_canvas()
        input( 'Press any key to continue...' )

    # Plot a list of CPoint objects on axes[ 2 ].
    p1 = CPoint( ( 0.0, 0.8 ), 'p1' )
    p2 = CPoint( ( 0.2, 0.8 ), 'p2' )
    p3 = CPoint( ( 0.4, 0.8 ), 'p3' )
    p4 = CPoint( ( 0.6, 0.8 ), 'p4' )
    p5 = CPoint( ( 0.8, 0.8 ), 'p5' )
    p6 = CPoint( ( 1.0, 0.8 ), 'p6' )
    plist = [ p1, p2, p3, p4, p5, p6 ]
    axes[ 2 ].plot( plist, 'ob', [ 0.9, 0.9, 0.9 ], [ 0.2, 0.3, 0.4 ], 'or',
                    markersize = 6 )

    # Redraw all figure to update its canvas.
    if ( CFigure.is_interactive() ):
        # f2.update_canvas()
        input( 'Press any key to continue...' )

    # Plot a list of CLine objects.
    l1 = CLine( ( 0.0, 1.0, -0.2 ), 'l1' )
    l2 = CLine( ( 0.0, 1.0, -0.3 ), 'l2' )
    l3 = CLine( ( 0.0, 1.0, -0.9 ), 'l3' )
    l4 = CLine( ( 1.0, 0.0, -0.1 ), 'l4' )
    llist = [ l1, l2, l3, l4 ]
    axes[ 2 ].plot( llist, 'sm-', linewidth = 0.5, markersize = 3, clinesamples = 11 )

    # Redraw all figure to update its canvas.
    if ( CFigure.is_interactive() ):
        # f2.update_canvas()
        input( 'Press any key to continue...' )

    # If the Figure is blocking, then show it.
    if ( not CFigure.is_interactive() ):
        f2.show()
    