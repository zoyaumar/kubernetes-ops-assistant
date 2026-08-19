-- Local development seed data.
INSERT INTO clusters (id, name, environment, created_at)
VALUES (
    'aaaaaaaa-0000-0000-0000-000000000001',
    'local-kind',
    'local',
    now()
) ON CONFLICT DO NOTHING;

INSERT INTO users (id, email, password_hash, created_at)
VALUES (
    'bbbbbbbb-0000-0000-0000-000000000001',
    'demo@local.dev',
    '$2b$12$PLACEHOLDER_CHANGE_BEFORE_USE',
    now()
) ON CONFLICT DO NOTHING;
