Repo per la tesi di Samuel Brandão.

Note a Bellettini e Paolo: vi ho dato anche accesso di scrittura, 
in modo che se vi viene da fare commenti o note potete pure farlo direttamente sul codice.

Il PDF Non sempre riflete l'ultima versione compilata (aggiungo una nuova versione compilata solo 
quando penso di aver raggiunto un punto specifico), 
vi prego di riferirsi al sorgente tex per correzioni. Ho cercato di indicare esplicitamente le parti
che sono cosciente richiedano più tempo.

####BELLETTINI: 

infatti non avresti dovuto proprio inserirlo il file PDF, in quanto file "generato".

Per congelare delle versioni binarie dovresti:

    git checkout -b temp
    git add tesi.pdf
    git commit -m "versione ... "
    git tag "xxx"   <<<  quello che vuoi
    git checkout master
    git branch -D temp

In questo modo sono richiamabili le varie versioni congelate (consegnate, stampate, etc etc), ma non disturbano il ramo master

