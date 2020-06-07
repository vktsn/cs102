-- Database: Lych

-- DROP DATABASE "Lych";

CREATE DATABASE "Lych"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
-- SCHEMA: public

-- DROP SCHEMA public ;

CREATE SCHEMA public
    AUTHORIZATION postgres;

COMMENT ON SCHEMA public
    IS 'standard public schema';

GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres;

-- Table: public.Client

-- DROP TABLE public."Client";

CREATE TABLE public."Client"
(
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default",
    phone text COLLATE pg_catalog."default",
    CONSTRAINT "Client_pkey" PRIMARY KEY ("Name")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Client"
    OWNER to postgres;
COMMENT ON TABLE public."Client"
    IS 'Таблица Рекламодатель, содержащая основную информацию о нанимателе.';
    
 -- Table: public.Labor_contract

-- DROP TABLE public."Labor_contract";

CREATE TABLE public."Labor_contract"
(
    "Req_ID" integer NOT NULL,
    "Work_ID" integer NOT NULL,
    "Dates" text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Labor_contract"
    OWNER to postgres;
COMMENT ON TABLE public."Labor_contract"
    IS 'Таблица Трудовое соглашение, связывающая рекламодателя с работником агенства.';
    
 -- Table: public.Material

-- DROP TABLE public."Material";

CREATE TABLE public."Material"
(
    "Mat_ID" integer NOT NULL,
    "Serv_ID" integer,
    "Number" text COLLATE pg_catalog."default",
    "Total cost" text COLLATE pg_catalog."default",
    CONSTRAINT "Material_pkey" PRIMARY KEY ("Mat_ID")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Material"
    OWNER to postgres;
COMMENT ON TABLE public."Material"
    IS 'Таблица Материал, связывающая материал из списка с услугой, для которой он необходим.';
    
 -- Table: public.Material_list

-- DROP TABLE public."Material_list";

CREATE TABLE public."Material_list"
(
    "Mat_ID" integer NOT NULL,
    "Naming" text COLLATE pg_catalog."default",
    "Descroption" text COLLATE pg_catalog."default",
    "Cost" text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Material_list"
    OWNER to postgres;
COMMENT ON TABLE public."Material_list"
    IS 'Таблица Список материалов, содержащая информацию о материалах.';
    
 -- Table: public.Payment_order

-- DROP TABLE public."Payment_order";

CREATE TABLE public."Payment_order"
(
    "Req_ID" integer NOT NULL,
    "Status" text COLLATE pg_catalog."default" NOT NULL,
    "Date" text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Payment_order"
    OWNER to postgres;
COMMENT ON TABLE public."Payment_order"
    IS 'Таблица Платежное поручение, содержая инормацию о статусе оплаты заявки.';
    
 -- Table: public.Price_list

-- DROP TABLE public."Price_list";

CREATE TABLE public."Price_list"
(
    "Serv_ID" integer NOT NULL,
    "Naming" text COLLATE pg_catalog."default",
    "Description" text COLLATE pg_catalog."default",
    "Cost" text COLLATE pg_catalog."default",
    CONSTRAINT "Price_list_pkey" PRIMARY KEY ("Serv_ID")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Price_list"
    OWNER to postgres;
COMMENT ON TABLE public."Price_list"
    IS 'Таблица Прайс лист, содержащая информацию о предоставляемых услугах.';
    
 -- Table: public.Request

-- DROP TABLE public."Request";

CREATE TABLE public."Request"
(
    "Req_ID" integer NOT NULL,
    "Name" text COLLATE pg_catalog."default",
    "Date" text COLLATE pg_catalog."default",
    CONSTRAINT "Request_pkey" PRIMARY KEY ("Req_ID")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Request"
    OWNER to postgres;
COMMENT ON TABLE public."Request"
    IS 'Заявка, которую оставляет рекламодатель.';
    
 -- Table: public.Service

-- DROP TABLE public."Service";

CREATE TABLE public."Service"
(
    "Serv_ID" integer NOT NULL,
    "Req_ID" integer,
    "Total cost" text COLLATE pg_catalog."default",
    CONSTRAINT "Service_pkey" PRIMARY KEY ("Serv_ID")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Service"
    OWNER to postgres;
COMMENT ON TABLE public."Service"
    IS 'Таблица Услуги,  состоящая из перечня услуг для конкретной заявки.';
    
 -- Table: public.Worker

-- DROP TABLE public."Worker";

CREATE TABLE public."Worker"
(
    "Work_ID" integer NOT NULL,
    "FIO" text COLLATE pg_catalog."default",
    "Expirience" text COLLATE pg_catalog."default",
    "Contacts" text COLLATE pg_catalog."default",
    CONSTRAINT "Worker_pkey" PRIMARY KEY ("Work_ID")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Worker"
    OWNER to postgres;
COMMENT ON TABLE public."Worker"
    IS 'Таблица Работник, содержащая информаю о работниках агенства.';
    
 
