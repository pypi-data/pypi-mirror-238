"""Example library for illustrating publication process.

Python library that serves as an example/template
for an open-source package publishing guide.
"""

import doctest

class published(): # pylint: disable=C0103,R0903
    """
    A published package.

    >>> p = published()
    >>> p.is_published()
    True
    >>> p.published = False
    >>> p.is_published()
    Traceback (most recent call last):
      ...
    RuntimeError: package must be published
    """
    def __init__(self, text):
        """Build an instance."""
        self.published = True
        self.text = text

    def is_published(self):
        """Check publication status."""
        if not self.published:
            raise RuntimeError("package must be published")

        return self.published
    
    def you_talk(self):
        print("Hi, I am you talk", self.text)

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover

