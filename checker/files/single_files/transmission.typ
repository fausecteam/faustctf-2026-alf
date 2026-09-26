#let title = "$title"
#let author = "$author"

#rect(width: 100%, inset: 14pt, radius: 5pt, stroke: 1.2pt)[
  #align(center)[
    #set text(size: 22pt, weight: "bold")
    #title
  ]
  #v(4pt)
  #align(right)[
    #set text(size: 11pt, style: "italic")
    // encoded and relayed across the dark by #author
    Relayed by #author
  ]
]

#v(1cm)

= Frame 001 — Hail
#text("$chap1")

= Frame 002 — Payload
#text("$chap2")

= Frame 003 — Sign-off
#text("$chap3")
