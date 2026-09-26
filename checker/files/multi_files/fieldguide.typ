#set page(numbering: "1")
#set heading(numbering: "1.")
#let title = "$title"
#let author = "$author"

#align(center)[
  #set text(size: 25pt, weight: "bold")
  #title
  #v(6pt)
  #set text(size: 12pt, weight: "regular")
  A Xenobiology Field Guide, compiled by #author
]

#v(0.6cm)
#figure(
  image("image.jpg", width: 70%),
  caption: [Specimen recorded in situ.],
)
#v(0.6cm)

= Habitat
#text("$chap1")

= Behaviour
#text("$chap2")

= Field Notes
#text("$chap3")
