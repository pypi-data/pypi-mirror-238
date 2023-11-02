#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'origin' ]

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
class Origin:
    x: float = 0.0
    y: float = 0.0

    def change_point( self, point: np.ndarray ) -> np.ndarray:
        return point - np.array( ( self.x, self.y, 0.0 ) )
    
    def change_line( self, line: np.ndarray ) -> np.ndarray:
        c = ( line[ 0 ] * self.x ) + ( line[ 1 ] * self.y )
        return line + np.array( ( 0.0, 0.0, c ) )

    def reset( self ) -> None:
        self.x = 0.0
        self.y = 0.0

#--------------------------------------------------------------
# Global variable.
#
origin = Origin()
