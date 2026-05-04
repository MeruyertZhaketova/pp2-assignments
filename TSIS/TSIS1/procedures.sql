-- clean old obj

DROP FUNCTION  IF EXISTS search_contacts(TEXT) CASCADE;
DROP FUNCTION  IF EXISTS pagination(INT, INT) CASCADE;

DROP PROCEDURE IF EXISTS move_to_group(VARCHAR, VARCHAR) CASCADE;
DROP PROCEDURE IF EXISTS add_phone(VARCHAR, VARCHAR, VARCHAR) CASCADE;
DROP PROCEDURE IF EXISTS del_user(VARCHAR) CASCADE;
DROP PROCEDURE IF EXISTS loophz(VARCHAR[], VARCHAR[]) CASCADE;
DROP PROCEDURE IF EXISTS upsert_u(VARCHAR, VARCHAR, VARCHAR) CASCADE;


-- upsert cont phone
CREATE PROCEDURE upsert_u(
    p_name  VARCHAR,
    p_phone VARCHAR,
    p_type  VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INT;
BEGIN
    -- insert contact if not exists
    INSERT INTO phonebook (username)
    VALUES (p_name)
    ON CONFLICT (username) DO NOTHING;

    -- get contact id
    SELECT id INTO v_id FROM phonebook WHERE username = p_name;

    -- insert phone
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);
END;
$$;


-- bulk insert with validation

CREATE PROCEDURE loophz(
    p_user  VARCHAR[],
    p_phone VARCHAR[]
)
LANGUAGE plpgsql AS $$
BEGIN
    FOR i IN 1..array_length(p_user, 1) LOOP

        IF p_phone[i] ~ '[a-zA-Z_!@#$%]' THEN
            RAISE NOTICE 'Invalid phone: %', p_phone[i];

        ELSIF p_user[i] ~ '[0-9]' THEN
            RAISE NOTICE 'Invalid username: %', p_user[i];

        ELSE
            CALL upsert_u(p_user[i], p_phone[i], 'mobile');
        END IF;

    END LOOP;
END;
$$;


-- del cont

CREATE PROCEDURE del_user(p VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    -- delete by username
    DELETE FROM phonebook WHERE username = p;

    -- delete by phone
    DELETE FROM phonebook
    WHERE id IN (
        SELECT contact_id FROM phones WHERE phone = p
    );
END;
$$;


-- add more phone

CREATE PROCEDURE add_phone(
    p_name  VARCHAR,
    p_phone VARCHAR,
    p_type  VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT id INTO v_id FROM phonebook WHERE username = p_name;

    IF v_id IS NULL THEN
        RAISE NOTICE 'User not found: %', p_name;
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);

    RAISE NOTICE 'Phone added to %', p_name;
END;
$$;


-- move to group

CREATE PROCEDURE move_to_group(
    p_name  VARCHAR,
    p_group VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_gid INT;
    v_cid INT;
BEGIN
    -- create group if not exists
    INSERT INTO groups (name)
    VALUES (p_group)
    ON CONFLICT (name) DO NOTHING;

    -- get ids
    SELECT id INTO v_gid FROM groups WHERE name = p_group;
    SELECT id INTO v_cid FROM phonebook WHERE username = p_name;

    IF v_cid IS NULL THEN
        RAISE NOTICE 'User not found: %', p_name;
        RETURN;
    END IF;

    -- update group
    UPDATE phonebook
    SET group_id = v_gid
    WHERE id = v_cid;

    RAISE NOTICE 'Moved % to group %', p_name, p_group;
END;
$$;


-- pagination

CREATE FUNCTION pagination(
    lim  INT,
    offs INT
)
RETURNS TABLE(
    id INT,
    username VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name,
        STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ')
    FROM phonebook c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    GROUP BY c.id, c.username, c.email, c.birthday, g.name, c.created_at
    ORDER BY c.username
    LIMIT lim OFFSET offs;
END;
$$;


-- search

CREATE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INT,
    username VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name,
        STRING_AGG(p.phone, ', ')
    FROM phonebook c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE
        c.username ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.username, c.email, c.birthday, g.name;
END;
$$;

SELECT 'procedures created successfully' AS status;