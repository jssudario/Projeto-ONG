--
-- PostgreSQL database dump
--

\restrict hquJPGMGzdr2ahpn8hX0zaEulseummoWTKSVLRqGSiWEJnQd3r0oj2j0n1E5o2O

-- Dumped from database version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: adotante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.adotante (
    id integer NOT NULL,
    nome_completo character varying(255) NOT NULL,
    cpf character varying(11) NOT NULL,
    data_nascimento date NOT NULL,
    email character varying(255) NOT NULL,
    telefone character varying(15) NOT NULL,
    estado character varying(2) NOT NULL,
    cidade character varying(100) NOT NULL,
    rua character varying(200) NOT NULL,
    numero character varying(30),
    complemento character varying(100),
    bairro character varying(50)
);


ALTER TABLE public.adotante OWNER TO postgres;

--
-- Name: adotante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.adotante_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.adotante_id_seq OWNER TO postgres;

--
-- Name: adotante_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.adotante_id_seq OWNED BY public.adotante.id;


--
-- Name: animal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.animal (
    id integer NOT NULL,
    nome character varying(80) NOT NULL,
    especie character varying(30) NOT NULL,
    raca character varying(60),
    sexo character varying(10) NOT NULL,
    idade_meses integer NOT NULL,
    porte character varying(15),
    castrado boolean NOT NULL,
    vacinado boolean NOT NULL,
    status character varying(15) NOT NULL,
    data_entrada date,
    observacoes text,
    foto character varying
);


ALTER TABLE public.animal OWNER TO postgres;

--
-- Name: animal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.animal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.animal_id_seq OWNER TO postgres;

--
-- Name: animal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.animal_id_seq OWNED BY public.animal.id;


--
-- Name: solicitacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.solicitacao (
    id integer NOT NULL,
    data_solicitacao date NOT NULL,
    status character varying(15) NOT NULL,
    motivo_recusa text,
    animal_id integer NOT NULL,
    adotante_id integer NOT NULL
);


ALTER TABLE public.solicitacao OWNER TO postgres;

--
-- Name: solicitacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.solicitacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.solicitacao_id_seq OWNER TO postgres;

--
-- Name: solicitacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.solicitacao_id_seq OWNED BY public.solicitacao.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    hashed_password character varying(255) NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: visita; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.visita (
    id integer NOT NULL,
    data_hora timestamp without time zone NOT NULL,
    retorno character varying(15) NOT NULL,
    observacoes text,
    solicitacao_id integer NOT NULL
);


ALTER TABLE public.visita OWNER TO postgres;

--
-- Name: visita_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.visita_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.visita_id_seq OWNER TO postgres;

--
-- Name: visita_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.visita_id_seq OWNED BY public.visita.id;


--
-- Name: adotante id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adotante ALTER COLUMN id SET DEFAULT nextval('public.adotante_id_seq'::regclass);


--
-- Name: animal id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animal ALTER COLUMN id SET DEFAULT nextval('public.animal_id_seq'::regclass);


--
-- Name: solicitacao id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitacao ALTER COLUMN id SET DEFAULT nextval('public.solicitacao_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: visita id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visita ALTER COLUMN id SET DEFAULT nextval('public.visita_id_seq'::regclass);


--
-- Data for Name: adotante; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.adotante (id, nome_completo, cpf, data_nascimento, email, telefone, estado, cidade, rua, numero, complemento, bairro) FROM stdin;
5	Graciele Freitas	11111111111	2003-03-24	graciele@gmail.com	35999887767	ES	Castelo	Rua Brasil	12	\N	Jardim
4	Lucas Martins	12345678903	2004-06-30	lucas@email.com	35999887766	SP	Franca	Avenida Europa	100	\N	Vila Nova
6	Julia Sudário	37822359835	2003-01-12	jssudario@gmail.com	35999398923	MG	Monte Azul	Rua Liberdade	15	\N	Consolação
9	Teste	11111111177	2003-02-01	teste@gmail.com	35999398899	RJ	Cambuci	Avenida Europa	12		Vila Nova
\.


--
-- Data for Name: animal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.animal (id, nome, especie, raca, sexo, idade_meses, porte, castrado, vacinado, status, data_entrada, observacoes, foto) FROM stdin;
5	Apollo	cachorro	\N	macho	24	grande	t	t	disponivel	2025-12-01	\N	apollo.jpeg
6	Zeus	cachorro	\N	macho	6	grande	t	t	disponivel	2025-12-02	\N	zeus.jpeg
8	Yuki	gato	\N	macho	39	nao_se_aplica	t	t	disponivel	2025-11-10	\N	yuki.jpeg
9	Dara	cachorro	\N	femea	22	medio	t	t	disponivel	2025-11-17	\N	dara.jpeg
10	Athena	cachorro	\N	femea	2	grande	t	t	disponivel	2025-11-17	\N	atheninha.jpeg
11	Maggie	gato	\N	femea	8	nao_se_aplica	t	t	disponivel	2025-11-24	\N	maggie.jpeg
12	Dinah	gato	\N	femea	11	nao_se_aplica	t	t	disponivel	2025-11-01	\N	dinah.jpg
13	Bryan	cachorro	\N	macho	36	pequeno	t	t	disponivel	2025-11-03	\N	bryan.jpeg
14	Spike	cachorro	\N	macho	9	medio	t	t	disponivel	2025-11-10	\N	spike.jpeg
16	Tekinha	cachorro	\N	femea	72	pequeno	t	t	disponivel	2025-12-01	\N	tekinha.jpeg
17	Noah	gato	\N	macho	8	nao_se_aplica	t	t	disponivel	2025-12-01	\N	noah.jpeg
18	Miah	gato	\N	femea	5	nao_se_aplica	t	t	disponivel	2025-12-01	\N	miah.jpeg
19	Lua	cachorro	\N	femea	26	pequeno	t	t	disponivel	2025-12-01	\N	lua.jpeg
22	Darwin	cachorro	\N	macho	60	pequeno	t	t	disponivel	2025-12-01	\N	darwin.jpeg
15	Glenn	gato	\N	macho	13	nao_se_aplica	t	t	reservado	2025-11-03	\N	glenn.jpeg
\.


--
-- Data for Name: solicitacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.solicitacao (id, data_solicitacao, status, motivo_recusa, animal_id, adotante_id) FROM stdin;
4	2025-12-01	pendente	\N	13	4
5	2025-12-01	pendente	\N	8	5
6	2025-12-01	pendente	\N	11	6
11	2025-12-02	pendente	\N	10	9
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, hashed_password) FROM stdin;
1	julia	$argon2id$v=19$m=65536,t=3,p=4$aO3dG0NIaa0VohRijBHCmA$/M/7TwoV8YNz6KXOHNAcdTjFHwrr/MCvyx1a1sMMOyE
\.


--
-- Data for Name: visita; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.visita (id, data_hora, retorno, observacoes, solicitacao_id) FROM stdin;
2	2025-12-05 12:30:00	reprovado	Mora em apartamento sem tela	5
1	2025-12-08 15:25:00	aprovado	\N	4
3	2025-12-15 14:15:00	pendente	\N	6
\.


--
-- Name: adotante_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.adotante_id_seq', 9, true);


--
-- Name: animal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.animal_id_seq', 22, true);


--
-- Name: solicitacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.solicitacao_id_seq', 11, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- Name: visita_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.visita_id_seq', 5, true);


--
-- Name: adotante adotante_cpf_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adotante
    ADD CONSTRAINT adotante_cpf_key UNIQUE (cpf);


--
-- Name: adotante adotante_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adotante
    ADD CONSTRAINT adotante_email_key UNIQUE (email);


--
-- Name: adotante adotante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adotante
    ADD CONSTRAINT adotante_pkey PRIMARY KEY (id);


--
-- Name: animal animal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animal
    ADD CONSTRAINT animal_pkey PRIMARY KEY (id);


--
-- Name: solicitacao solicitacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitacao
    ADD CONSTRAINT solicitacao_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: visita visita_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visita
    ADD CONSTRAINT visita_pkey PRIMARY KEY (id);


--
-- Name: ix_adotante_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_adotante_id ON public.adotante USING btree (id);


--
-- Name: ix_animal_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_animal_id ON public.animal USING btree (id);


--
-- Name: ix_solicitacao_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_solicitacao_id ON public.solicitacao USING btree (id);


--
-- Name: ix_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_id ON public."user" USING btree (id);


--
-- Name: ix_user_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_username ON public."user" USING btree (username);


--
-- Name: ix_visita_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_visita_id ON public.visita USING btree (id);


--
-- Name: solicitacao solicitacao_adotante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitacao
    ADD CONSTRAINT solicitacao_adotante_id_fkey FOREIGN KEY (adotante_id) REFERENCES public.adotante(id);


--
-- Name: solicitacao solicitacao_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitacao
    ADD CONSTRAINT solicitacao_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animal(id);


--
-- Name: visita visita_solicitacao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visita
    ADD CONSTRAINT visita_solicitacao_id_fkey FOREIGN KEY (solicitacao_id) REFERENCES public.solicitacao(id);


--
-- PostgreSQL database dump complete
--

\unrestrict hquJPGMGzdr2ahpn8hX0zaEulseummoWTKSVLRqGSiWEJnQd3r0oj2j0n1E5o2O

