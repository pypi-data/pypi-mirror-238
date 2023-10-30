# ThorpyWebsite (c) Yann Thorimbert 2023

How to generate site :
* Set the root for Thorpy in generate_website.py
    For thorpy's core code, I copy/paste all the code from site-packages/thorpy to ../Thorpy2.
    For the examples, it's often in ../Thorpy2. Be careful to use the right folder in any case !
* Copy-paste the actual thorpy folder to ./thorpy/
    Attention /!\ : j'ai dû c/c aussi dans ./thorpy pour que ça marche...
* Run generate_website.py

How to update elements :
* Nothing special to do for the doc description, it is automatic as long as you indicate things in docstrings
* For the image, put an image with the same name as the class (but lowercase) in the doc folder
* For the examples, don't forget to add tags so that it is referenced. This also includes adding the name of the function or the class to which you want to point from the doc section.

Files to upload to server:
* All things inside to_upload/ should be sent to ftp.thorpy.org/httpdocs/
Cl1_-whfam_v, _ est trinité


Upload on PyPi :
1. Change version number in both setup.py AND thorpy/__init__.py (and dont forget the actual thorpy git !)
2. Copy paste the actual thorpy folder (on my computer its 'Thorpy2') to ./thorpy/
3. pip install twine setuptools wheel
4. python setup.py sdist bdist_wheel
5. twine upload dist/* (without 2FA) : Account : Thorpy, Pwd : Don't worry
5. twine upload -u __token__ -p my_token dist/*



***TODO***

cursor resize marche pas
Documentation pour les attributs de style (set_style("border_thickness", 1) n'est pas inné ! )

# versions + tard: ####################################################################
#TODOs
#script de tutos auto basé sur les commentaires
# detecter quels examples figurent pas dans les automatiquement proposes et faire un systeme de tags bijectifs
#lifebar vertical
# site : quand on hover un element de code d'example, un encart qui explique ce qu'est l'élément apparait
# offset du style pour effet d'appui
# flash du DDL : a cause de launch_nonblocking=True
# gen oscillating lights et autres ==> a ranger dans la lib, fair un truc du style:
# my_element.fx.add_oscillating_light(...)
# my_element.fx.add_shadow(...)
# my_element.fx.add_particle_emission(...)
# my_element.fx.add_bloom(...)
# bloom https://www.youtube.com/watch?v=ml-5OGZC7vE
#masque pour appliquer degradé sur polygone
#hyphenize autocut line
#life heart tout faits (arg : img_full and img_empty)
#TODO: inclure thornoise, et utiliser pour joli animations electriques ainsi que pour generer un fond de nuages pour exemples
#include les autre utils de thorpy
#TODO: thorpypack --> thorpy, thornoise, thorphys, thorpyfx
#miscgui du vieux thorpy ==> HUD
# * slider with text vertical ; teleport dragger of slider at click
#text input on focus : option de delete ancien contenu dès l'écriture du nouveau (comme un ctrl+A)
#shadowgen optimises pour les round rect
#texte riche peut etre augmente en changeant les attributs de font (font, fontsize, antialias, bold, italic) (prochaine version)
#italic et gras marchent que quand on appelle manuellement set_default_font()