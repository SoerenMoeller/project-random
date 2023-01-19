# project-random
The goal is to create a video involving science communication. We are using [3Blue1Brown](https://www.youtube.com/@3blue1brown)s work as inspiration. 

---

## Framework: 
Using the [Python](https://www.python.org/) library [Manim](https://github.com/ManimCommunity/manim/) for the animations.  

## Video idea:
The main topic is "randomness" in computer systems. 
- What is "random"
- Use cases
- How are computers creating it? (example)
- Is this a usefull approach for all use cases?
- True random number generators

## Script:  
- Cold Opener

> Einschub: Existiert echter Zufall?

Computer sind dafür konstruiert, deterministisch (also vorhersehbar) zu arbeiten. 
Das ist wichtig, da Berechnungen im allgemeinen präzise sein sollen und die Korrektheit 
dieser nicht variieren soll. (Beispiel angeben)

Ein wichtiges Konzept für beispielsweise Spiele, Algorithmen und insbesondere der Kryptographie 
ist der Zufall und im speziellen Zufallszahlen. Wie kann allerdings diese deterministische
Architektur eines Computers, echte Zufallswerte generieren?

Während es verschiedene Konzepte gibt um Zufallszahlen zu generieren, haben die meisten die Eigenschaft gemein,
arithmetik auf eine Eingabezahl anzuwenden um diese, in eine scheinbar zufällige Zahl umzuwandeln.

Beispiel angeben, zuerst Generator als Black-Box, dann auflösen.
Beschreiben, warum dieser nicht gut funktioniert, aber in die vorherige "Definition" passt.
Schwierigkeit beschreiben, Verfahren zu wählen ohne Zirkel oder Bias.

Besseres (Standard)-Verfahren vorstellen.

Seed in Fokus rücken, erklären (Minecraft Bezug?)
Ist das Verhalten gewünscht? Wann ist es das nicht?

"Auflösung": Das ist kein echter Zufall, sondern Pseudo-Zufall. Aber ist das schlimm?
Für welche Fälle, ist das nicht erwünscht? Wie kann man das reparieren?

True-Random-Number-Generators erwähnen. - Somit Architektur des Computers ändern.

Aussicht auf Zufalls-Themen:
- Quantencomputer
- Kryptographie
- Verbesserung von Algorithmen (oder auch Approximationen)
usw.
