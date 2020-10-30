Udledninger
===========

Udledninger af simple formler relevant for personlig finans.

Månedlig afbetalling
--------------------

Månedlig ydelse for at afbetale i lån over :math:`n` måneder. 
Ved at starte fra ligning :eq:`opsparing` og sætte :math:`k_{\mathrm{start}}\rightarrow k_{\mathrm{lån}}` og :math:`k_{\mathrm{måned}}\rightarrow-k_{\mathrm{afbetalling}}`, 
kan det ses at det tilbage værende kapital af lånet efter :math:`n` måneder er:

.. math::
   k_{n}=k_{\mathrm{lån}}\left(1+r\right)^{n} - k_{\mathrm{afbetalling}}\left(\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1+\left(1+r\right)^{n}\right)
   
Her er :math:`k_{\mathrm{lån}}` størrelsen af lånet ved begyndelsen afbetalling.
:math:`k_{\mathrm{afbetalling}}` er den månedelige ydelse, og :math:`r` er renten på lånet.

Lånet er betal ud når :math:`k_{n}=0`, derfor:

.. math::
   0=k_{\mathrm{lån}}\left(1+r\right)^{n}-k_{\mathrm{afbetalling}}\left(\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1+\left(1+r\right)^{n}\right)
   
Herved findes det at:

.. math::
   k_{\mathrm{afbetalling}}=\frac{k_{\mathrm{lån}}\left(1+r\right)^{n}}{\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1+\left(1+r\right)^{n}}

Opsparing
---------

Ved en opsparing med et start indskud på :math:`k_{\mathrm{start}}`, et månedligt indskud på :math:`k_{\mathrm{måned}}` og en rente på :math:`r`, vil kapitalet efter en måned være:

.. math::
   k_{1}=k_{\mathrm{start}}\left(1+r\right)+k_{\mathrm{måned}}\left(1+r\right)
   
Efter to måneder:

.. math::
   \begin{eqnarray}
   k_{2} &=& k_{1}\left(1+r\right)+k_{\mathrm{m\mathring{a}ned}}\left(1+r\right) \\
         &=& \left(k_{\mathrm{start}}\left(1+r\right)+k_{\mathrm{m\mathring{a}ned}}\left(1+r\right)\right)\left(1+r\right)+k_{\mathrm{m\mathring{a}ned}}\left(1+r\right) \\
         &=& k_{\mathrm{start}}\left(1+r\right)^{2}+k_{\mathrm{m\mathring{a}ned}}\left(1+r\right)^{2}+k_{\mathrm{m\mathring{a}ned}}\left(1+r\right)
    \end{eqnarray}
    
Det kan nu ses at det gennerale udtryk er:

.. math::
   k_{n}=k_{\mathrm{start}}\left(1+r\right)^{n}+k_{\mathrm{måned}}\sum_{l=1}^{n}\left(1+r\right)^{l}

Det vides at den geometriske serie er givet ved:

.. math::
   \sum_{l=0}^{n-1}x^{l}=\left(\frac{1-x^{n}}{1-x}\right)

Denne kan skrives om til:

.. math::
   \sum_{l=1}^{n}x^{l}=\left(\frac{1-x^{n}}{1-x}\right)-1+x^{n}
   
Ved at sætte :math:`x=1+r` findes det at:

.. math::
   k_{n} = k_{\mathrm{start}}\left(1+r\right)^{n} + k_{\mathrm{måned}}\left(\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1 + \left(1+r\right)^{n}\right)
   :label: opsparing
   

   
Årlig rente til månedelig rente
-------------------------------

Hvis renten over :math:`n` perioder skal kendes for at renten vil være den samme som givet over et år skal det følgende løses:

.. math::
   \left(1+r_{n}\right)^{n}=\left(1+r\right)
   
Med :math:`r` værende renten, og :math:`r_{n}` værende renten spredt ud over :math:`n` perioder.
   
Herved bliver:

.. math::
   r_{n}=\left(1+r\right)^{1/n}-1
