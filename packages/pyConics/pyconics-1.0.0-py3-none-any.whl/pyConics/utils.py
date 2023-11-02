#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'skew_symmetric', 'cross', 'dot', 'are_perpendicular', \
            'are_parallel', 'distance' ]

#------------------------------------------------------------------
# Import from...
#
from typing import Any
from numpy import linalg as LA

#------------------------------------------------------------------
# Import from...
# We use here TYPE_CHECKING constant to avoid circular import  
# exceptions.
#
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ... # Do nothing here, because there are no pyConics modules
        # here to be imported.
        
from pyConics.errors import CTypeError, CArgumentsError
from pyConics.tolerance import tol
from pyConics.constants import const
from pyConics.point import CPoint
from pyConics.line import CLine

#------------------------------------------------------------------
# Import as...
#
import numpy as np

def skew_symmetric( gf: CPoint | CLine ) -> np.ndarray:
    if ( not isinstance( gf, ( CPoint, CLine ) ) ):
        raise CTypeError( gf.__class__.__name__ )

    # Build a skew-symmetric matrix from a point or a Line.
    l1 = [ 0.0, -gf.gform[ 2 ], gf.gform[ 1 ] ]
    l2 = [ gf.gform[ 2 ], 0.0, -gf.gform[ 0 ] ]
    l3 = [ -gf.gform[ 1 ], gf.gform[ 0 ], 0.0 ]
    return np.array( [ l1, l2, l3 ] )

def cross( gf1: CPoint | CLine, gf2: CPoint | CLine ) -> Any[ CPoint | CLine ]:
    if ( not isinstance( gf1, ( CPoint, CLine ) ) ):
        raise CTypeError( gf1.__class__.__name__ )
    if ( not isinstance( gf2, ( CPoint, CLine ) ) ):
        raise CTypeError( gf2.__class__.__name__ )
    
    # There are 3 conditions:
    # 1) Point x Point returns a Line that passes
    #    through both Points.
    # 2) Line x Line returns a Point that intercepts
    #    both Lines.
    # 3) Line x Point or Point x Line returns a Line
    #    that pass through the Point.
    if ( ( isinstance( gf1, ( CPoint ) ) ) and ( isinstance( gf2, ( CLine ) ) ) ) or \
        ( ( isinstance( gf1, ( CLine ) ) ) and ( isinstance( gf2, ( CPoint ) ) ) ):
        # Condition 3.
        to_origin = np.array( [ [ 1.0, 0.0, 0.0 ], [ 0.0, 1.0, 0.0 ], [ 0.0, 0.0, 0.0 ] ] )

        # Get the skew-symmetric matrix from gf{1,2}.
        if ( isinstance( gf1, ( CPoint ) ) ):
            ss_gf = skew_symmetric( gf1 )
            res = ss_gf @ to_origin @ gf2.gform
        else:
            ss_gf = skew_symmetric( gf2 )
            res = ss_gf @ to_origin @ gf1.gform
        return CLine( tuple[float, float, float]( res ), shift_origin = False )
    elif ( ( isinstance( gf1, ( CPoint ) ) ) and ( isinstance( gf2, ( CPoint ) ) ) ):
        # Condition 1.
        # Points couldn't be the same.
        if ( gf1 == gf2 ):
            return CLine( ( 0.0, 0.0, 0.0 ), shift_origin = False )
        
        # Get the skew-symmetric matrix from gf1.
        ss_gf1 = skew_symmetric( gf1 )

        # Cross product betwwen them.
        return CLine( tuple[float, float, float]( ss_gf1 @ gf2.gform ), shift_origin = False )
    else:    
        # Condition 2.
        # Lines couldn't be the same.
        if ( gf1 == gf2 ): # type: ignore
            return CPoint( ( 0.0, 0.0, 0.0 ), shift_origin = False )
        
        # Are they parallel lines? Test for epsilon number condition.
        alpha = 1.0
        if ( are_parallel( gf1, gf2 ) == True ): # type: ignore
            # If gf1 // gf2 then gf1[ 0 : 1 ] == gf2[ 0 : 1 ] and
            # a constant alpha must multiply all the vector.
            if ( gf1.gform[ 1 ] != 0.0 ):
                alpha = gf2.gform[ 1 ] / gf1.gform[ 1 ]
            elif ( gf1.gform[ 0 ] != 0.0 ):
                alpha = gf2.gform[ 0 ] / gf1.gform[ 0 ]
            else:
                alpha = 1.0
            
            a = alpha * gf1.gform[ 0 ]
            b = alpha * gf1.gform[ 1 ]
            c = alpha * gf1.gform[ 2 ]
            l0 = CLine( ( a, b, c ), 'l0' )

            # Get the skew-symmetric matrix from l0.
            ss_gf1 = skew_symmetric( l0 )
        else:
            # Get the skew-symmetric matrix from gf1.
            ss_gf1 = skew_symmetric( gf1 )

        return CPoint( tuple[ float, float, float ]( ( ss_gf1 @ gf2.gform ) / alpha ), shift_origin = False )

def dot( gf1: CPoint | CLine, gf2: CPoint | CLine ) -> float:
    if ( not isinstance( gf1, ( CPoint, CLine ) ) ):
        raise CTypeError( gf1.__class__.__name__ )
    if ( not isinstance( gf2, ( CPoint, CLine ) ) ):
        raise CTypeError( gf2.__class__.__name__ )
    
    # There are 2 conditions:
    # 1) Point x Line returns their inner product.
    # 2) Line x Point returns their inner product.
    if ( ( isinstance( gf1, ( CPoint ) ) ) and ( isinstance( gf2, ( CLine ) ) ) ):
        # Condition 1.
        res = np.inner( gf1.gform, gf2.gform )
    elif ( ( isinstance( gf1, ( CLine ) ) ) and ( isinstance( gf2, ( CPoint ) ) ) ):
        # Condition 2.
        res = np.inner( gf1.gform, gf2.gform )
    else:
        raise CArgumentsError( dot.__name__, gf1.__class__.__name__, gf2.__class__.__name__ )
    return 0.0 if ( tol.iszero( res ) ) else res

def are_parallel( gf1: CLine, gf2: CLine ) -> bool:
    if ( not isinstance( gf1, CLine ) ):
        raise TypeError( gf1.__class__.__name__ )
    if ( not isinstance( gf2, CLine ) ):
        raise TypeError( gf2.__class__.__name__ )
    
    # To be parallel lines, x1 == x2 and y1 == y2 must be equals
    # or ( x1 * y2 ) - ( x2 * y1 ) must be zero.
    op1  = gf1.gform[ 0 ] * gf2.gform[ 1 ]
    op2 = gf1.gform[ 1 ] * gf2.gform[ 0 ]

    return True if ( tol.iszero( op1 - op2  ) ) else False

def are_perpendicular( gf1: CLine, gf2: CLine ) -> bool:
    if ( not isinstance( gf1, CLine ) ):
        raise CTypeError( gf1.__class__.__name__ )
    if ( not isinstance( gf2, CLine ) ):
        raise CTypeError( gf2.__class__.__name__ )
    
    # To be orthogonal lines, ( x1 * x2 ) + ( y1 * y2 ) must be zero.
    op1  = gf1.gform[ 0 ] * gf2.gform[ 0 ]
    op2 = gf1.gform[ 1 ] * gf2.gform[ 1 ]

    return True if ( tol.iszero( op1 + op2  ) ) else False

def distance( gf1: CPoint | CLine, gf2: CPoint | CLine ) -> float:
    if ( not isinstance( gf1, ( CPoint, CLine ) ) ):
        raise CTypeError( gf1.__class__.__name__ )
    if ( not isinstance( gf2, ( CPoint, CLine ) ) ):
        raise CTypeError( gf2.__class__.__name__ )
    
    # Test points and lines to check if they are at the infinity.
    if ( ( gf1.at_infinity() ) or ( gf2.at_infinity() ) ):
        return const.inf

    # There are 4 conditions:
    # 1) Point x Point returns the distance between them.
    # 2) Line x Point returns the distance between them.
    # 3) Point x Line returns the distance between them.
    # 4) Line x Line returns  the distance between them if they are parallel lines.
    d = 0.0
    if ( ( isinstance( gf1, ( CPoint ) ) ) and ( isinstance( gf2, ( CPoint ) ) ) ):
        # Condition 1.
        d = float( LA.norm( gf1.gform - gf2.gform ) )
    elif ( ( isinstance( gf1, ( CLine ) ) ) and ( isinstance( gf2, ( CPoint ) ) ) ):
        # Condition 2.
        l: CLine = gf1 * gf2 # line passes through gf2 and it is orthogonal to gf1.
        p: CPoint = l * gf1  # point is the intersection point beween l and gf1.
        d = float( LA.norm( p.gform - gf2.gform ) )
    elif ( ( isinstance( gf1, ( CPoint ) ) ) and ( isinstance( gf2, ( CLine ) ) ) ):
        # Condition 3.
        l: CLine = gf1 * gf2 # line passes through gf1 and it is orthogonal to gf2.
        p: CPoint = l * gf2  # point is the intersection point beween l and gf2.
        d = float( LA.norm( p.gform - gf1.gform ) )
    else:
        # Condition 4.
        if ( are_parallel( gf1, gf2 ) == False ): # type: ignore
            return 0.0
        
        # Create a line that is orthogonal to gf1 and gf2.
        l_ort = CLine( ( gf1.gform[ 1 ], -gf1.gform[ 0 ], gf1.gform[ 2 ] ) )
        
        # Get the intersection point between those lines.
        p1 = l_ort * gf1        
        p2 = l_ort * gf2
        
        # Calc. the distance between these points.
        d = distance( p1, p2 )
    return 0.0 if ( tol.iszero( d ) ) else d

#------------------------------------------------------------------
# For development and test.
#  
if __name__ == '__main__':
    import os
    os.system( 'cls' )

    # Plot the skew-symmetric matrix of a point.
    p1 = CPoint( ( 3.0, 2.0 ) )
    print( p1, '\n' )
    ssp1 = skew_symmetric( p1 )
    print( ssp1, '\n' ) 

    # Test invalid argument for the skew_symmetric function.
    try:
        p2 = ( ( 'a', 'b' )  )
        ssp2 = skew_symmetric( p2 ) # type: ignore
    except TypeError as e:
        print( e )
    print()

    # How to use cross product.
    p1 = CPoint( ( 1, 1 ) )      # p1 = ( 1, 1 )
    p2 = CPoint( ( -1, -1 ) )    # p2 = ( -1, -1 ) 
    l1: CLine = cross( p1, p2 )  # l1: y = x
    print( l1, '\n' )
    
    l1 = CLine( ( 1, -1, 1 ) )    # y = x + 1
    l2 = CLine( ( 1, -1, -1 ) )   # y = x - 1
    l3 = CLine( ( -1, -1, 1 ) )   # y = -x + 1
    p3: CPoint = cross( l1, l2 )  # p3 is a point at the infinity.
    print( p3, '\n' )
    p4: CPoint = cross( l1, l3 )  # p4 = ( 0, 1 )
    print( p4, '\n' )
    p5: CPoint = cross( l2, l3 )  # p5 = ( 1, 0 )
    print( p5, '\n' )
    
    p6 = CPoint( ( 1, 0 ) )
    l4: CLine = cross( l1, p6 )   # l4 = ( 1, 1, -1 ) that pass through p6
    print( l4, '\n' )
    l5: CLine = cross( p6, l1 )   # l5 = ( 1, 1, -1 ) that pass through p6
    print( l5, '\n' )

    # Test invalid argument for dot function.
    try:
        print( dot( l1, l2 ) )
    except CArgumentsError as e:
        print( e )
    print()

    # Get the inner product from a Line and a Point.
    # l1: y = x + 1 and p4 = ( 0, 1 ) => <p4, l1> = 0.0 
    print( f'Inner product: < p4, l1 > = {dot( p4, l1 )}' )
    print( f'Inner product: < l1, p4 > = {dot( l1, p4 )}\n' )

    
    # Are Lines parallel or orthogonal?
    l1 = CLine( ( 1, -1, 0 ), 'l1' )  # x = y
    l2 = CLine( ( 1, -1, 1 ), 'l2' )  # y = x + 1
    l3 = CLine( ( 1, 1, -2 ), 'l3' )  # y = -x + 2
    
    # Are the lines parallel?
    print( l1, l2, l3, sep = '\n' )
    print( f'Are l1 and l2 parallel? {are_parallel( l1, l2 )}' )
    print( f'Are l1 and l3 parallel? {are_parallel( l1, l3 )}' )
    print( f'Are l2 and l3 parallel? {are_parallel( l2, l3 )}' )

    # Are the lines perpendicular?
    print( f'Are l1 and l2 perpendicular? {are_perpendicular( l1, l2 )}' )
    print( f'Are l1 and l3 perpendicular? {are_perpendicular( l1, l3 )}' )
    print( f'Are l2 and l3 perpendicular? {are_perpendicular( l2, l3 )}\n' )

    # Distance between 2 points.
    p1 = CPoint( ( 0, 1 ), 'p1' )
    p2 = CPoint( ( 1, 0 ), 'p2' )
    d12 = distance( p1, p2 )
    d21 = distance( p2, p1 )
    d11 = distance( p1, p1 )
    print( f'The distance from {p1}\nto {p2}\nis {d12:.4f}.\n' )
    print( f'The distance from {p2}\nto {p1}\nis {d21:.4f}.\n' )
    print( f'The distance from {p1}\nto {p1}\nis {d11:.4f}.\n' )

    # Distance between a point and a line.
    p1 = CPoint( ( 1, 0 ), 'p1' )
    l1 = CLine( ( 1, -1, 1 ), 'l1' )
    dlp = distance( l1, p1 )
    dpl = distance( p1, l1 )
    print( f'The distance from {l1}\nto {p1}\nis {dlp:.4f}.\n' )
    print( f'The distance from {p1}\nto {l1}\nis {dpl:.4f}.\n' )

    # Distance between two lines.
    l1 = CLine( ( 1, -1, 1 ), 'l1' )
    l2 = CLine( ( 1, -1, -1 ), 'l2' )
    l3 = CLine( ( -2 * 0.99999, -2 * -1, -2 * -1 ), 'l3' )
    d13 = distance( l1, l3 )
    d31 = distance( l3, l1 )
    d23 = distance( l2, l3 )
    print( f'The distance from {l1}\nto {l3}\nis {d13:.4f}.\n' )
    print( f'The distance from {l3}\nto {l1}\nis {d31:.4f}.\n' )
    print( f'The distance from {l2}\nto {l3}\nis {d23:.4f}.\n' )
    print( l2 * l1 )
    print( l1 * l3 )
    print( l2 * l3, '\n' )

    # Test points and lines at the infinity.
    p1 = CPoint( ( 1, 0, 0 ), 'p1' )
    print( p1 )
    p2 = CPoint( ( 1, 0 ), 'p2' )
    print( p2 )
    l1 = CLine( ( 0, 0, 1 ), 'l1' )
    print( l1 )
    l2 = CLine( ( 1, -1, -1 ), 'l2' )
    print( l2 )
    if ( distance( p1, p2 ) == const.inf ):
        print( f'p1 or p2 is a point at the infinity.' )
    if ( distance( p2, l1 ) == const.inf ):
        print( f'p2 or l1 is a point/line at the infinity.' )
    if ( distance( l2, l1 ) == const.inf ):
        print( f'l2 or l1 is a line at the infinity.' )
    if ( distance( p2, l2 ) != const.inf ):
        print( f'p2 and l2 are point and line that are not at the infinity.\n' )
    
    # Lines are coincident.
    l1 = CLine(( 1, -1, 1 ), 'l1' )
    l2 = CLine(( 2, -2, 5 ), 'l2' )
    print( l1 )
    print( l2 )
    print( cross( l1, l2 ) )
    print( l1 )
    print( l2 )
