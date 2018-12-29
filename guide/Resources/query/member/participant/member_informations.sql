SELECT 
  actif, 
  numero_membre, 
  membre_honoraire, 
  date_renouvellement 
FROM 
  membre 
WHERE 
  id_participante = :id_participante