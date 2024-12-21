BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 33abefe81181

INSERT INTO alembic_version (version_num) VALUES ('33abefe81181') RETURNING alembic_version.version_num;

-- Running upgrade 33abefe81181 -> 8cb825b7e37e

CREATE TYPE roletype AS ENUM ('merchant', 'buyer', 'admin');

CREATE TABLE users (
    id UUID NOT NULL, 
    first_name VARCHAR(50) NOT NULL, 
    last_name VARCHAR(50) NOT NULL, 
    email VARCHAR(100) NOT NULL, 
    hashed_password VARCHAR(128) NOT NULL, 
    location VARCHAR(100) NOT NULL, 
    photo_url VARCHAR(250), 
    phone VARCHAR(20), 
    store_name VARCHAR(100), 
    role roletype NOT NULL, 
    is_active BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    deleted_at TIMESTAMP WITH TIME ZONE, 
    PRIMARY KEY (id)
);

COMMENT ON COLUMN users.first_name IS 'User''s first name.';

COMMENT ON COLUMN users.last_name IS 'User''s last name.';

COMMENT ON COLUMN users.email IS 'Unique user email address.';

COMMENT ON COLUMN users.hashed_password IS 'Hashed user password.';

COMMENT ON COLUMN users.location IS 'User''s location.';

COMMENT ON COLUMN users.photo_url IS 'Optional photo URL for the user.';

COMMENT ON COLUMN users.phone IS 'Optional phone number.';

COMMENT ON COLUMN users.store_name IS 'Optional store name for sellers.';

COMMENT ON COLUMN users.role IS 'User role. Default is ''buyer''.';

COMMENT ON COLUMN users.is_active IS 'Indicates if the user is active.';

COMMENT ON COLUMN users.deleted_at IS 'Soft delete timestamp.';

CREATE UNIQUE INDEX ix_users_email ON users (email);

UPDATE alembic_version SET version_num='8cb825b7e37e' WHERE alembic_version.version_num = '33abefe81181';

COMMIT;

