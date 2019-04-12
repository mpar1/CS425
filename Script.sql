create index timestamps on login(LoginTime,LogoutTime);
create index fullname on patient(fname,lname);
create index staff_fullname on employee(fname,lname);

create table login (
	userID varchar(16),
	privilege varchar(12),
	LoginTime time,
	LogoutTime time,
	primary key (userID),
	check (privilege in ('admin', 'scheduler', 'medicalStaff', 'patient'))
);

create table diagnostic (
	ID varchar(16),
	price decimal(6,2),
	category varchar(12),
	primary key (ID),
	check (category in ('Lab', 'MRI', 'Xray', 'Office Visit'))
);

create table patient (
	fname varchar(16),
	lname varchar(16),
	address varchar(16),
	patientID varchar(16)
);

create table Orders (
	orderID varchar(16),
	customerID varchar(16),
	staffID varchar(16),
	diagnosticID varchar(16),
	results text,
	primary key (orderID),
	foreign key (diagnosticID) references diagnostic(ID),
	foreign key (staffID) references employee(staffID)
);

create table employee (
	fname varchar(16),
	lname varchar(16),
	staffID varchar(16),
	jobtype varchar(15),
	primary key (staffID),
	check (jobtype in ('Medical Staff', 'Admin', 'Scheduler'))
);

create role admin;
create role scheduler;
create role medicalStaff;
create role patient;

grant select on Orders to public;
grant insert on Orders to medicalStaff;
grant select, update on patient to medicalStaff;
grant insert on patient to admin;
grant insert on login to admin;
