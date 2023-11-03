#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'CPoint2CoordXY', 'CLine2MatrixXY', 'CPointList2MatrixXY',\
           'CLineList2MatrixXY' ]

#------------------------------------------------------------------
# Import from...
#

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
from pyConics.point import CPoint
from pyConics.line import CLine

#------------------------------------------------------------------
# Import as...
#
import numpy as np

def CPoint2CoordXY( p: CPoint ) -> np.ndarray:
    # Test for points at infinity.
    if ( p.gform[ 2 ] == 0.0 ):
        return np.array( [ const.inf, const.inf ] )
    return np.array( [ p.gform[ 0 ], p.gform[ 1 ] ] )

def CLine2MatrixXY( l: CLine, xlim: tuple[ float, float ],
                    ylim: tuple[ float, float ], samples: int ) -> np.ndarray:
    # Test for lines at infinity.
    if ( ( l.gform[ 0 ] == 0.0 ) and ( l.gform[ 1 ] == 0.0 ) ):
        return np.array( [ const.inf, const.inf ] )[np.newaxis]

    # Test for the other conditions.
    x = np.linspace( *xlim, samples )[np.newaxis].T
    y = np.linspace( *ylim, samples )[np.newaxis].T
    alp: float = l.gform[ 0 ]
    bet: float = l.gform[ 1 ]
    gam: float = l.gform[ 2 ]
    if ( bet == 0.0 ):
        v = ( -gam / alp ) * np.ones( ( x.size, 1 ) )
        return np.block( [ [ v, y ] ] )
    elif ( abs( alp / bet ) <= 1.0 ):
        v = ( ( -alp * x ) - gam ) / bet
        return np.block( [ [ x, v ] ] )
    else:
        v = ( ( -bet * y ) - gam ) / alp
        return np.block( [ [ v, y ] ] )

def CPointList2MatrixXY( pp: list[ CPoint ] ) -> np.ndarray:
    X = []
    Y = []
    for p in pp:
        xy = CPoint2CoordXY( p )
        X.append( xy[ 0 ] )
        Y.append( xy[ 1 ] )

    # Create the Nx2 matrix.
    x = np.array( X )[np.newaxis].T
    y = np.array( Y )[np.newaxis].T
    return np.block( [ [ x, y ] ] )

def CLineList2MatrixXY( ll: list[ CLine ], xlim: tuple[ float, float ],
                        ylim: tuple[ float, float ], samples: int ) -> list[ np.ndarray ]:
    X = []
    Y = []
    for l in ll:
        xy = CLine2MatrixXY( l, xlim, ylim, samples )
        X.append( xy[ :, 0 ] )
        Y.append( xy[ :, 1 ] )

    # Create the NxM matrix.
    x = np.array( X ).T
    y = np.array( Y ).T
    return [ x, y ]
