#set page(width: auto, height: auto, margin: 16pt, fill: none)
#set text(font: "Bernard MT", size: 44pt)
#set text(fill: rgb("#d9a566"))
#let s(body) = text(size: 14pt, body)
#let cap(c) = text(fill: rgb("#7ed957"), stroke: 0.4pt + rgb("#ffffff"))[#c]

#box[#cap[A]#h(0.04em)#box[#s[lien]]#h(-0.30em)#box(baseline: -0.3em)[#h(-0.16em)#cap[L]]#h(-0.08em)#box(baseline: -0.84em)[#s[anguage]]#h(-0.96em)#box(baseline: 0.12em)[#cap[F]]#h(0.04em)#box(baseline: -0.32em)[#s[ormatter]]]
