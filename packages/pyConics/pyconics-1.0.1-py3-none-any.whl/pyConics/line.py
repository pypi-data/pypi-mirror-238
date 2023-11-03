#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations
from typing import Any

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'CLine' ]

#------------------------------------------------------------------
# Import from...
#
from typing import Any

#------------------------------------------------------------------
# Import from...
# We use here TYPE_CHECKING constant to avoid circular import  
# exceptions.
#
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ... # Do nothing here, because there are no pyConics modules
        # here to be imported.

from pyConics.constants import const
from pyConics.agobj import CAGObj
from pyConics.errors import CLineTypeError
from pyConics.origin import origin
from pyConics.tolerance import tol

#------------------------------------------------------------------
# Import as...
#
import numpy as np
np.set_printoptions( formatter = { 'float': lambda x: "{0:0.4e}".format( x ) } )

#------------------------------------------------------------------
# Class CLine.
#  
class CLine( CAGObj ):
    def __init__( self,
                  line: tuple[ float, float, float ] = ( 1.0, -1.0, 0.0 ),
                  name: str = '',
                  shift_origin: bool = True  ) -> None:
        super().__init__( name )

        # Redim the geometric form.
        self._gform = _validate_line( line )

        # Test for epsilon number condition.
        self._gform = tol.adjust2relzeros( self._gform )

        # Store this value to be possible restore it to the origin.
        self._from_origin = self._gform

        # Translate the origin from ( 0, 0 ) to another origin in '(origin.x, origin.y )'.
        if ( shift_origin == True ):
            self.update_origin()

    def __repr__( self ) -> str:
        # return an info messsage for this class.
        info = f'{self.name}: ( x, y ) | {self.gform} * [ x y 1 ]\' = 0'
        if ( self.gform[ 0 ] == 0.0 ) and ( self.gform[ 1 ] == 0.0 ):
            info += f' -> line at the infinity'
        return info

    def update_origin( self ) -> None:
        # Translate the origin from ( 0, 0 ) to another origin in '(origin.x, origin.y )'.
        self._gform = origin.change_line( self._from_origin )

    def cross( self, other: CPoint | CLine ) -> Any[ CPoint | CLine ]:
        from pyConics.utils import cross

        # Get the cross product.
        return cross( self, other )

    def __mul__( self, other: CPoint | CLine ) -> Any[ CPoint | CLine ]:
        # Get the cross product.
        return self.cross( other )

    def __contains__( self, other: CPoint ) -> bool:
        from pyConics.utils import dot

        # Get the dot function.
        if ( dot( self, other ) == 0.0 ):
            return True
        return False

    def distance( self, other: CPoint | CLine ) -> float:
        from pyConics.utils import distance

        # Get the distance function.
        return distance( self, other )
    
    def are_perpendicular( self, other: CLine ) -> bool:
        from pyConics.utils import are_perpendicular

        # Returns True if the lines are orthogonal.
        return are_perpendicular( self, other )
    
    def __add__( self, other: CLine ) -> bool:
        # Returns True if the lines are orthogonal.
        return self.are_perpendicular( other )

    def are_parallel( self, other: CLine ) -> bool:
        from pyConics.utils import are_parallel

        # Returns True if the lines are parallel.
        return are_parallel( self, other )
    
    def __floordiv__( self, other: CLine ) -> bool:
        # Returns True if the lines are parallel.
        return self.are_parallel( other )
    
    def __eq__( self, other: CLine ) -> bool:
        # Are l1 // l2?
        if ( self.are_parallel( other ) == False ):
            return False

        # Return True if dist( l1, l2 ) = 0.0.
        if ( self.distance( other ) == 0.0 ):
            return True
        return False
    
    def at_infinity( self ) -> bool:
        if ( ( self.gform[ 0 ] == 0.0 ) and ( self.gform[ 1 ] == 0.0 ) ):
            return True
        return False
    
    def are_coincident( self, other: CLine ) -> bool:
        if ( self == other ):
            return True
        return False

    def are_concurrent( self, other: CLine ) -> bool:
        if ( self // other ):
            return False
        return True

    def sequence( self, x: list[ float ] ) -> tuple[ CPoint, ... ]:
        from pyConics.point import CPoint
        
        xy = []

        # Test for lines at infinity.
        if ( ( self.gform[ 0 ] == 0.0 ) and ( self.gform[ 1 ] == 0.0 ) ):
            return tuple( [ CPoint( ( 0.0, 0.0, 0.0 ), shift_origin = False ) ] )

        # Test for the other conditions.
        y = x
        alp: float = self.gform[ 0 ]
        bet: float = self.gform[ 1 ]
        gam: float = self.gform[ 2 ]
        for i, _x in enumerate( x ):
            if ( bet == 0.0 ):
                xy.append( CPoint( ( -gam / alp, y [ i ] ), shift_origin = False ) )
            else:
                xy.append( CPoint( ( _x, ( ( -alp * _x ) - gam ) / bet ), shift_origin = False ) )
        return tuple( xy )
    
#------------------------------------------------------------------
# Internal functions.
#  
def _validate_line( line: tuple[ float, float, float ] ) -> np.ndarray:
    if ( len( line ) == 3 ):
        return np.array( line )
    else:
        raise CLineTypeError( CLine.__name__, CLine.gform.fget.__name__ )

#------------------------------------------------------------------
# For development and test.
#  
if __name__ == '__main__':
    # Keep this imports even there is no test code.
    from pyConics.point import CPoint
    from pyConics.line import CLine
    
    import os
    os.system( 'cls' )

    # Create the line y = x + 1
    print( origin )
    l1 = CLine( ( 1, -1, 1 ) )
    print( l1, '\n' )

    # Change the origin to ( 0, 1 ), update the origin and back it to the origin.
    origin.x = 0
    origin.y = 1
    print( origin )
    l1.update_origin()
    print( l1, '\n' )
    origin.reset()
    print( origin )
    l1.update_origin()
    print( l1, '\n' )

    # Change the origin to ( 1, 0 ), update the origin and back it to the origin.
    origin.x = 1
    origin.y = 0
    print( origin )
    l1.update_origin()
    print( l1, '\n' )
    origin.reset()
    print( origin )
    l1.update_origin()
    print( l1, '\n' )
 
    # How to use cross product.
    p1 = CPoint( ( 1, 1 ) )      # p1 = ( 1, 1 )
    p2 = CPoint( ( -1, -1 ) )    # p2 = ( -1, -1 ) 
    l1: CLine = p1.cross( p2 )   # l1: y = x
    print( l1, '\n' )
    l1: CLine = p1 * p2          # l1: y = x
    print( l1, '\n' )
    
    l1 = CLine( ( 1, -1, 1 ) )   # y = x + 1
    l2 = CLine( ( 1, -1, -1 ) )  # y = x - 1
    l3 = CLine( ( -1, -1, 1 ) )  # y = -x + 1

    p3: CPoint = l1.cross( l2 )   # p3 is a point at the infinity.
    print( p3, '\n' )
    p3: CPoint = l1 * l2          # p3 is a point at the infinity.
    print( p3, '\n' )
    p4: CPoint = l1.cross( l3 )   # p4 = ( 0, 1 )
    print( p4, '\n' )
    p4: CPoint = l1 * l3          # p4 = ( 0, 1 )
    print( p4, '\n' )
    p5: CPoint = l2.cross( l3 )   # p5 = ( 1, 0 )
    print( p5, '\n' )
    p5: CPoint = l2 * l3          # p5 = ( 1, 0 )
    print( p5, '\n' )

    p6 = CPoint( ( 1, 0 ) )
    l4: CLine = l1.cross( p6 )  # l4 = ( 1, 1, -1 ) that pass through p6
    print( l4, '\n' )
    l4: CLine = l1 * p6         # l4 = ( 1, 1, -1 ) that pass through p6
    print( l4, '\n' )
    l5: CLine = p6.cross( l1 )  # l5 = ( 1, 1, -1 ) that pass through p6
    print( l5, '\n' )
    l5: CLine = p6 * l1         # l5 = ( 1, 1, -1 ) that pass through p6
    print( l5, '\n' )

    # Shifting origin.
    origin.x = 3
    origin.y = 2
    print( origin )
    
    # Point is in or is not in a Line.
    # for...
    #  l1: y = x + 1 and p4 = ( 0, 1 ) => p4 in l1
    l1.update_origin()
    p4.update_origin()
    p5.update_origin()
    print( l1 ) 
    print( p4 )
    print( f'Point p4 belongs to Line l1? {p4 in l1}\n' )
    
    #  l1: y = x + 1 and p5 = ( 1, 0 ) => p5 in l1 
    print( l1 ) 
    print( p5 )
    print( f'Point p5 belongs to Line l1? {p5 in l1}\n' )

    # Are Lines parallel or orthogonal?
    l1 = CLine( ( 1, -1, 0 ), 'l1' )  # x = y
    l2 = CLine( ( 1, -1, 1 ), 'l2' )  # y = x + 1
    l3 = CLine( ( 1, 1, -2 ), 'l3' )  # y = -x + 2
    
    # Are the lines parallel?
    print( l1, l2, l3, sep = '\n' )
    print( f'Are l1 and l2 parallel? {l1 // l2}' )
    print( f'Are l1 and l3 parallel? {l1 // l3}' )
    print( f'Are l2 and l3 parallel? {l2 // l3}' )

    # Are the lines perpendicular?
    print( f'Are l1 and l2 perpendicular? {l1 + l2}' )
    print( f'Are l1 and l3 perpendicular? {l1 + l3}' )
    print( f'Are l2 and l3 perpendicular? {l2 + l3}\n' )

    # Distance between a point and a line.
    p1 = CPoint( ( 1, 0 ), 'p1' )
    l1 = CLine( ( 1, -1, 1 ), 'l1' )
    dlp = l1.distance( p1 )
    dpl = p1.distance( l1 )
    print( f'The distance from {l1}\nto {p1}\nis {dlp:.4f}.\n' )
    print( f'The distance from {p1}\nto {l1}\nis {dpl:.4f}.\n' )

    # Distance between two lines.
    l1 = CLine( ( 1, -1, 1 ), 'l1' )
    l2 = CLine( ( 1, -1, -1 ), 'l2' )
    d12 = l1.distance( l2 )
    d21 = l2.distance( l1 )
    print( f'The distance from {l1}\nto {l2}\nis {d12:.4f}.\n' )
    print( f'The distance from {l2}\nto {l1}\nis {d21:.4f}.\n' )

    # 
    # Test for epsilon number condition.
    l1 = CLine( ( 1, -1, 1 ) )           # y = x + 1
    l2 = CLine( ( -2 * 0.99999, -2 * -1, -2 * -1 ) )    # y = 0.99999x + 1
    # Are l1 and l2 parallel?
    p1 = l1 * l2
    print( f'Intersection point between l1 and l2:\n\t{p1}' )
    print( f'Are l1 and l2 parallel? {l1 // l2}.\n' )

    # Shifting origin.
    origin.reset()
    print( origin )

    # Are these points the same?
    l1 = CLine( ( 1, -1, 1 ), 'l1' )           # y = x + 1
    l2 = CLine( ( -2 * 0.99999, -2 * -1, -2 * 1 ), 'l2' )    # y = 0.99999x + 1
    l3 = CLine( ( 1, -1, -1 ), 'l3' )           # y = x - 1
    print( l1 )
    print( l2 )
    print( l3 )
    print( f'l1 == l1? {l1 == l1}.' )
    print( f'l1 == l2? {l1 == l2}.' )
    print( f'l2 == l1? {l2 == l1}.' )
    print( f'l2 == l2? {l2 == l2}.' )
    print( f'l1 == l3? {l1 == l3}.' )
    print( f'l3 == l1? {l3 == l1}.' )
    print( f'l2 == l3? {l2 == l3}.' )
    print( f'l3 == l2? {l3 == l2}.\n' )

    # Lines at the infinity?
    l1 = CLine( ( 0, 0, 2 ), 'l1' )
    l2 = CLine( ( 1, -1, 1 ), 'l2' )
    print( l1 )
    print( l2 )
    print( f'l1 is a line at the infinity? {l1.at_infinity()}.' )
    print( f'l2 is a line at the infinity? {l2.at_infinity()}.\n' )

    ps1 = l2.sequence( [ 0.1, 0.2, 0.3, 0.4 ])
