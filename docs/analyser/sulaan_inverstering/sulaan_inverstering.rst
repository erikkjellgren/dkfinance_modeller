.. role:: python(code)
   :language: python

Inverstering af SU lån simpel model
===================================

*Brug ikke dette som finansiel rådgivning. Dette er kun model.*

En meget simpel analyse af inverstering af SU lån.

Først importeres hvad der skal bruges:

.. literalinclude:: sulaan_inverstering.py
   :lines: 1-6
   
Nu bygges modellen for SU-lån.
Under uddannelse kan der lånes 3 194 DKK hver måned, https://www.su.dk/su-laan/satser-for-su-laan/, 30-10-2020.
Renter for SU lån er 4 % under uddanelse og 1 % derefter, https://www.borger.dk/oekonomi-skat-su/SU-og-oekonomi-under-uddannelse/Studiegaeld-oversigt/Studiegaeld-renter-gebyrer, 30-10-2020.

Den totale skyld efter endt uddannelse kan regnes som en "opsparing".

.. literalinclude:: sulaan_inverstering.py
   :lines: 19-21
   
Efter endt uddanelse skal der først afdrages fra 1. Januar i andet år efter endt uddannelse, heraf 18 måneder.

.. literalinclude:: sulaan_inverstering.py
   :lines: 23-24

Det månedlige afdrag kan nu beregnes, afdrags periode afhænger af størrelsen af SU lånet, https://www.borger.dk/oekonomi-skat-su/SU-og-oekonomi-under-uddannelse/Studiegaeld-oversigt/Studiegaeld-tilbagebetaling, 30-10-2020.

.. literalinclude:: sulaan_inverstering.py
   :lines: 26-32

Den totale model for SU lån er derfor:

.. literalinclude:: sulaan_inverstering.py
   :lines: 9-37

Nu kan modellen for inversteringen konstrueres.
Inverstering følger samme struktur, hvor SU lånet investeres:

.. literalinclude:: sulaan_inverstering.py
   :lines: 62-63
   
Samler kapital efter endt uddanelse:

.. literalinclude:: sulaan_inverstering.py
   :lines: 65
   
Og bliver reduceret når lånet skal betales tilbage:

.. literalinclude:: sulaan_inverstering.py
   :lines: 67
   
Hele modellen for inversteringen er derfor:

.. literalinclude:: sulaan_inverstering.py
   :lines: 40-70
   
Bemærk at når mindst mulige afkast skal findes sættes :python:`til_optimering=True`, da det så bliver et simpel minimeringsproblem.

Minimalt inversteringsafkast indenfor modellen kan nu findes, først for en tre årig uddannelse:

.. literalinclude:: sulaan_inverstering.py
   :lines: 73-84
   
Og for en fem årig uddannelse:

.. literalinclude:: sulaan_inverstering.py
   :lines: 86-97
   
Det vil sige at et årlig afkast på 1.7% er nok for at inversting af SU lån kan betale sig inden for denne model.
For inversteringsmodellen er det antaget at der ikke betalles noget skat.
Endnu vigtigere er det antaget der er samme afkast hver eneste måned. 
Der er altså ikke nogen risiko analyse af hvad der sker, hvis der er et stort fald på forskellige tidspunkter af forløbet.
Det skal også bemærkes at SU lån ikke er fast forrentet, men bundet til diskontoen, https://www.su.dk/su-laan/tilbagebetaling-af-dit-su-laan/renter-paa-dit-su-laan/, 15-11-2020.

Hele modellen er:

.. literalinclude:: sulaan_inverstering.py
   :lines: 1-97


