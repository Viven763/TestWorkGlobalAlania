create table auth
(
	uuid uuid,
	user_uuid uuid,
	access_token text,
	expire timestamp with time zone
);

create table users
(
	uuid uuid,
	login text not null
		unique,
	pswd text,
	fio text,
	status integer
		constraint users_status_check
			check ((status >= 0) AND (status <= 3))
);

create table equipment_list
(
	uuid uuid unique not null,
	ip_address text,
	description text
);

create table terminal_list
(
	uuid uuid,
	device_uuid uuid
		references equipment_list (uuid),
	mac text,
	model text,
	dt_created timestamp with time zone,
	dt_last_pool timestamp with time zone default null
);

