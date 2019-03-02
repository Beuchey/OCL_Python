from __future__ import annotations # To be able to return the current class in class method. This import should become unnecessary in Python 4.0 to be able to di this.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..', 'result'))
import OclPyth

class OclWrapper_String(OclPyth.OclWrapper):

    def __init__(self, awrapped : str):
        """__init__ method.

        Args:
            awrapped (str): The target string of this wrapper.
        """
        OclPyth.OclWrapper.__init__(self, awrapped)

    def concat(self, otherObject: object) -> OclWrapper_String:
        """Concatenate the other object (eventually already wrapped) to the wrapped string.

        Args:
            otherString (str): The other string to concatenate to the wrapped stringself.

        Returns:
            An OclWrapper_String wrapping the original wrapped string concatenated with the other object (eventually already wrapped).

        OclWrapper_String('Hello World!').concat(' I\'m a string.')._wrapped
        'Hello World! I'm a string.'
        """
        if isinstance(otherObject, OclPyth.OclWrapper):
            return OclWrapper_String(self._wrapped + otherObject._wrapped)
        else:
            return OclWrapper_String(self._wrapped + otherObject)






astr = OclWrapper_String('Hello World!')
print(astr.concat(' I\'m a string.')._wrapped)
print(astr.concat(OclWrapper_String(' I\'m a another string.'))._wrapped)
