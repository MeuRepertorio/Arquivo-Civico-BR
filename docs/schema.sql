-- Arquivo Cívico BR · modelo relacional projetado para a evolução do acervo
-- Não gera afirmações e não atribui culpabilidade automática. PostgreSQL 15+.
-- Toda afirmação factual deve manter documento primário verificável.
CREATE TABLE sources (
  source_id BIGSERIAL PRIMARY KEY,
  institution TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL CHECK(url ~ '^https://'),
  published_at DATE,
  retrieved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  document_number TEXT,
  sha256 TEXT,
  archived_copy_url TEXT,
  verified_by TEXT
);
CREATE TABLE political_parties (
  party_id BIGSERIAL PRIMARY KEY,
  abbreviation TEXT NOT NULL UNIQUE,
  full_name TEXT NOT NULL,
  ballot_number SMALLINT,
  registry_approved_on DATE,
  status_as_of DATE,
  registry_source_id BIGINT REFERENCES sources(source_id),
  notes TEXT
);
CREATE TABLE people (
  person_id BIGSERIAL PRIMARY KEY,
  official_name TEXT NOT NULL,
  source_id BIGINT NOT NULL REFERENCES sources(source_id),
  official_identifier TEXT,
  jurisdiction TEXT,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE party_memberships (
  membership_id BIGSERIAL PRIMARY KEY,
  person_id BIGINT NOT NULL REFERENCES people(person_id),
  party_id BIGINT NOT NULL REFERENCES political_parties(party_id),
  start_on DATE,
  end_on DATE,
  source_id BIGINT NOT NULL REFERENCES sources(source_id),
  notes TEXT
);
CREATE TABLE public_offices (
  office_id BIGSERIAL PRIMARY KEY,
  person_id BIGINT NOT NULL REFERENCES people(person_id),
  office_type TEXT NOT NULL,
  government_level TEXT NOT NULL,
  state_code CHAR(2),
  start_on DATE,
  end_on DATE,
  source_id BIGINT NOT NULL REFERENCES sources(source_id)
);
CREATE TABLE proposals (
  proposal_id BIGSERIAL PRIMARY KEY,
  chamber TEXT NOT NULL,
  institution_identifier TEXT NOT NULL,
  proposal_type TEXT NOT NULL,
  number INTEGER NOT NULL,
  year SMALLINT NOT NULL,
  synopsis TEXT,
  current_status TEXT,
  status_as_of DATE,
  source_id BIGINT NOT NULL REFERENCES sources(source_id),
  UNIQUE(chamber,institution_identifier)
);
CREATE TABLE proposal_authors (
  proposal_id BIGINT NOT NULL REFERENCES proposals(proposal_id),
  person_id BIGINT NOT NULL REFERENCES people(person_id),
  participation_type TEXT NOT NULL,
  source_id BIGINT NOT NULL REFERENCES sources(source_id),
  PRIMARY KEY(proposal_id,person_id,participation_type)
);
CREATE TABLE nominal_votes (
  vote_id BIGSERIAL PRIMARY KEY,
  institution TEXT NOT NULL,
  official_vote_id TEXT NOT NULL,
  voted_at TIMESTAMPTZ,
  description TEXT,
  source_id BIGINT NOT NULL REFERENCES sources(source_id),
  UNIQUE(institution,official_vote_id)
);
CREATE TABLE individual_votes (
  vote_id BIGINT NOT NULL REFERENCES nominal_votes(vote_id),
  person_id BIGINT NOT NULL REFERENCES people(person_id),
  recorded_choice TEXT NOT NULL,
  source_id BIGINT NOT NULL REFERENCES sources(source_id),
  PRIMARY KEY(vote_id,person_id)
);
CREATE TABLE judicial_cases (
  case_id BIGSERIAL PRIMARY KEY,
  tribunal TEXT NOT NULL,
  case_number TEXT NOT NULL,
  case_type TEXT,
  status TEXT NOT NULL CHECK(status IN ('alegacao','investigacao','denuncia','acao','decisao','recurso','transito_em_julgado','arquivado','absolvido','outro')),
  status_as_of DATE NOT NULL,
  primary_document_id BIGINT NOT NULL REFERENCES sources(source_id),
  case_summary TEXT,
  UNIQUE(tribunal,case_number)
);
CREATE TABLE case_participants (
  case_id BIGINT NOT NULL REFERENCES judicial_cases(case_id),
  person_id BIGINT NOT NULL REFERENCES people(person_id),
  formal_role TEXT NOT NULL,
  role_source_id BIGINT NOT NULL REFERENCES sources(source_id),
  PRIMARY KEY(case_id,person_id,formal_role)
);
CREATE TABLE case_events (
  event_id BIGSERIAL PRIMARY KEY,
  case_id BIGINT NOT NULL REFERENCES judicial_cases(case_id),
  occurred_on DATE NOT NULL,
  procedural_stage TEXT NOT NULL,
  description TEXT NOT NULL,
  source_id BIGINT NOT NULL REFERENCES sources(source_id)
);
CREATE TABLE party_case_documented_links (
  case_id BIGINT NOT NULL REFERENCES judicial_cases(case_id),
  party_id BIGINT NOT NULL REFERENCES political_parties(party_id),
  relation_kind TEXT NOT NULL CHECK(relation_kind IN ('person_was_member_at_event','party_entity_was_formal_party','audited_party_accounts')),
  source_id BIGINT NOT NULL REFERENCES sources(source_id),
  note TEXT NOT NULL,
  PRIMARY KEY(case_id,party_id,relation_kind)
);
CREATE TABLE federations (
  federation_id BIGSERIAL PRIMARY KEY,
  official_name TEXT UNIQUE NOT NULL,
  registration_on DATE,
  source_id BIGINT NOT NULL REFERENCES sources(source_id)
);
CREATE TABLE federation_members (
  federation_id BIGINT NOT NULL REFERENCES federations(federation_id),
  party_id BIGINT NOT NULL REFERENCES political_parties(party_id),
  source_id BIGINT NOT NULL REFERENCES sources(source_id),
  PRIMARY KEY(federation_id,party_id)
);
CREATE INDEX ix_people_name ON people(official_name);
CREATE INDEX ix_party_memberships_person ON party_memberships(person_id);
CREATE INDEX ix_proposals_year ON proposals(year);
CREATE INDEX ix_case_events_date ON case_events(occurred_on);
-- NENHUM campo de "nota de corrupção", "credibilidade" ou "melhor político".