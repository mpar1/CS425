
create index timestamps on login(LoginTime,LogoutTime);
create index fullname on patient(fname,lname);
create index staff_fullname on employee(fname,lname);

create table Login (
	userID varchar(16),
	privilege varchar(12),
	LoginTime time,
	LogoutTime time,
	primary key (userID)
	check (privilege in ('admin', 'scheduler', 'medicalStaff', 'patient'))
);

create table Diagnostic (
	ID varchar(16),
	price decimal(6,2),
	category varchar(12),
	primary key (ID)
	check (category ('Lab', 'MRI', 'Xray', 'Office Visit'))
);

create table Patient (
	fname varchar(16),
	lname varchar(16),
	address varchar(16),
	patientID varchar(16)
);

create table Employee (
	fname varchar(16),
	lname varchar(16),
	staffID varchar(16),
	jobtype varchar(15),
	primary key (staffID)
	check (jobtype in ('Medical Staff', 'Admin', 'Scheduler'))
);

create table Order (
	orderID varchar(16),
	customerID varchar(16),
	staffID varchar(16),
	diagnosticID varchar(16),
	results text,
	primary key (orderID),
	foreign key (diagnosticID) references diagnostic(ID),
	foreign key (staffID) references employee(staffID)

);

create role admin;
create role scheduler;
create role medicalStaff;
create role patient;

grant select on Order to public;
grant insert on Order to medicalStaff;
grant select, update on Patient to medicalStaff;
grant insert on Patient to admin;
grant insert on Login to admin;

grant admin to
	select userID
	from Login
	where privilege = 'admin';
grant scheduler to
	select userID
	from Login
	where privilege = 'scheduler';
grant medicalStaff to
	select userID
	from Login
	where privilege = 'medicalStaff';
grant patient to
	select userID
	from Login
	where privilege = 'patient';

