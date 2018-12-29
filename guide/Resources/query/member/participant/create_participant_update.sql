UPDATE participante
SET
  appellation = :appellation,
  prenom = :prenom,
  nom = :nom,
  adresse_1 = :adresse_1,
  adresse_2 = :adresse_2,
  ville = :ville,
  province = :province,
  code_postal = :code_postal,
  courriel = :courriel,
  telephone_1 = :telephone_1,
  poste_telephone_1 = :poste_telephone_1,
  telephone_2 = :telephone_2,
  poste_telephone_2 = :poste_telephone_2,
  date_naissance = :date_naissance,
  personne_nourrie = :personne_nourrie,
  consentement_photo = :consentement_photo
WHERE
  id_participante = (SELECT id_participante
                     FROM participante
                     WHERE prenom = :prenom AND nom = :nom AND telephone_1 = :telephone_1)