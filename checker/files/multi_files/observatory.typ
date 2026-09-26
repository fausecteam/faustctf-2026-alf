#set page(columns: 1, numbering: "— 1 —")
#set heading(numbering: "I.")
#let title = "$title"
#let author = "$author"

#align(center)[
  #set text(size: 24pt, weight: "bold")
  #title
  #v(4pt)
  #set text(size: 11pt, weight: "regular")
  Deep-Space Observatory Report · Principal Observer: #author
]

#line(length: 100%, stroke: 0.7pt)
#v(0.5cm)

= Observation
#text("$chap1")

#figure(
  image("image.jpg", width: 85%),
  caption: [Long-exposure plate from the primary array.],
)

= Analysis
#text("$chap2")

= Conclusions
#text("$chap3")
