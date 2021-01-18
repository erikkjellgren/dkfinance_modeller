.. role:: python(code)
   :language: python

Indeks og ÅOP for Nordnet Månedsopsparing og SKATs positiv liste.
=================================================================

*Husk selv at checke op på webscrapede informationer, for at sikre de er rigtige.*

Givet lister som `SKATs positiv liste <https://skat.dk/skat.aspx?oid=2244641>`_
og `Nordnets månedsopsparing <https://www.nordnet.dk/dk/tjenester/manedsopsparing>`_,
kan det være svært at overskue omkostninger og hvilke indeks de forskellige ETFer følger.

På https://www.justetf.com/en/ kan man finde informationer fra en lang liste af ETFer.
Ved at bruge Python kan man webscrape informationer, og kompilere dem i en tabel.

Tabelen for Nordnets månedsopsparing kan findes her:
`Nordnets månedsopsparing ETF liste <https://docs.google.com/spreadsheets/d/1FTxNdAT43Dkcix32ase-R8O1tQDkWkr3hvvkqLLOihY/edit?usp=sharing>`_.

Listen for Nordnets månedsopsparing inkludere alle udenlandske ETFer med undtagelse af WisdomTree Brent Crude Oil (ISIN: DE000A1N49P6) og WisdomTree WTI Crude Oil (ISIN: DE000A0KRJX4).

Tabelen for SKATs positiv liste kan findes her:
`SKATs positiv ETF liste <https://docs.google.com/spreadsheets/d/181WgeIKI_c9z2DpjqcBxXkOwbcPLnrDjRT4JhHY8eB8/edit?usp=sharing>`_.

For listen over ETFer på SKATs positiv liste er det kun ETFer fra Amundi, iShares, JPMorgan, Lyxor og Xtrackers.

*Hvis du har fået værdi ud af denne data-samling kan du støtte med* `en kop kaffe <https://www.buymeacoffee.com/erikrk>`_, *hvis du har lyst :)*

Python detaljer
###############

Starter med at importere alle de moduler der skal bruges:

.. literalinclude:: webscrape_skat_og_nordnet_lister.py
   :lines: 1-3

Webscraping fra SKATs positiv liste:

.. literalinclude:: webscrape_skat_og_nordnet_lister.py
   :lines: 5-21

Webscraping fra Nordnets månedsopsparing:

.. literalinclude:: webscrape_skat_og_nordnet_lister.py
   :lines: 24-42

Hele scriptet er:

.. literalinclude:: webscrape_skat_og_nordnet_lister.py
   :lines: 1-42

