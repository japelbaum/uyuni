
create or replace function web_contact_ins_trig_fun() returns trigger
as
$$
begin
        new.modified := current_timestamp;
        new.login_uc := UPPER(new.login);
        insert into web_contact_all (id, org_id, login)
            values (new.id, new.org_id, new.login);

        return new;
end;
$$
language plpgsql;

