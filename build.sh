#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Copy product images from static/images to media/ so they are served correctly
echo "Copying images to media folder..."
mkdir -p media
for folder in Earrings Chains Bracelet Mangalsutra Rings Watch; do
    if [ -d "static/images/$folder" ]; then
        cp -r "static/images/$folder" "media/"
        echo "  Copied $folder"
    fi
done
echo "Images copied successfully."

# Fix double-space filename issue in Chains folder
if [ -f "media/Chains/Chain  16.jpeg" ]; then
    cp "media/Chains/Chain  16.jpeg" "media/Chains/Chain 16.jpeg"
    echo "  Fixed Chain 16 filename"
fi

python manage.py seed_data
