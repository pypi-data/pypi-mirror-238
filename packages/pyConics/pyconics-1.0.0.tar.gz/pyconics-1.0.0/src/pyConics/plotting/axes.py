#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'CAxes' ]

#------------------------------------------------------------------
# Import from ...
#
from pyConics.constants import const
from pyConics.errors import CValueError, CTypeError
from matplotlib import pyplot as plt
from pyConics import CPoint, CLine
from pyConics.plotting.utils import CPoint2CoordXY, CLine2MatrixXY
from pyConics.plotting.utils import CPointList2MatrixXY, CLineList2MatrixXY

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
import numpy as np

#------------------------------------------------------------------
# Class CFigure.
#  
class CAxes:
    def __init__( self, axes: plt.Axes ) -> None: #type: ignore
        self._axes = axes

    def __repr__( self ) -> str:
        _arts = self._axes.findobj( None )
        return f'{self.__class__.__name__} class with {len( _arts )} objects.'

    def get_pyplot_axes( self ) -> plt.Axes: #type: ignore
        return self._axes

    @property
    def xlim( self ) -> tuple[ float, float ]:
        return self._axes.get_xlim()
     
    @xlim.setter
    def xlim( self, xl: tuple[ float, float ] ) -> None:
        self._axes.set_xlim( xl )

    @property
    def ylim( self ) -> tuple[ float, float ]:
        return self._axes.get_ylim()
    
    @ylim.setter
    def ylim( self, yl: tuple[ float, float ] ) -> None:
        self._axes.set_ylim( yl )
    
    @property
    def xticks( self ) -> np.ndarray:
        return self._axes.get_xticks()
    
    @xticks.setter
    def xticks( self, xt: np.ndarray ) -> None:
        self._axes.tick_params( axis = 'x', labelsize = const.tickssize )
        self._axes.set_xticks( xt )

    @property
    def yticks( self ) -> np.ndarray:
        return self._axes.get_yticks()
    
    @yticks.setter
    def yticks( self, yt: np.ndarray ) -> None:
        self._axes.tick_params( axis = 'y', labelsize = const.tickssize )
        self._axes.set_yticks( yt )

    @property
    def title( self ) -> str:
        return self._axes.get_title()
    
    @title.setter
    def title( self, title: str ) -> None:
        self._axes.set_title( title, fontsize = const.titlesize )

    @property
    def xlabel( self ) -> str:
        return self._axes.get_xlabel()
    
    @xlabel.setter
    def xlabel( self, label: str ) -> None:
        self._axes.set_xlabel( label, fontsize = const.labelsize )

    @property
    def ylabel( self ) -> str:
        return self._axes.get_ylabel()
    
    @ylabel.setter
    def ylabel( self, label: str ) -> None:
        self._axes.set_ylabel( label, fontsize = const.labelsize )

    def text( self, x: float, y: float, txt: str, **kwargs ) -> None:
        if( not 'fontsize' in kwargs.keys() ):
            kwargs[ 'fontsize' ] = const.textsize

        # Call Axes.text() method.
        self._axes.text( x, y, txt, kwargs )
        
    def plot( self, *args, clinesamples: int = 11, **kwargs ) -> None:
        new_args = [] # new arguments to be passed into axes.plot.

        # Search for a CPoint, a CLine, or lists of them.
        for arg in args:
            if ( isinstance( arg, CPoint ) ):
                # Convert a CPoint to a XY-coord.
                xy = CPoint2CoordXY( arg )
                new_args.append( xy[ 0 ] )
                new_args.append( xy[ 1 ] )
                continue

            if ( isinstance( arg, CLine ) ):
                # Convert a CLine to a (nx2)-matrix.
                xy = CLine2MatrixXY( arg, self.xlim, self.ylim, clinesamples )
                new_args.append( xy[ :, 0 ] )
                new_args.append( xy[ :, 1 ] )
                continue

            if ( isinstance( arg, list ) ):
                # It is a list, but is it a list of CPoint or CLine?
                if ( not _is_cpoint_list( arg ) ) and ( not _is_cline_list( arg ) ):
                    new_args.append( arg )
                    continue

                # Yes. It is a list of CPoint or CLine.
                if ( _is_cpoint_list( arg ) ):
                    # convert the list to a (nx2)-matrix.
                    xy = CPointList2MatrixXY( arg )
                    new_args.append( xy[ :, 0 ] )
                    new_args.append( xy[ :, 1 ] )
                    continue

                if ( _is_cline_list( arg ) ):
                    # convert the list to a list of (nxm)-matrix.
                    xy = CLineList2MatrixXY( arg, self.xlim, self.ylim, clinesamples )
                    new_args.append( xy[ 0 ] )
                    new_args.append( xy[ 1 ] )
                    continue

            # It is not a pyConic object.
            new_args.append( arg )

        self._axes.plot( *tuple( new_args ), **kwargs ) # type: ignore

#------------------------------------------------------------------
# Internal functions.
#  
def _is_cpoint_list( arg: list ) -> bool:
    for p in arg:
        if ( not isinstance( p, CPoint ) ):
            return False
    return True

def _is_cline_list( arg: list ) -> bool:
    for l in arg:
        if ( not isinstance( l, CLine ) ):
            return False
    return True

#------------------------------------------------------------------
# For development and test.
#  
if ( __name__  == '__main__' ):
    ...
