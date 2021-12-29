CREATE DATABASE "Beautipoll"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
--    LC_COLLATE = 'English_Europe.1252'
--    LC_CTYPE = 'English_Europe.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;




-- Table: public.Users

-- DROP TABLE IF EXISTS public."Users";

CREATE TABLE IF NOT EXISTS public."Users"
(
    username character varying[] COLLATE pg_catalog."default" NOT NULL,
    active boolean NOT NULL,
    CONSTRAINT "Users_pkey" PRIMARY KEY (username)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Users"
    OWNER to postgres;



-- Table: public.Admins

-- DROP TABLE IF EXISTS public."Admins";

CREATE TABLE IF NOT EXISTS public."Admins"
(
    username character varying[] COLLATE pg_catalog."default" NOT NULL,
    password character varying[] COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Admins_pkey" PRIMARY KEY (username)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Admins"
    OWNER to postgres;




-- Table: public.Polls

-- DROP TABLE IF EXISTS public."Polls";

CREATE TABLE IF NOT EXISTS public."Polls"
(
    poll_id integer NOT NULL,
    CONSTRAINT "Polls_pkey" PRIMARY KEY (poll_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Polls"
    OWNER to postgres;



-- Table: public.Questions

-- DROP TABLE IF EXISTS public."Questions";

CREATE TABLE IF NOT EXISTS public."Questions"
(
    question_id integer NOT NULL,
    poll_id integer NOT NULL,
    description character varying[] COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Questions_pkey" PRIMARY KEY (question_id),
    CONSTRAINT "Questions_poll_id_fkey" FOREIGN KEY (poll_id)
        REFERENCES public."Polls" (poll_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Questions"
    OWNER to postgres;
-- Index: fki_pull_id

-- DROP INDEX IF EXISTS public.fki_pull_id;

CREATE INDEX IF NOT EXISTS fki_pull_id
    ON public."Questions" USING btree
    (poll_id ASC NULLS LAST)
    TABLESPACE pg_default;



-- Table: public.Answers

-- DROP TABLE IF EXISTS public."Answers";

CREATE TABLE IF NOT EXISTS public."Answers"
(
    answer_id integer NOT NULL,
    description character varying[] COLLATE pg_catalog."default" NOT NULL,
    question_id integer,
    CONSTRAINT "Answers_pkey" PRIMARY KEY (answer_id),
    CONSTRAINT "Answers_question_id_fkey" FOREIGN KEY (question_id)
        REFERENCES public."Questions" (question_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Answers"
    OWNER to postgres;
-- Index: fki_d

-- DROP INDEX IF EXISTS public.fki_d;

CREATE INDEX IF NOT EXISTS fki_d
    ON public."Answers" USING btree
    (question_id ASC NULLS LAST)
    TABLESPACE pg_default;




-- Table: public.PollsAnswers

-- DROP TABLE IF EXISTS public."PollsAnswers";

CREATE TABLE IF NOT EXISTS public."PollsAnswers"
(
    username character varying[] COLLATE pg_catalog."default" NOT NULL,
    poll_id integer NOT NULL,
    question_id integer NOT NULL,
    answer_id integer NOT NULL,
    CONSTRAINT "PollsAnswers_pkey" PRIMARY KEY (username, poll_id, question_id, answer_id),
    CONSTRAINT "PollsAnswers_answer_id_fkey" FOREIGN KEY (answer_id)
        REFERENCES public."Answers" (answer_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "PollsAnswers_poll_id_fkey" FOREIGN KEY (poll_id)
        REFERENCES public."Polls" (poll_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "PollsAnswers_question_id_fkey" FOREIGN KEY (question_id)
        REFERENCES public."Questions" (question_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "PollsAnswers_username_fkey" FOREIGN KEY (username)
        REFERENCES public."Users" (username) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."PollsAnswers"
    OWNER to postgres;
-- Index: fki_3

-- DROP INDEX IF EXISTS public.fki_3;

CREATE INDEX IF NOT EXISTS fki_3
    ON public."PollsAnswers" USING btree
    (username COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: fki_poll_id FK of Polls

-- DROP INDEX IF EXISTS public."fki_poll_id FK of Polls";

CREATE INDEX IF NOT EXISTS "fki_poll_id FK of Polls"
    ON public."PollsAnswers" USING btree
    (poll_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: fki_s

-- DROP INDEX IF EXISTS public.fki_s;

CREATE INDEX IF NOT EXISTS fki_s
    ON public."PollsAnswers" USING btree
    (poll_id ASC NULLS LAST)
    TABLESPACE pg_default;