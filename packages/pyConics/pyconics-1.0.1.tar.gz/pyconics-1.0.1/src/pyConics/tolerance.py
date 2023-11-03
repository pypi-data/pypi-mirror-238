#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'tol' ]

#------------------------------------------------------------------
# Import from...
#  
from dataclasses import dataclass

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
# Import as...
#  
import numpy as np

#------------------------------------------------------------------
# Data Class Origin.
#  
@dataclass
class CTolerance:
    eps_iszero: float = 1e-4    # It is used in iszero function.
    eps_relzero: float = 1e-5   # It is used in adjust2relzeros function.

    def iszero( self, num: float ) -> bool:
        if ( abs( num ) <= self.eps_iszero ):
            return True
        return False

    def adjust2relzeros( self, x: np.ndarray ) -> np.ndarray:
        if ( x.size <= 1 ):
            return x
        
        # Get the rank of the largest number in x.
        rk: float = _larger_rank( x )

        # Return 'x' that was adjusted to relative zeros.
        return np.where( np.abs( x ) > rk * self.eps_relzero, x, 0.0 )

#------------------------------------------------------------------
# Internal functions.
#  
def _larger_rank( x: np.ndarray ) -> float:
    x_max: float = np.max( np.abs( x ) )
    x_min: float = np.min( np.abs( x ) )

    if ( ( x_max == 0.0 ) and ( x_min == 0.0 ) ):
        return 0.0
    
    p_rk = 1
    if ( x_max > 1.0 ): # for values greater than 1.0
        while ( ( x_max // 10.0 ) != 0.0 ):
            x_max = x_max // 10.0
            p_rk += 1

    else: # for values less or equal to 1.0
        while ( ( ( x_max * 10.0 ) // 10.0 ) == 0.0 ):
            x_max *= 10.0
            p_rk -= 1

    if ( x_max == 1.0 ):
        p_rk -= 1

    return ( 10 ** p_rk )

#--------------------------------------------------------------
# Global variable.
#
tol = CTolerance()

#------------------------------------------------------------------
# For development and test.
#  
if __name__ == '__main__':
    # Testing _larger_rank fucntion.
    x = np.array( [ 99, 0.0, 0.0 ] )
    print( _larger_rank( x ) )

    y = np.array( [ 0.05, 0.0, 0.0 ] )
    print( _larger_rank( y ) )

    A = np.array( [ [ 100000, 1 ],[ 1, 1 ] ] )
    A = tol.adjust2relzeros( A )
    print( A )

    A = np.array( [ [ 1e-1, 1e-6 ],[ 1e-6, 1e-5 ] ] )
    A = tol.adjust2relzeros( A )
    print( A )
    