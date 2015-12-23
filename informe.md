TP InfoVis ITBA - Big Data 2015/2
-----------------------------------

* Autor: Ignacio Peluffo
* [ipeluffo@gmail.com](mailto:ipeluffo@gmail.com)
* [Github](https://www.github.com/ipeluffo)

# Descubriendo eventos excepcionales

## Objetivo

El objetivo principal del trabajo práctico consistió en hacer un procesamiento de los datos para luego hacer visualizaciones de manera eficiente.

Con las visualizaciones realizadas, la meta era encontrar si en el dataset podían detectarse comportamientos de búsquedas fuera de lo convencional, para luego intentar hacer un análisis de la posible razón de los mismos.

## Procesamiento de la información

El procesamiento del dataset brindado para la realización del trabajo práctico se dividió en tres etapas.

### Primera etapa de procesamiento

En la primera etapa del procesamiento de datos, el objetivo fue encontrar las búsquedas (compuestas de una latitud y longitud) que fueran únicas y la cantidad de veces que aparece en el dataset.

Utilizando [Apache Spark](https://en.wikipedia.org/wiki/Apache_Spark), un framework para cómputo distribuido, se realizó el procesamiento del dataset original para detectar la cantidad total de búsquedas para cada combinación de latitud y longitud únicas en el dataset.

La implementación de este procesamiento se puede ver en [ProcessSearchedPlacesByCount.scala](https://github.com/ipeluffo/InfoVisDataProcessing/blob/master/src/main/scala/ipeluffo/ProcessSearchedPlacesByCount.scala).

Este script, implementado utilizando Scala como lenguaje de programación, tiene la ventaja que puede ejecutarse fácilmente con datasets de cualquier tamaño en un cluster para hacer un procesamiento paralelo de manera más eficiente y rápida.

Una vez ejecutado el script con el dataset original, la salida contendra el listado de pares de latitud y longitud únicos ordenados por la cantidad de veces que aparecen.

Por ejemplo, las primeras diez combinaciones que más se repiten son:

```
1. -58.462533043214712,-34.555480273340216,5866
2. -58.456693312239103,-34.562035632676761,5268
3. -58.415951157589191,-34.58515196888407,4420
4. -58.436456844987347,-34.618300699103081,3706
5. -58.442150657451087,-34.579703319951435,3527
6. -58.39331196149918,-34.595863030826337,3350
7. -58.380955935561197,-34.604036535260882,3189
8. -58.392286335032786,-34.604436079428034,2785
9. -58.402347871304684,-34.594442849219298,2753
10. -58.416099219248636,-34.625437403806465,2716
```

### Segunda etapa de procesamiento: Georeferencia inversa

Con el procesamiento realizado en la primera etapa, se procedió a utilizar un servicio web de georeferenciamiento inverso para obtener la información sobre la esquina más próxima a cada una de las búsquedas. Esto permitiría luego mostrar las búsquedas con los nombre de las calles además de la latitud y la longitud.

El servicio web utilizado para obtener los nombres de las calles de la intersección buscada fue [GeoNames](http://www.geonames.org/). Más precisamente, el webservice (WS) utilizado fue [findNearestIntersectionOSM](http://www.geonames.org/maps/osm-reverse-geocoder.html#findNearestIntersectionOSM).

Para procesar el dataset y obtener la información del WS, se desarrolló un script en Python: [cornersMapping.py](https://github.com/ipeluffo/itba-infovis-2015/blob/master/cornersMapping.py) 

Una vez obtenida la información de las esquinas, se generó un dataset enriquecido de información.

A cotinuación se pueden ver las diez primeras entradas del dataset generado:

```
1. -58.462533043214712,-34.555480273340216,5866,-58.4625104,-34.5555029,Av. Cabildo,Av. Congreso
2. -58.456693312239103,-34.562035632676761,5268,-58.4566839,-34.5620541,Av. Cabildo,Av. Juramento
3. -58.415951157589191,-34.58515196888407,4420,-58.4159601,-34.5851406,Av. Santa Fe,Av. Raúl Scalabrini Ortiz
4. -58.436456844987347,-34.618300699103081,3706,-58.4364584,-34.6182756,Av. José María Moreno,Av. Rivadavia
5. -58.442150657451087,-34.579703319951435,3527,-58.4415663,-34.5800319,Zapiola,Av. Dorrego
6. -58.39331196149918,-34.595863030826337,3350,-58.393271,-34.5958568,Av. Santa Fe,Av. Callao
7. -58.380955935561197,-34.604036535260882,3189,-58.38090988138305,-34.604061911603495,Av. Presidente Roque Sáenz Peña,Carlos Pellegrini
8. -58.392286335032786,-34.604436079428034,2785,-58.3922779,-34.6044056,Av. Callao,Avenida Corrientes
9. -58.402347871304684,-34.594442849219298,2753,-58.402398,-34.59446,Av. Santa Fe,Av. Pueyrredón
10. -58.416099219248636,-34.625437403806465,2716,-58.4160807,-34.6254619,Av. Boedo,Av. San Juan
```

### Tercera etapa de procesamiento: Mapeo y sumarización de esquinas

La tercera y última etapa del procesamiento consistió en mapear las búsquedas que se relacionaban con las mismas esquinas y sumarizarlas por día y hora.

De igual forma que la primera etapa, se utilizó [Apache Spark](https://en.wikipedia.org/wiki/Apache_Spark) para hacer el procesamiento de la información dado el tamaño de los datasets y la facilidad de la API de Spark para manipular información con gran cantidad de datos.

El código fuente del algoritmo realizado para hacer el procesamiento se puede encontrar en [FinalDataProcessing.scala](https://github.com/ipeluffo/InfoVisDataProcessing/blob/master/src/main/scala/ipeluffo/FinalDataProcessing.scala). El código fue detalladamente comentado para comprender cada etapa del procesamiento.

El dataset que resulta de este procesamiento contiene la fecha y hora de búsqueda, información de la esquina como la latitud, longitud y el nombre de las calles que se intersectan. Además contiene la sumarización de la cantidad de veces que esa esquina fue buscada en la misma fecha y hora para luego hacer más ágil la visualización de la información y disminuir la carga de procesamiento de la herramienta utilizada.

Observar que la hora fue mapeada a la hora sin considerar los minutos y segundos para obtener una cantidad mayor de búsquedas para la misma hora.

Finalmente, a continuación se pueden ver las diez esquinas más buscadas y la cantidad para cada caso.

```
1. 2014-08-05 17:00:00,-58.4352783,-34.5696592,Baez y Teniente Benjamín Matienzo,1789
2. 2014-08-05 16:00:00,-58.4352783,-34.5696592,Baez y Teniente Benjamín Matienzo,377
3. 2014-07-30 22:00:00,-58.4090392,-34.5875775,Av. Coronel Díaz y Beruti,193
4. 2014-08-13 11:00:00,-58.4415663,-34.5800319,Av. Dorrego y Zapiola,147
5. 2014-08-13 10:00:00,-58.4415663,-34.5800319,Av. Dorrego y Zapiola,141
6. 2014-07-30 10:00:00,-58.4630645,-34.586898,14 de Julio y Iturri,139
7. 2014-07-30 09:00:00,-58.4630645,-34.586898,14 de Julio y Iturri,139
8. 2014-08-13 23:00:00,-58.4160807,-34.6254619,Av. Boedo y Av. San Juan,120
9. 2014-08-05 16:00:00,-58.3889738,-34.6155965,México y Virrey Cevallos,105
10. 2014-07-30 11:00:00,-58.4630645,-34.586898,14 de Julio y Iturri,102
```


## Visualizaciones y análisis

<!-- -->
<script type='text/javascript' src='https://public.tableau.com/javascripts/api/viz_v1.js'></script>
<!-- --->

Una vez realizado el procesamiento de la información siguiendo los tres pasos explicados anteriormente, el objetivo era visualizar la información con el objetivo de encontrar comportamientos de búsquedas que se salieran de lo normal.

Para la visualización de la información se utilizó exclusivamente la herramienta [Tableau](http://www.tableau.com/) y el dataset procesado y enriquecido de información.

### Visualización 1

Primeramente, se implementó una visualización de un mapa de calor (*heatmap* en Inglés).

La visualización fue configurada de la siguiente manera:

* El eje horizontal representa los días.
* El eje vertical representa las horas.
* El color de cada momento esta dado por la suma de cantidad de búsquedas de todas las esquinas en ese día y horario.

De esta manera se obtuvo la siguiente visualización:

<!-- -->
<div class='tableauPlaceholder' style='width: 2048px; height: 742px;'><noscript><a href='#'><img alt='Sheet 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;IT&#47;ITBA-InfoVis-2015-01&#47;Sheet1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz' width='982' height='742' style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='site_root' value='' /><param name='name' value='ITBA-InfoVis-2015-01&#47;Sheet1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;IT&#47;ITBA-InfoVis-2015-01&#47;Sheet1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='showVizHome' value='no' /><param name='showTabs' value='y' /><param name='bootstrapWhenNotified' value='true' /></object></div>
<!---->

De manera inmediata, se pueden sacar las siguientes conclusiones del dataset:
* El dataset contiene datos a partir de las 6 hs del 27/7/14 hasta las 15 hs del 15/8/14.
* Hay un comportamiento muy similar respecto a los días de semana y la franja horaria entre las 8 y las 19 hs.
* El 13 de Agosto a las 11 hs se hizo una cantidad de búsqueda claramente mayor a cualquier otro día y horario.

Dado que el objetivo del proyecto era encontrar búsquedas fuera de lo convencional, el último punto descripto del análisis de la visualización era un candidato a seguir investigando.


### Visualización 2

Gracias a la primera visualización, se prosiguió a construir una segunda visualización que nos diera más información sobre ese día y hora en el que se hizo la mayor cantidad de búsquedas entre todos los demás días y horarios.

Así es que se decidió realizar un gráfico de barras horizontales donde se representaba:

* En el eje horizontal la cantidad de búsquedas.
* En el eje vertical las esquinas buscadas.
* El gráfico se filtró a las 35 esquinas más buscadas, y al día 13/8 a las 11 hs como se vió en la anterior visualización.

Una vez determinado los parámetros de la visualización, se obtuvo el siguiente gráfico de barras:

<!---->
<div class='tableauPlaceholder' style='width: 982px; height: 742px;'><noscript><a href='#'><img alt='Sheet 2 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;IT&#47;ITBA-InfoVis-Visualizacin2&#47;Sheet2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz' width='982' height='742' style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='site_root' value='' /><param name='name' value='ITBA-InfoVis-Visualizacin2&#47;Sheet2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;IT&#47;ITBA-InfoVis-Visualizacin2&#47;Sheet2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='showVizHome' value='no' /><param name='showTabs' value='y' /><param name='bootstrapWhenNotified' value='true' /></object></div>
<!---->

Al setear los parámetros, el resultado esperado era encontrar esquinas con muchas búsquedas pero con cantidades similares.
Sorpresivamente, la esquina de Av. Dorrego y Zapiola superaba ampliamente al resto de las esquinas en cantidad de búsquedas.

A pesar de este resultado, aún se desconocía si esta esquina era regularmente buscada por encima de otras esquinas. Por esto, se decidió a armar una tercera visualización.

### Visualización 3

Para la tercera y última visualización, se optó por crear nuevamente un mapa de calor con las siguientes características:

* Se utilizaron los mismos parámetros que la primera visualización.
* Se filtraron las esquinas para solo mostrar la esquina a estudiar de Av. Dorrego y Zapiola.

Una vez seteados todos los parámetros, se obtuvo la siguiente visualización mediante Tableau:

<!-- -->
<div class='tableauPlaceholder' style='width: 982px; height: 742px;'><noscript><a href='#'><img alt='Sheet 3 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;IT&#47;ITBA-InfoVis-Visualizacin3&#47;Sheet3&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz' width='982' height='742' style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='site_root' value='' /><param name='name' value='ITBA-InfoVis-Visualizacin3&#47;Sheet3' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;IT&#47;ITBA-InfoVis-Visualizacin3&#47;Sheet3&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='showVizHome' value='no' /><param name='showTabs' value='y' /><param name='bootstrapWhenNotified' value='true' /></object></div>
<!---->

Gracias a esta visualización, se pudo rechazar la hipótesis de que la esquina era regularmente buscada.
Luego, haciendo un análisis del gráfico se desprende que la esquina de Av. Dorrego y Zapiola fue muy buscada durante todo el 13 de Agosto, 
pero mayorítariamente entre las 10 y 11 hs reforzando lo encontrado en la primera visualización.

La pregunta que quedaba contestar es qué había pasado el 13 de Agosto entre las 10 y 11 hs en la esquina de Av. Dorrego y Zapiola.

## Resultados

Haciendo una rápida búsqueda en Google filtrando por fecha: [Búsqueda en Google](https://www.google.com/search?q=av.+dorrego+y+zapiola&biw=1680&bih=928&source=lnt&tbs=cdr%3A1%2Ccd_min%3A8%2F13%2F2014%2Ccd_max%3A8%2F13%2F2014&tbm=)

Se encontraron los siguientes artículos:

* [Misión Solidaria de Metro 9.51](http://www.buendiario.com/evento/mision-solidaria-de-metro-9-51/)
* [Desfile de diseñadores emergentes ¡Retirá tus entradas gratuitas!](http://agendacultural.buenosaires.gob.ar/evento/desfile-de-disenadores-emergentes-retira-tus-entradas/9951)

Como se puede observar, el primer artículo hace referencia a un evento especial de Misión Solidaria realizado por la radio Metro exactamente en la esquina de Av. Dorrego y Zapiola entre 6 y las 20 hs.
De esta manera, se pudo encontrar la razón detras de la cantidad significativa y diferenciadora de búsquedas que se hicieron el 13 de Agosto.

El segundo artículo hace mención a la entrega de entradas para otro evento en el mismo lugar. Sin embargo, este artículo no podría tomarse como la razón detras del hecho encontrado en el análisis de las visualizaciones.

De esta manera, se puede concluir que el procesamiento, visualización y posterior análisis sirvió para encontrar al menos un 
momento en el que se hizo una cantidad de búsquedas de manera anormal y la explicación detrás de ello, es decir, un evento excepcional
como se planteó como objetivo del proyecto.