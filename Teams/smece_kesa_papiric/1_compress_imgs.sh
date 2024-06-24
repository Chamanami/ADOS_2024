#!/bin/bash

# TODO Python script.

IMG_DIR=/home/bazina/ADOS_2024/Teams/smece_kesa_papiric/dataset/images/train
TMP_DIR="$IMG_DIR/tmp"

# Promena dozvola za sve slike
chmod u+rw "$IMG_DIR"/*.jpg

# Kreiraj privremeni direktorijum
mkdir -p "$TMP_DIR"

# Logovanje - Prikaz slika koje će biti kompresovane
echo "Pronalazim slike u $IMG_DIR:"
find "$IMG_DIR" -name '*.jpg'

# Pronađi i kompresuj slike
find "$IMG_DIR" -name '*.jpg' -exec sh -c '
for img; do
    echo "Kompresujem: $img"
    convert "$img" -resize 640x480 "'"$TMP_DIR"'"/$(basename "$img")
done
' sh {} +

# Proveri da li su slike uspešno kompresovane
if [ "$(ls -A "$TMP_DIR")" ]; then
    # Logovanje - Prikaz kompresovanih slika
    echo "Kompresovane slike:"
    ls -l "$TMP_DIR"

    # Obriši originalne slike
    rm "$IMG_DIR"/*.jpg

    # Premesti kompresovane slike nazad u originalni direktorijum
    mv "$TMP_DIR"/*.jpg "$IMG_DIR"
else
    echo "Nema slika za kompresovanje u $IMG_DIR."
fi

# Obriši privremeni direktorijum
rmdir "$TMP_DIR"

