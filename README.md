# PolyBot

Projecte per l'assignatura de Llenguatges de Programació (LP) de la FIB, Q1 2020-21. L'objectiu consisteix en:
1. Crear una classe per a manipular i representar polígons convexos.
2. Crear un llengüatge de programació (usant ANTLR) que faci ús de la classe per a treballar amb polígons convexos.
3. Implementar un Bot de Telegram que permeti als usuaris usar el llengüatge de programació definit per a treballar amb polígons convexos.

## Per a començar
S'han d'instal·lar les llibreries necessaries (es troben al fitxer ```requeriments.txt```):

```$ pip3 install -r requeriments.txt```

### Execució de la gramàtica
Si es vol probar el llenguatge de programació directament al PC, es pot fer de la següent manera:
1. Anar a la carpeta /cl.
2. Executar el fitxer ```script-parser.py```. L'entrada està definida per la terminal.
3. Si es vol veure el comportament del evaluador, executar el fitxer ```script-eval.py```. L'entrada és un fitxer de text que se li ha de passar com a paràmetre (hi ha un amb l'exemple de l'enunciat anomenat ```input.txt```). Exemple, en linux, de l'execució:

```$ python3 script-eval.py input.txt```

### Execució del bot de telegram
Si es vol usar el bot de Telegram, s'han de seguir aquests passos:
1. Instal·lar i registar-se a Telegram.
2. Anar a @BotFather.
3. Crear un nou bot amb la comanda /newbot i proporcionant la informació requerida.
4. Copiar el token en un fitxer anomenat ```token.txt``` i desar-lo a la carpeta /bot.
5. Executar el bot:

```$ python3 bot.py```

## Definició del llenguatge de programació
Aquest llenguatge de programació suporta les següents definicions:
- _var_ := _polígon_ ➡️ Asigna un polígon convex a una variable.            
- print _polígon_ OR "_text_" ➡️ printa un polígon o un text.            
- area _polígon_ ➡️ àrea del polígon.            
- perimeter _polígon_ ➡️ perímetre del polígon.            
- vertices _polígon_ ➡️ # de vèrtex del polígon.            
- centroid _polígon_ ➡️ centroid del polígon.            
- color var, _{0, 1, 0.5}_ ➡️ assigna un color al polígon de la variable.            
- inside _polígon1_, _polígon2_ ➡️ indica si el polígon 1 està a dintre del 2.            
- equal _polígon1_, _polígon2_ ➡️ indica si els dos polígons són iguals.            
- draw _output_, _polígons_ ➡️ dibuixa els polígons (seprarats per comes) en un fitxer output.            
- operacions ➡️ els polígons es poden operar per a formar nous polígons.            
    - _polígon1_ + _polígon2_ ➡️ unió convexa dels dos polígons.            
    - _polígon1_ * _polígon2_ ➡️ intersecció dels dos polígons.            
    - \# _polígon_ ➡️ bounding box del polígon.            
    - _!n_ ➡️ retorna un polígon convex format amb n punts random entre ([0,1]²).            

Per a definir un polígon es poden usar les operacions o indicant els punts en el format ```[x1 y1 x2 y2 ... xn yn]```.


## Implementació de la classe
La classe ```ConvexPolygon``` representa un poligon com una llista de punts (x, y) del convex hull del polígon. Aquesta llista no té punts repetits i està ordenada en contra de les agulles del rellotge (counterclockwise) començant pel punt que està més a l'esquerra (i, si hi ha empat, amb el que es troba més a baix en l'eix y). A més, cada instància té un color associat (per defecte és el negre).

Aquesta classe s'ha dividit en els següents apartats:
- *Auxiliar functions*: funcions auxiliars que es van utilitzant al llarg del programa.
- *Init class functions*: funció per instanciar un objecte de la classe a partir d'uns punts (que són processats amb convex hull per a obtenir la llista de punts que representa el polígon).
- *Getters functions*: funcions per obtenir atributs de la classe (com la llista de vèrtexs) o característiques del polígon (com l'àrea o el centoride).
- *Setters functions*: només hi ha una funció que actualitza el color associat al polígon.
- *Query functions*: funcions asociades a preguntar característiques del polígon. Per exemple, si aquest es regular, si un punt donat està dintre seu, si és igual a un altre polígon, etc.
- *Operation functions*: funcions per operar amb els polígons, que com a resultat creen nous polígons. Hi ha la intersecció, unió i bounding box.
- *Draw function*: funció dedicada a crear un objecte imatge d'una llista de polígons.

Totes les funcions del codi i el seu cost (si no es trivial) es troben comentades (en anglès).

## Implementació del llenguatge de programació
El LP s'ha creat usant ANTLR4. Tot el codi relacionat es troba a la carpeta /cl. La gramàtica està en el fitxer ```Expr.g4``` i l'avaluador d'aquesta en el fitxer ```EvalVisitor.py```. D'aquest últim fitxer cal destacar l'atribut diccionari de la classe, que s'encarrega de guardar les assignacions de polígons a variables en un diccionari. També cal destacar l'atribut buff, que indica si la imatge es guarda directament al sistema o en un buffer (per motius de seguretat).

## Implementació del Bot de Telegram
El bot de telegram es troba a la carpeta /bot. De la seva implementació cal destacar l'ús del diciconari ```context.user_data``` que serveix per desar informacions per l’usuari amb qui ens estem comunicant (aquest diccionari és diferent per a cada usuari amb qui el bot estigui comunicant-se). Amb l'objectiu de no perdre les assignacions durant la conversació amb un usuari, aquest diccionari es pasa per referència a la classe ```EvalVisitor``` que l'utilitza per a guardar les assignacions de polígons a variables. A més, l'atribut buff de la classe ```EvalVisitor``` es activat, així les imatges creades per la comanda ```draw``` es guarden en un buffer i no al sistema.

