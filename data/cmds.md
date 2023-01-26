# accounts.db
CREATE TABLE accounts (id int, username text, mail text, password_hash text, totp text, created int);
CREATE TABLE permissions (id int, admin int, moderator int, creator int); 
    // admin = all permission 
    // moderator = delete / manage all polls 
    // creator = create polls and delte / edit them

# polls.db
CREATE TABLE polls (id int, creator int, created int, cookie_prot int, user_agent_prot int, ip_prot int, type int, sheet text, link text, title text, description text);
    // type: 1=question by question, 2=sheet mode
    // ip, cookie, useragent are to block multipe votes