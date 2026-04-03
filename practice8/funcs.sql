create or replace function search(pattern varchar)
RETURNS TABLE( id int, name varchar, surname varchar, phone varchar)
AS $$
BEGIN
return query
select p.id, p.name, p.surname, p.phone from phb as p
WHERE p.name ILIKE '%' || pattern || '%'
       OR p.surname ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%'
    ORDER BY id;
end;
$$
LANGUAGE plpgsql;


create or replace function pagination(lim int, os int)
RETURNS TABLE( id int, name varchar, surname varchar, phone varchar)
AS $$
BEGIN
return query
select p.id, p.name, p.surname, p.phone from phb as p ORDER BY id LIMIT lim OFFSET os;
end;
$$
LANGUAGE plpgsql;


