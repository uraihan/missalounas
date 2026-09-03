--migrate:up
ALTER TABLE cities ADD COLUMN default_area TEXT; --TODO: remove this in prod
UPDATE cities SET default_area = 'Hervanta' WHERE name = 'Tampere';
UPDATE cities SET default_area = 'Keskusta' WHERE name = 'Helsinki';
UPDATE cities SET default_area = 'UTU Kampus' WHERE name = 'Turku';
--migrate:down
