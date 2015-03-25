namespace = self.get_namespace() # get_namespace e' definito dalle sottoclassi
batch_date = datetime.now()      # Tutti palazzi aggiornati devono avere
                                 # il campo "updated_at" con lo stesso valore
for b in buildings:
  b_id = b.get("b_id", "")       # variabili temporanee, aggiungono stati intermedi
  l_b_id = b.get("l_b_id", "")   
 
  # Step 1 - validazioni iniziali e segnalazione eventuali problemi
  if not Building.is_valid_bid(b_id):              # Validazione ID di palazzo
    if Building.is_valid_bid(l_b_id):              # Tentattivo di risoluzione errori
      Logger.warning("Legacy Id will be used ...") # Segnalazione: inconsist. risolta
      b["b_id"] = l_b_id                           # (messaggio truncato)
    else:                                          
      Logger.error([String multiline omessa])      # Segnalazione: dati invalidi
      continue                                     # Questo palazzo non va aggiornato
 
  # Step 2 - Queste quattro righe trovano nel DB il documento da aggiornare o creano
  # un nuovo oggetto di tipo Building da venir inserito. Namespaced_attr si riferisce
  # alla parte del documento relativa alla sorgente attuale (easyroom o edilizia)
  building = self.find_building_to_update(b)    
  namespaced_attr = building.get(namespace, {})  
  building[namespace] = namespaced_attr
  namespaced_attr.update(b)             # aggiornamento dei dati di questa sorgente

  # Step 3 - primo passo della politica di snapshot (garantire che palazzi non 
  # contemplati in questo aggiornamento vengano rimossi se necessario)
  deleted_key = "deleted_" + namespace
  if deleted_key in building:
    del building[deleted_key]
 
  # Step 4 - richiesta di integrazione delle sorgenti gia' presenti in DB
  # e salvataggio
  with Logger.info("Processing "+str(building)):
    building['merged'] = DataMerger.merge_building(
      building.get('edilizia'), building.get('easyroom'), building.get('dxf')
    )
    building['updated_at'] = batch_date           # Definizione della data dell'ultimo
    namespaced_attr["updated_at"] = batch_date    # Aggiornamento sul documento
    building.save()                               # Invio al Database dei dati aggior.
 
  # Step 5 - Secondo passo della politica di snapshot, rimuovere dal database
  # palazzi non piu' esistenti
  n_removed, b_removed = Building.remove_untouched_keys(namespace, batch_date)
  b_removed = [ b["b_id"] for b in b_removed ]
 
  if b_removed:
    Logger.info(n_removed, "previously existing buildings are not present...")
 
  n_destroyed, b_destroyed  = Building.remove_deleted_buildings()
  b_destroyed        = [ b["b_id"] for b in b_destroyed ]
  if n_destroyed:
    Logger.info(n_destroyed, "buildings were effectively removed...") 