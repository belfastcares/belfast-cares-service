INSERT INTO web_app_address VALUES (1, 'Unit 36, Townsend Enterprise Park, Townsend St, Belfast', 'Antrim', 'BT13 2ES');
INSERT INTO web_app_address VALUES (2, '196-200 Antrim Road, Belfast', 'Antrim', 'BT15 2AJ');
INSERT INTO web_app_address VALUES (3, '4th Floor, Andras House, 60 Great Victoria St, Belfast', 'Antrim', 'BT2 7BB');
INSERT INTO web_app_address VALUES (4, '25-27 Franklin St, Belfast', 'Antrim', 'BT2 8DS');

SELECT pg_catalog.setval('web_app_address_id_seq', 4, true);

INSERT INTO web_app_contact VALUES (1, 'Outreach', 'Team', '02890 000 000', '07894 931 047', 'welcome@organisation.com', 'Every year the Welcome Organisation assists around 1,300 individuals make their journey out of homelessness.', 1);
INSERT INTO web_app_contact VALUES (2, 'Aileen', 'Coney', '028 9035 1561', '028 9000 0000', 'info@svpni.co.uk', 'No work of charity is foreign to the society. Our work through person to person contact encompasses every form of aid that alleviates suffering and promotes the dignity of mankind. The society strives not only to alleviate need but also to discover and redress the situtations which cause it. It services everyone in need, regardless of creed, opinion,colour, origin or caste.', 2);
INSERT INTO web_app_contact VALUES (3, 'Council for the Homeless', 'NI', '028 9024 6440', '028 9000 0000', 'contact@chni.com', 'Founded in 1983, we are the sole representative organisation for those working with and supporting homeless people across Northern Ireland. We are the independent voice of the sector.', 3);
INSERT INTO web_app_contact VALUES (4, 'Central', 'Office', '028 90 232 882', '028 9000 0000', 'info@simoncommunity.org', 'Established in 1971 in response to a homelessness crisis in Belfast, Simon Community has grown to become Northern Ireland’s leading homelessness charity and service provider. From a beginning of just one house, two full time staff and a few volunteers in Belfast, Simon Community NI now helps over 3000 people every year across 22 projects throughout Northern Ireland with a staff count of 300 and 50 volunteers. We work without judgement to support people who are, or are at risk of, becoming homeless.', 4);

SELECT pg_catalog.setval('web_app_contact_id_seq', 4, true);

INSERT INTO web_app_wishlist VALUES (1, '2016-09-10 07:00:00+01', '2016-10-10 07:00:00+01', true);
INSERT INTO web_app_wishlist VALUES (2, '2016-09-10 07:00:00+01', '2016-10-10 07:00:00+01', false);
INSERT INTO web_app_wishlist VALUES (3, '2016-09-10 07:00:00+01', '2016-10-10 07:00:00+01', false);
INSERT INTO web_app_wishlist VALUES (4, '2016-09-10 07:00:00+01', '2016-10-10 07:00:00+01', false);


INSERT INTO web_app_item VALUES (1, 'Sleeping Bag', 'Warm, durable & waterproof if possible', 1);
INSERT INTO web_app_item VALUES (2, 'Toothbrush', 'Travel toothbrush. Non-electric.', 1);
INSERT INTO web_app_item VALUES (3, 'Toothpaste', 'Small travel toothpaste', 1);
INSERT INTO web_app_item VALUES (4, 'Mens Winter Socks', 'New mens winter socks.', 1);
INSERT INTO web_app_item VALUES (5, 'Womens Winter Socks', 'New womens'' winter socks.', 1);
INSERT INTO web_app_item VALUES (6, 'Cutlery', 'All cutlery welcome. Should be clean and considered usable by others.', 1);
INSERT INTO web_app_item VALUES (7, 'Sleeping Bag', 'Warm, durable & waterproof if possible.', 2);
INSERT INTO web_app_item VALUES (8, 'Toothbrush', 'Small travel toothbrush.', 2);
INSERT INTO web_app_item VALUES (9, 'Toothpaste', 'Small travel toothpaste.', 2);
INSERT INTO web_app_item VALUES (10, 'Mens Winter Socks', 'New mens'' winter socks.', 2);
INSERT INTO web_app_item VALUES (11, 'Womens Winter Socks', 'New womens'' winter socks', 2);
INSERT INTO web_app_item VALUES (12, 'Cutlery', 'All cutlery welcome. Should be clean and considered usable by others.', 2);
INSERT INTO web_app_item VALUES (13, 'Sleeping Bag', 'Warm, durable & waterproof if possible.', 3);
INSERT INTO web_app_item VALUES (14, 'Toothbrush', 'Small travel toothpaste.', 3);
INSERT INTO web_app_item VALUES (15, 'Toothbrush', 'Small travel toothbrush.', 3);
INSERT INTO web_app_item VALUES (16, 'Mens Winter Socks', 'New mens'' winter socks.', 3);
INSERT INTO web_app_item VALUES (17, 'Womens Winter Socks', 'New womens'' winter socks.', 3);
INSERT INTO web_app_item VALUES (18, 'Cutlery', 'All cutlery welcome. Should be clean and considered usable by others.', 3);
INSERT INTO web_app_item VALUES (19, 'Sleeping Bag', 'Warm, durable & waterproof if possible.', 4);
INSERT INTO web_app_item VALUES (20, 'Toothbrush', 'Small travel toothbrush.', 4);
INSERT INTO web_app_item VALUES (21, 'Toothpaste', 'Small travel toothpaste.', 4);
INSERT INTO web_app_item VALUES (22, 'Mens Winter Socks', 'New mens'' winter socks.', 4);
INSERT INTO web_app_item VALUES (23, 'Womens Winter Socks', 'New womens'' winter sock.', 4);
INSERT INTO web_app_item VALUES (24, 'Cutlery', 'All cutlery welcome. Should be clean & considered usable by others.', 4);

SELECT pg_catalog.setval('web_app_item_id_seq', 24, true);

INSERT INTO web_app_organisation VALUES (1, 'Welcome Organisation', '/charities/welcome_organisation.png', 'Every year the Welcome Organisation assists around 1,300 individuals make their journey out of homelessness.', 1, 1, 1);
INSERT INTO web_app_organisation VALUES (2, 'St. Vincent de Paul', '/vincent.jpg', 'No work of charity is foreign to the society. Our work through person to person contact encompasses every form of aid that alleviates suffering and promotes the dignity of mankind. The society strives not only to alleviate need but also to discover and redress the situations which cause it. It services everyone in need, regardless of creed, opinion,colour, origin or caste.', 2, 2, 2);
INSERT INTO web_app_organisation VALUES (3, 'Council for the Homeless NI', '/chni.jpg', 'Founded in 1983, we are the sole representative organisation for those working with and supporting homeless people across Northern Ireland. We are the independent voice of the sector.', 3, 3, 3);
INSERT INTO web_app_organisation VALUES (4, 'Simon Community', '/charities/simon.png', 'Established in 1971 in response to a homelessness crisis in Belfast, Simon Community has grown to become Northern Ireland’s leading homelessness charity and service provider. From a beginning of just one house, two full time staff and a few volunteers in Belfast, Simon Community NI now helps over 3000 people every year across 22 projects throughout Northern Ireland with a staff count of 300 and 50 volunteers. We work without judgement to support people who are, or are at risk of, becoming homeless.', 4, 4, 4);

SELECT pg_catalog.setval('web_app_organisation_id_seq', 4, true);

INSERT INTO web_app_user VALUES (1, 'welcomeuser', 'welcomepassword', 1, 1);
INSERT INTO web_app_user VALUES (2, 'vincentuser', 'vincentpassword', 2, 2);
INSERT INTO web_app_user VALUES (3, 'counciluser', 'councilpassword', 3, 3);
INSERT INTO web_app_user VALUES (4, 'simonuser', 'simonpassword', 4, 4);

SELECT pg_catalog.setval('web_app_user_id_seq', 4, true);
SELECT pg_catalog.setval('web_app_wishlist_id_seq', 4, true);
