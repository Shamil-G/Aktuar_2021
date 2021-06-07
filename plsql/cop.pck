create or replace package cop is

  -- Author  : ГУСЕЙНОВ_Ш
  -- Created : 02.11.2020 16:13:15
  -- Purpose : 
  
  -- Public type declarations
  procedure user(uname in nvarchar2, upass out nvarchar2, uactive out nchar);
  procedure new_user(uname in nvarchar2, upass in nvarchar2, imess out nvarchar2);
  procedure login(uname in nvarchar2, upass out nvarchar2, uactive out nchar);
  procedure login(uname in nvarchar2, upass out nvarchar2, iid_user out number);
  
  
  
end cop;
/
create or replace package body cop is

  procedure user(uname in nvarchar2, upass out nvarchar2, uactive out nchar)
  is
  begin
    insert into protocol(event_date, message) values(sysdate, 'get User: '||uname||' : '||upass||' : '||uactive);
    commit;
    select
         u.password, u.active
         into
         upass, uactive
    from users u where u.name=uname;
    exception when no_data_found then upass := '';
  end;

  procedure new_user(uname in nvarchar2, upass in nvarchar2, imess out nvarchar2)
  is
  v_id_user number(9);
  begin
    select max(id_user) into v_id_user from users;
    insert into protocol(event_date, message) values(sysdate, 'New User: '||uname||' : '||upass);
    commit;
    insert into users(id_user, name, password) values(v_id_user+1, uname, upass);
    commit;
    imess:='';
    exception when dup_val_on_index then
      begin
        insert into protocol(event_date, message) values(sysdate, 'New User duplicate user name: '||uname);
        imess:='Такое имя в системе уже существует';
        commit;
      end;
  end;

  procedure login(uname in nvarchar2, upass out nvarchar2, uactive out nchar)
  is
  v_password nvarchar2(512);
  v_active   nchar(1);
  v_id       number(9);
  begin
    insert into protocol(event_date, message) values(CURRENT_TIMESTAMP, 'Login for: '||uname);
    commit;
    select
        u.password, u.active
         into
        v_password, v_active
    from users u where u.name=uname;
    insert into protocol(event_date, message) values(CURRENT_TIMESTAMP, 'Success: '||uname||' : '||v_id ||' : '||v_password||' : '||v_active);
    commit;
    upass:=v_password;
    uactive:=v_active;
    exception when no_data_found then upass := '';
  end;

  procedure login(uname in nvarchar2, upass out nvarchar2, iid_user out number)
  is
  v_password nvarchar2(512);
  v_active   nchar(1);
  v_id       number(9);
  begin
    insert into protocol(event_date, message) values(CURRENT_TIMESTAMP, 'Login for: '||uname);
    commit;
    select
        u.password, u.id_user
         into
        v_password, v_id
    from users u where u.name=uname;
    insert into protocol(event_date, message) values(CURRENT_TIMESTAMP, 'Success: '||uname||' : '||v_id||' : '||v_password);
    commit;
    upass:=v_password;
    iid_user:=v_id;
    exception when no_data_found then upass := '';
  end;

begin
  null;
end cop;
/
