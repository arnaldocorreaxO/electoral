SELECT * FROM electoral_ciudad


SELECT * FROM electoral_manzana

INSERT INTO electoral_ciudad VALUES (0,'NO DEFINIDO')

INSERT INTO electoral_manzana VALUES 
(1,0,'NO DEFINIDO',0),
(2,1,'LIC. JOSE PARADEDA',1),
(3,2,'DOMINGO BURGOS',1),
(4,3,'WILSON ARZAMENDIA',1),
(5,4,'FRANCISCO NARVAEZ',1),
(6,5,'BAR KO-EYU',1),
(7,6,'VICTOR RAMIREZ',1),
(8,7,'BARRILITO',1),
(9,8,'COSTANERA',1),
(10,1,'JORGE VILLALBA',2),
(11,2,'SANTIAGO OJEDA',2),
(12,3,'BERNARDINO BENITEZ ',2),
(13,4,'HECTOR RUIZ DIAZ',2),
(14,5,'EL TRIANGULO',2),
(15,1,'FEDERICO FERNANDEZ',3),
(16,2,'RELOJERIA ORIS',3),
(17,3,'OSVALDO GOMEZ',3),
(18,4,'GLADYS DE MIRANDA',3),
(19,5,'G-15',3),
(20,6,'RIVERA',3),
(21,1,'CASA DOMITILA',4),
(22,2,'FAUSTINO LEON',4),
(23,3,'SANTIAGO RAMIREZ',4),
(24,4,'GUILLERMO CORREA',4),
(25,5,'KARINA',4),
(26,6,'RAMON GUTIERREZ',4),
(27,7,'FRANCISCA VDA DE PUCHETA',4),
(28,8,'ICO RUIZ',4),
(29,9,'KAWASAKI',4),
(30,1,'EX-SALON 10',5),
(31,2,'LAS MELLIZAS',5),
(32,3,'ANTONIO FERREIRA',5),
(33,4,'EMILSON PORTILLO',5),
(34,5,'MIRTHA NARVAEZ',5),
(35,6,'DESPENSA PICAFLOR',5),
(36,1,'TETI BENITEZ',6),
(37,2,'LA NORTEÑITA',6),
(38,3,'MENDIETA',6),
(39,4,'MARIA VDA DE FERREIRA',6),
(40,5,'KAMBUCHI',6),
(41,6,'ARTURITO COMERCIAL',6),
(42,7,'ALFREDO ANDINO',6),
(43,8,'CATALINO FRANCO',6),
(44,9,'RUTILIO COLMAN',6),
(45,10,'KACHACA TROPICAL',6),
(46,11,'TEODORO ORTEGA',6),
(47,12,'HELADERIA DENISSE',6),
(48,13,'VICTOR RIOS',6),
(49,1,'COOPEMAVA',7),
(50,2,'IGLESIA',7),
(51,3,'RAMON DEL PILAR GOMEZ',7),
(52,4,'NARCISO ROMAN',7),
(53,5,'CASA NOLY',7),
(54,6,'ANASTACIO PALACIOS',7),
(55,7,'COMERCIAL KUARAHY',7),
(56,8,'COPACO',7),
(57,9,'OSVALDO BURGOS',7),
(58,10,'COMERCIAL OLY',7),
(59,11,'AUGUSTO ALVAREZ',7),
(60,12,'ARNALDO AVALOS',7),
(61,1,'CARPINTERIA SAN ISIDRO',8),
(62,2,'DESP. 13 DE MARZO',8),
(63,3,'ANGEL VALDEZ',8),
(64,4,'IRAN DUO',8),
(65,5,'CARLOS ZORRILLA',8),
(66,6,'TINA GONZALEZ',8),
(67,7,'VIDRERIA SAN MIGUEL',8),
(68,8,'LA MOVIDA',8),
(69,9,'GUILLERMO FERNANDEZ',8),
(70,1,'SANTIAGO VILLALBA',9),
(71,2,'ELEUTERIA DE BRITOS',9),
(72,3,'IPS',9),
(73,4,'SIXTO VERA',9),
(74,1,'CAPILLA PUEBLO DE DIOS',10),
(75,2,'ROPA USADA',10),
(76,3,'COSTADO DEL CEMENTERIO',10),
(77,1,'LA ECONOMIA',12),
(78,2,'ROSA SORIA CABALLERO',12),
(79,3,'ALEJANDRO ALCARAZ',12),
(80,4,'MEDICO',12),
(81,5,'MIRTA RUIZ DIAZ',12),
(82,1,'EX-HIPICO',13),
(83,2,'ANICIA GOMEZ',13),
(84,3,'P. QUIÑONEZ',13),
(85,1,'AVDA PRINCIPAL',14),
(86,2,'MIRADOR / ZUCAL',14),
(87,3,'CAMINO A SANTO DOMINGO',14),
(88,4,'EX-TORALES',14),
(89,1,'AVDA PRINCIPAL',15),
(90,2,'DETRAS DEL AEROPUERTO',15),
(91,3,'CAMINO A SANTA ELENA',15),
(92,4,'CAMINO A RIO APA',15),
(93,5,'CAMINO A COL. INDIGENA',15),
(94,1,'COL. INDIGENA - RIO APA',16),
(95,1,'LAS CARMELITAS',11),
(96,1,'WENCESLAO SILVANO',17),
(97,2,'ELADIO PONCE',17),
(98,1,'CAMINO A TRES CERROS',18),
(99,1,'RIACHO MOSQUITO',19),
(100,1,'SAN LAZARO',20),
(101,1,'TRES CERROS - MORADO',21),
(102,9,'MIGUEL KIM',1),
(103,1,'ÑATI-U RETIRO',22),
(104,4,'ISABELINO VILLALVA',13),
(105,2,'ZONA NORTE',21),
(106,3,'ZONA SUR',21),
(107,4,'ZONA CENTRO - CARLOS PALMA',21),
(108,5,'COSTANERA',21),
(109,1,'CERRO MORADO',23)


(0,'NO DEFINIDO',1),
(1,'SAN JOSE',1),
(2,'SAN JUAN',1),
(4,'CAACUPEMI',1),
(5,'SAN RAMON',1),
(6,'SAN ANTONIO',1),
(8,'SAN CARLOS',1),
(10,'SAN BLAS',1),
(11,'LAS CARMELITAS',1),
(12,'SAN MARTIN',1),
(13,'SAN GERARDO',1),
(17,'PAGANI',1),
(18,'CAMINO A TRES CERROS',1),
(19,'RIACHO MOSQUITO',1),
(20,'SAN LAZARO',1),
(22,'ÑATI-U RETIRO',1),
(3,'STA TERESITA',1),
(7,'Vº DE FATIMA',1),
(9,'Vº DE LORETO',1),
(14,'Sta ELENA',1),
(15,'Sto DOMINGO',1),
(16,'Col. INDIGENA',1),
(21,'TRES CERROS ',1),
(23,'CERRO MORADO',1)


SELECT * FROM padgral


UPDATE electoral_elector 
SET barrio_id = 
(SELECT cod_barrio FROM padgral 
WHERE numero_ced = electoral_elector.ci),

manzana_id = 
(
SELECT id FROM electoral_manzana 
WHERE cod = (SELECT cod_manzana FROM padgral 
				WHERE numero_ced = electoral_elector.ci)
AND barrio_id = 
				(SELECT cod_barrio FROM padgral 
				WHERE numero_ced = electoral_elector.ci)

),
nro_casa = (SELECT nro_casa FROM padgral 
WHERE numero_ced = electoral_elector.ci)





SELECT pasoxpc, COUNT(pasoxpc), pasoxmv, COUNT(pasoxmv) FROM electoral_elector 
WHERE pasoxpc = 'S' OR pasoxmv = 'S'
GROUP BY 1,3



SELECT * FROM security_module


SELECT "electoral_elector"."id", "electoral_elector"."departamento_id",
"electoral_elector"."distrito_id", "electoral_elector"."seccional_id",
"electoral_elector"."ci", "electoral_elector"."apellido", 
"electoral_elector"."nombre", "electoral_elector"."direccion",
"electoral_elector"."partido", "electoral_elector"."fecha_nacimiento", 
"electoral_elector"."fecha_afiliacion", "electoral_elector"."tipo_voto_id",
"electoral_elector"."voto1", "electoral_elector"."voto2",
"electoral_elector"."voto3", "electoral_elector"."voto4",
"electoral_elector"."voto5", "electoral_elector"."pasoxpc",
"electoral_elector"."pasoxmv", "electoral_elector"."ciudad_id",
"electoral_elector"."barrio_id", "electoral_elector"."manzana_id", 
"electoral_elector"."nro_casa", 
"electoral_elector"."telefono",
 COALESCE("electoral_elector"."nombre", "") || COALESCE(COALESCE(" " ," " ) || COALESCE("electoral_elector"."apellido","" ),"" ) AS "fullname" 
 FROM "electoral_elector" 
 WHERE ("electoral_elector"."ci" = 0 
 OR COALESCE("electoral_elector"."nombre","" ) || COALESCE(COALESCE(" " ," " ) || COALESCE("electoral_elector"."apellido","" ),"" ) 
 LIKE '%ARNALDO%CORREA%' ESCAPE '\') ORDER BY "fullname" ASC LIMIT 10