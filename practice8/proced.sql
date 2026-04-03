CREATE OR REPLACE PROCEDURE upsert(
    n_name VARCHAR,
    n_surname VARCHAR,
    n_phone VARCHAR
)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phb WHERE name = n_name and surname = n_surname) THEN
        UPDATE phb SET phone = n_phone
        WHERE name = n_name and surname = n_surname;
    ELSE
        INSERT INTO phb(name, surname, phone)
        VALUES(n_name, n_surname, n_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE bulk_insert(
    names VARCHAR[],
    surnames VARCHAR[],
    phones VARCHAR[]
)
AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF phones[i] ~ '[a-zA-Z_!@#$%^&*()_~]' THEN 
            RAISE NOTICE 'Number %s is invalid.', phones[i];
        ELSIF names[i] ~ '[0-9~!@#$%^&*()_+=-]' THEN
            RAISE NOTICE 'Name %s is invalid.', names[i];
        ELSIF surnames[i] ~ '[0-9~!@#$%^&*()_+=-]' THEN
            RAISE NOTICE 'Surname %s is invalid.', surnames[i];
        ELSE
            CALL upsert(names[i], surnames[i], phones[i]);
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete(d_name VARCHAR)
AS
$$
BEGIN
    DELETE FROM phb WHERE name = d_name or surname = d_name or phone = d_name;
END;
$$
LANGUAGE plpgsql;
