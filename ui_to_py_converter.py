# -*- coding: utf-8 -*-
"""
Created on Wed May 17 13:28:48 2023

@author: MONSTER
"""

from PyQt5 import uic
 
with open('kitapListesiUI.py', 'w', encoding="utf-8") as fout:
   uic.compileUi('kitapListesi.ui', fout)
""" 
with open('loginUI.py', 'w', encoding="utf-8") as fout:
   uic.compileUi('login.ui', fout)

with open('personelEkraniUI.py', 'w', encoding="utf-8") as fout:
   uic.compileUi('personelEkrani.ui', fout)"""