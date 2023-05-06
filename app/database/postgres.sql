-- Table for Hunts
CREATE TABLE IF NOT EXISTS HUNTS(
    hunt_id         BIGINT PRIMARY KEY,
    organizer_id    BIGINT NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT NOT NULL,
    photo_url       TEXT,
    created_at      TIMESTAMP DEFAULT current_timestamp,
    start_date      TIMESTAMP NOT NULL,
    end_date        TIMESTAMP NOT NULL
);

-- Table for Treasures
CREATE TABLE IF NOT EXISTS TREASURES(
    treasure_id     BIGINT PRIMARY KEY,
    treasure_secret TEXT  UNIQUE NOT NULL,
    hunt_id         BIGINT NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT,
    win_message     TEXT NOT NULL,
    photo_url       TEXT,
    riddle_id       INT
);

-- Table for Participants
CREATE TABLE IF NOT EXISTS HUNT_PARTICIPANTS(
    treasure_id     BIGINT NOT NULL,
    user_id         BIGINT NOT NULL,
    join_date       TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY     (treasure_id, user_id)
);

-- Table for winners
CREATE TABLE IF NOT EXISTS WINNERS(
    treasure_id     BIGINT PRIMARY KEY ,
    user_id         BIGINT NOT NULL,
    win_date       TIMESTAMP DEFAULT current_timestamp
);

-- Table for riddles
CREATE TABLE IF NOT EXISTS RIDDLES(
    riddle_id SERIAL PRIMARY KEY,
    riddle          TEXT NOT NULL,
    answer          TEXT NOT NULL,
    hints           TEXT
);
