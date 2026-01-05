```py
equi = Image.open("panorama.jpg")
faces = cubemap_faces(equi, 512)

for k, img in faces.items():
    img.save(f"{k}.png")
```