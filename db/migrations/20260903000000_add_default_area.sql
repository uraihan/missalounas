--migrate:up
UPDATE cities SET default_area = 'Hervanta' WHERE name = 'Tampere';
UPDATE cities SET default_area = 'Keskusta' WHERE name = 'Helsinki';
UPDATE cities SET default_area = 'UTU Kampus' WHERE name = 'Turku';
--migrate:down
