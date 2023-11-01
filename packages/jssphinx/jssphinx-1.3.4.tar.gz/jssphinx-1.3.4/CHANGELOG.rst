Release history and notes
=========================
.. References

.. _Semantic versioning: https://semver.org/spec/v2.0.0.html

`Semantic versioning`_ is used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  1.0.0 to 1.0.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  1.0.4 to 1.1.0).
- All backwards incompatible changes are mentioned in this document.

1.3.4
-----
*2023-10-31*

- Slightly change the behaviour of the ``jsphinx-toggle-emphasis`` directive.
  Instead of replacing the original block with it, we toggle visibility of the
  full code under the link. Old behaviour could still be achieved by using
  ``jsphinx-toggle-emphasis-replace`` instead.

1.3.3
-----
*2023-10-28*

.. note::

    Release dedicated to my daughter Ani, who turned 4 yesterday.
    Happy birthday, my dear girl!

- Python package released on PyPI.

1.3.2
-----
*2023-10-24*

- Fixes in docs.

1.3.1
-----
*2023-10-21*

- Fixes in the JS for toggling emphasized lines.

1.3.0
-----
*2023-10-20*

- Project renamed to ``jsphinx``. Rename ``prismjs-sphinx`` to ``jsphinx``
  everywhere you used it (CDN, documentation).

1.2.1
-----
*2023-10-19*

- Add `toggle emphasized lines` functionality for toggling emphasized lines,
  inside ``.. container:: jsphinx-toggle-emphasis`` blocks.

1.2.0
-----
*2023-10-18*

- Documentation improvements.
- Test rendered documentation.
- Change ``.. container:: jsphinx``
  to ``.. container:: jsphinx-download``. Update your documentation
  accordingly.

1.1.2
-----
*2023-10-18*

- Remove ``jQuery`` requirement.
- Add ``pydata_sphinx_theme`` theme.

1.1.1
-----
*2023-10-17*

- Added ``sphinx_book_theme``.

1.1.0
-----
*2023-10-15*

- The jsphinx adapter JavaScript now only hooks on links wrapped with
  ``jsphinx`` class (easily achieved by nesting the ``:download:``
  or entire block under ``.. container:: jsphinx`` block). See the
  example below:

  .. code-block:: rst

     .. container:: jsphinx

        *See the full example*
        :download:`here <_static/py/faker_file_docx_1.py>`

1.0.5
-----
*2023-10-13*

- Minor colour corrections in all themes.

1.0.4
-----
*2023-10-13*

- Clean up pyproject.toml.
- Minor improvements of ``alabaster`` and ``bootstrap`` themes.
- Major documentation improvements.
- Add Python tests.

1.0.3
-----
*2023-10-11*

- Added more themes.

1.0.2
-----
*2023-10-10*

- Fixes in docs.

1.0.1
-----
*2023-10-10*

- Minor fixes.

1.0.0
-----
*2023-10-10*

- Initial release.
