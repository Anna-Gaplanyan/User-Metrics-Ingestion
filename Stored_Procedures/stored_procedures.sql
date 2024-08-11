CREATE OR REPLACE FUNCTION aggregate_user_metrics(p_user_id INT)
RETURNS TABLE(talked_time_sum INT, session_count INT) AS $$
BEGIN
    RETURN QUERY
    SELECT COALESCE(SUM(m.talked_time), 0) AS talked_time_sum, COUNT(DISTINCT s.session_id) AS session_count
    FROM sessions s
    LEFT JOIN metrics m ON s.session_id = m.session_id
    WHERE s.user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_session_details(p_session_id INT)
RETURNS TABLE(name TEXT, email TEXT, start_time TIMESTAMPTZ, end_time TIMESTAMPTZ, device_info TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT u.name, u.email, s.start_time, s.end_time, s.device_info
    FROM sessions s
    JOIN users u ON s.user_id = u.user_id
    WHERE s.session_id = p_session_id;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION generate_weekly_report()
RETURNS TABLE(name TEXT, email TEXT, session_count INT, total_talked_time INT, last_session TIMESTAMPTZ) AS $$
BEGIN
    RETURN QUERY
    SELECT
        u.name,
        u.email,
        COUNT(DISTINCT s.session_id) AS session_count,
        COALESCE(SUM(m.talked_time), 0) AS total_talked_time,
        MAX(s.start_time) AS last_session
    FROM
        users u
    LEFT JOIN
        sessions s ON u.user_id = s.user_id
    LEFT JOIN
        metrics m ON s.session_id = m.session_id
    WHERE
        s.start_time >= NOW() - INTERVAL '7 days'
    GROUP BY
        u.user_id, u.name, u.email;
END;
$$ LANGUAGE plpgsql;
