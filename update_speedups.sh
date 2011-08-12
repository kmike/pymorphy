#!/bin/sh
cython -X boundscheck=True pymorphy/_morph.py -o speedups/_morph.c
