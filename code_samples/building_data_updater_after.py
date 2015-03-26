self.batch_date = datetime.now()

for b_data in buildings:
  if not self._validate_building_data(b_data):      # Step 1 - Righe 5-15 
    continue                                        # dell'originale

  building = self.find_building_to_update(b_data)   # Step 2 - Righe 20-23
  self._mark_building_as_updated(building)          # Step 3 - Righe 26-28

  with Logger.info("Processing "+str(building)):
    self._update_a_building(building, b_data)       # Step 4 - Righe 31-37

self._destroy_unmarked_buildings()                  # Step 5 - Righe 41-51
