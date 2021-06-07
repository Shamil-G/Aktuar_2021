-- Create table
create table AKTUAR_MODELS
(
  id_model NUMBER(6) not null,
  title    VARCHAR2(100 CHAR) not null,
  intro    VARCHAR2(300 CHAR) not null,
  text     CLOB,
  dat      DATE
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
-- Create/Recreate primary, unique and foreign key constraints 
alter table AKTUAR_MODELS
  add constraint PK_AKTUAR_MODELS primary key (ID_MODEL)
  using index 
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );


-- Create table
create table MODEL_CALCULATES
(
  id_calc   NUMBER not null,
  calc_type CHAR(1) not null,
  pnpt_id   NUMBER(12) not null,
  rfpm_id   VARCHAR2(8) not null,
  summ_all  NUMBER(19,2) not null,
  date_stop DATE
)
tablespace DATA
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 2M
    next 2M
    minextents 1
    maxextents unlimited
  )
nologging;
-- Create/Recreate primary, unique and foreign key constraints 
alter table MODEL_CALCULATES
  add constraint PK_MODLE_CALCULATES primary key (ID_CALC, CALC_TYPE, PNPT_ID)
  using index 
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

-- Create table
create table MODEL_STATUS_CALCULATES
(
  id_calc         NUMBER(5) not null,
  date_calc       DATE,
  id_model        NUMBER(5),
  st_0701         CHAR(1),
  st_0702         CHAR(1),
  st_0703         CHAR(1),
  st_0705         CHAR(1),
  sched_time_0701 DATE,
  beg_time_0701   DATE,
  end_time_0701   DATE,
  sched_time_0702 DATE,
  beg_time_0702   DATE,
  end_time_0702   DATE,
  sched_time_0703 DATE,
  beg_time_0703   DATE,
  end_time_0703   DATE,
  sched_time_0705 DATE,
  beg_time_0705   DATE,
  end_time_0705   DATE
)
tablespace DATA
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 16K
    next 16K
    minextents 1
    maxextents unlimited
  );
-- Create/Recreate primary, unique and foreign key constraints 
alter table MODEL_STATUS_CALCULATES
  add constraint PK_MODEL_CALCULATES primary key (ID_CALC)
  using index 
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

-- Create table
create table ROLES
(
  id_role   NUMBER(6),
  name      NVARCHAR2(255),
  id_parent NUMBER(6),
  active    CHAR(1)
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );


-- Create table
create table USERS
(
  id_user  NUMBER(6) not null,
  name     NVARCHAR2(32),
  password NVARCHAR2(512),
  active   CHAR(1)
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
-- Create/Recreate indexes 
create unique index XU_USERS_USERNAME on USERS (NAME)
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
-- Create/Recreate primary, unique and foreign key constraints 
alter table USERS
  add constraint PK_USERS_USER_ID primary key (ID_USER)
  using index 
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

-- Create table
create table USERS_ROLES
(
  id_user NUMBER,
  id_role NUMBER
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

-- Create table
create table PROTOCOL
(
  event_date TIMESTAMP(6),
  message    VARCHAR2(1000)
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
