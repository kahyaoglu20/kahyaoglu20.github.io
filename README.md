# kahyaoglu20.github.io

Source of my portfolio site, served by GitHub Pages at **https://kahyaoglu20.github.io**.

The pages are static HTML generated from one content file:

```
_build/content.py     every sentence, project, metric and link on the site
_build/build.py       renders index.html and projects/<slug>/index.html
assets/css/site.css   the stylesheet (light and dark)
assets/js/site.js     theme toggle, navigation, lightbox, the X = L + S hero animation
assets/img/           figures and screenshots (WebP)
assets/papers/        manuscripts and reports (PDF)
projects/             project pages, plus two hosted interactive documents
```

To change the site, edit `_build/content.py`, then run:

```bash
python _build/build.py
```

No framework, no build dependencies beyond Python 3.

© 2026 Ömer Kahyaoğlu. All rights reserved for the text, figures and documents.
