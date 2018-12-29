SELECT 
  facture.date, 
  article.description, 
  article.prix 
FROM facture 
INNER JOIN article ON article.id_facture = facture.id_facture 
WHERE facture.id_participante = :id_participante