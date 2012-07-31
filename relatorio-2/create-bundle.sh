#!/bin/bash


analises="processos-por-categoria processos-por-tipo-de-corte \
          processos-por-uf-por-ano"

rm -rf bundle
mkdir bundle
for i in $analises; do
    echo "*** $i"
    cd $i
    ./gera_graficos.py
    mv graficos/ ../bundle/$i
    cd ..
done
tar -zcf bundle.tar.gz bundle
