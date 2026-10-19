-- Deliberately small, synthetic example; NOT actual Portuguese station data.
INSERT INTO stations (station_id, station_name, basin, country) VALUES
 (1, 'Almourol (synthetic)', 'Tejo', 'Portugal'),
 (2, 'Abrantes (synthetic)', 'Tejo', 'Portugal'),
 (3, 'Acude Ponte Coimbra (synthetic)', 'Mondego', 'Portugal');

INSERT INTO daily_flow (station_id, observed_date, flow_m3s) VALUES
 (1,'2026-01-01',75),(1,'2026-01-02',80),(1,'2026-01-03',95),
 (1,'2026-01-04',110),(1,'2026-01-05',100),(1,'2026-01-06',90),(1,'2026-01-07',88),
 (2,'2026-01-01',55),(2,'2026-01-02',57),(2,'2026-01-03',70),
 -- 2026-01-04 is intentionally missing for station 2.
 (2,'2026-01-05',85),(2,'2026-01-06',80),(2,'2026-01-07',75),
 (3,'2026-01-01',22),(3,'2026-01-02',24),(3,'2026-01-03',26),
 (3,'2026-01-04',28),(3,'2026-01-05',27),(3,'2026-01-06',25),(3,'2026-01-07',24);

INSERT INTO daily_weather (basin, observed_date, rainfall_mm) VALUES
 ('Tejo','2026-01-01',0),('Tejo','2026-01-02',1),('Tejo','2026-01-03',12),
 ('Tejo','2026-01-04',18),('Tejo','2026-01-05',4),('Tejo','2026-01-06',0),('Tejo','2026-01-07',2),
 ('Mondego','2026-01-01',0),('Mondego','2026-01-02',0),('Mondego','2026-01-03',4),
 ('Mondego','2026-01-04',7),('Mondego','2026-01-05',2),('Mondego','2026-01-06',1),('Mondego','2026-01-07',0);
