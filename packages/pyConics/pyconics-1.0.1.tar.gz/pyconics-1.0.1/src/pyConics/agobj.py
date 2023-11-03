#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'CAGObj' ]

#------------------------------------------------------------------
# Import from...
#  
from abc import ABC, abstractmethod

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
# Abstract Base Class AGObj.
#  
class CAGObj( ABC ):
    @abstractmethod
    def __init__( self, name: str = '' ) -> None:
        # Set the name of the AGObject.
        self.name = name

        # Create a zero-dimensional array that will represent
        # a geometric form such as point, line and conics.
        # Each child class will redim this array.
        self._gform = np.ndarray( shape = ( 0, 0 ) )
        
        # Save the original geo form. So, we are able
        # to return its value from origin.
        self._from_origin = np.ndarray( shape = ( 0, 0 ) )

    @abstractmethod
    def __repr__( self ) -> str:
        # Each child class will implement this method.
        return super().__repr__()
    
    @abstractmethod
    def update_origin( self ) -> None:
        # Each child class will implement this method.
        pass # Do nothing.

    @property
    def name( self ) -> str:
       return self._name
    
    @name.setter
    def name( self, name: str ) -> None:
       self._name = name

    @property
    def gform( self ) -> np.ndarray:
       return self._gform
    
    @property
    def from_origin( self ) -> np.ndarray:
       return self._from_origin
