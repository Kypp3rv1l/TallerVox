#!/usr/bin/env python3
"""Aplica reeditar.py a todo el catalogo (salvo ruinas y el ejemplo). Uso: reeditar_todo.py [carpeta_estructuras]"""
import sys, os, json, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reeditar import procesar, escribir
SALTAR = ('ejemplo_caseta', 'casa_2_plantas_1', 'edificio_medieval_2', 'salon_2_plantas_1', 'salon_2_plantas_3')   # ruinas / casos especiales
NOTA = ' [v0.1.4: ventanas y chimenea segun la Taberna v1]'
carpeta = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogo', 'estructuras')
for fn in sorted(glob.glob(os.path.join(carpeta, '*.json'))):
    nombre = os.path.basename(fn)[:-5]
    if nombre in SALTAR or nombre.startswith('taberna'):
        print('salto', nombre); continue
    d = json.load(open(fn))
    if NOTA in d.get('description', ''):
        print('ya hecha', nombre); continue
    c, rep = procesar(d, nombre + '.json')
    print('\n'.join(rep))
    d['description'] = d.get('description', '') + NOTA
    escribir(c, d, fn)
