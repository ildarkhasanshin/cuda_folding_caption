Plugin for CudaText.
Shows additional 'statusbar' on the editor top: chain of folding-blocks containing
line with (first) caret. Click on cells in this 'statusbar' moves caret to the
begin of corresponding block.

Configuration
-------------
Menu item "Options / Settings-plugins / Folding Caption / Config".
Options in the settings/plugins.ini file, in [folding_caption], are:

- "lexers": comma-separated list of lexers, which are allowed.
- "position": "top" or "bottom" (without quotes).
- "max_length": maximal length of statusbar cells, in chars.
- "cuts": comma-separated list of words; if statusbar cell starts with any of
         these words, bracketed part "(....)" will be stripped from cell.

Authors:
  ildar r. khasanshin (@ildarkhasanshin at GitHub)
  Alexey Torgashin (CudaText)
License: MIT
