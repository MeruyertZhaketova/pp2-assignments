-- 1. UPSERT (insert or update)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone)
        VALUES(p_name, p_phone);
    END IF;
END;
$$;


-- 2. BULK INSERT с проверкой телефонов
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_data JSON)
LANGUAGE plpgsql AS $$
DECLARE
    rec JSON;
    invalid_data TEXT := '';
BEGIN
    FOR rec IN SELECT * FROM json_array_elements(p_data)
    LOOP
        -- проверка телефона (только цифры, можно с +, длина 10-15)
        IF (rec->>'phone') ~ '^\+?\d{10,15}$' THEN
            -- если имя уже есть → update
            IF EXISTS (SELECT 1 FROM contacts WHERE name = rec->>'name') THEN
                UPDATE contacts
                SET phone = rec->>'phone'
                WHERE name = rec->>'name';
            ELSE
                INSERT INTO contacts(name, phone)
                VALUES (rec->>'name', rec->>'phone');
            END IF;
        ELSE
            -- сохраняем неправильные данные
            invalid_data := invalid_data || rec::text || E'\n';
        END IF;
    END LOOP;

    -- выводим ошибки
    IF invalid_data <> '' THEN
        RAISE NOTICE 'Invalid data:\n%', invalid_data;
    END IF;
END;
$$;


-- 3. DELETE по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact(
    p_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_name IS NOT NULL THEN
        DELETE FROM contacts WHERE name = p_name;

    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM contacts WHERE phone = p_phone;

    ELSE
        RAISE NOTICE 'Provide name or phone';
    END IF;
END;
$$;