-- DROP SCHEMA urbvan;

CREATE SCHEMA urbvan AUTHORIZATION postgres;

-- DROP TYPE urbvan."_user_auth_api";

CREATE TYPE urbvan."_user_auth_api" (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = urbvan.user_auth_api,
	DELIMITER = ',');

-- DROP TYPE urbvan."_van_vehicle";

CREATE TYPE urbvan."_van_vehicle" (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = urbvan.van_vehicle,
	DELIMITER = ',');
-- urbvan.user_auth_api definition

-- Drop table

-- DROP TABLE urbvan.user_auth_api;

CREATE TABLE urbvan.user_auth_api (
	user_id numeric NOT NULL,
	username varchar NOT NULL, -- Username to authenticate to the API
	"password" varchar NOT NULL, -- Password to authenticate to API
	password_hash bpchar NULL, -- Password hash authenticated
	creation_date timestamp(0) NULL,
	last_update_date timestamp(0) NULL,
	CONSTRAINT user_auth_api_pk PRIMARY KEY (user_id)
);
COMMENT ON TABLE urbvan.user_auth_api IS 'contain the data to authenticate to the API';

-- Column comments

COMMENT ON COLUMN urbvan.user_auth_api.username IS 'Username to authenticate to the API';
COMMENT ON COLUMN urbvan.user_auth_api."password" IS 'Password to authenticate to API';
COMMENT ON COLUMN urbvan.user_auth_api.password_hash IS 'Password hash authenticated';

-- Permissions

ALTER TABLE urbvan.user_auth_api OWNER TO postgres;
GRANT ALL ON TABLE urbvan.user_auth_api TO postgres;


-- urbvan.van_vehicle definition

-- Drop table

-- DROP TABLE urbvan.van_vehicle;

CREATE TABLE urbvan.van_vehicle (
	uuid_van uuid NOT NULL, -- UUID unico para identificar la reserva del usuario
	plates_van varchar NOT NULL, -- Placas de la VAN
	economic_number_van varchar NOT NULL, -- Una nomenclatura para identificar a las camionetas.Ejemplo A1-0001
	seats_van numeric NOT NULL, -- Cantidad de asientos disponibles por camioneta
	created_at date NULL, -- Fecha de alta de la VAN
	status_van varchar NOT NULL DEFAULT 'Activa'::character varying, -- Posibles estatus de la VAN: “Activa”, “En reparación”, “Baja”
	last_update_date timestamp(0) NULL, -- Contiene la fecha de actualizacion del registro
	CONSTRAINT van_vehicle_check CHECK (((status_van)::text = ANY ((ARRAY['Activo'::character varying, 'En reparacion'::character varying, 'Baja'::character varying])::text[]))),
	CONSTRAINT van_vehicle_pk PRIMARY KEY (uuid_van),
	CONSTRAINT van_vehicle_un UNIQUE (uuid_van, plates_van)
);
COMMENT ON TABLE urbvan.van_vehicle IS 'contain the van vehicle attributes to manage it';

-- Column comments

COMMENT ON COLUMN urbvan.van_vehicle.uuid_van IS 'UUID unico para identificar la reserva del usuario';
COMMENT ON COLUMN urbvan.van_vehicle.plates_van IS 'Placas de la VAN';
COMMENT ON COLUMN urbvan.van_vehicle.economic_number_van IS 'Una nomenclatura para identificar a las camionetas.Ejemplo A1-0001';
COMMENT ON COLUMN urbvan.van_vehicle.seats_van IS 'Cantidad de asientos disponibles por camioneta';
COMMENT ON COLUMN urbvan.van_vehicle.created_at IS 'Fecha de alta de la VAN';
COMMENT ON COLUMN urbvan.van_vehicle.status_van IS 'Posibles estatus de la VAN: “Activa”, “En reparación”, “Baja”';
COMMENT ON COLUMN urbvan.van_vehicle.last_update_date IS 'Contiene la fecha de actualizacion del registro';

-- Permissions

ALTER TABLE urbvan.van_vehicle OWNER TO postgres;
GRANT ALL ON TABLE urbvan.van_vehicle TO postgres;

-- Permissions

GRANT ALL ON SCHEMA urbvan TO postgres;

