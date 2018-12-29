SELECT 
  categorie_activite.nom, 
  activite.date, 
  activite.heure_debut, 
  activite.heure_fin 
FROM inscription 
LEFT JOIN activite 
  ON inscription.id_activite = activite.id_activite 
LEFT JOIN categorie_activite 
  ON activite.id_categorie_activite = categorie_activite.id_categorie_activite 
WHERE 
  (inscription.id_participante = :id_participante) 
  AND (activite.date >= :current_date) 
  AND (inscription.status = :status) 
  AND (activite.status = 1)
ORDER BY categorie_activite.nom ASC, activite.date ASC