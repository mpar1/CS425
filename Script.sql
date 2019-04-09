create type privilege as ENUM('admin', 'scheduler', 'medicalStaff', 'patient');
create type category as ENUM('Lab', 'MRI', 'Xray', 'Office Visit');
create type jobtype as ENUM('Medical Staff', 'Admin', 'Scheduler');

create table login (

	userID varchar(16),
	/*privilege ,
	*/
	priv privilege,
	LoginTime time,
	LogoutTime time,
	primary key (userID)

);

create table diagnostic (

	ID varchar(16),
	price decimal(6,2),
	cat category,
	primary key (ID)

);

create table patient (

	fname varchar(16),
	lname varchar(16),
	address varchar(16),
	patientID varchar(16)

);

create table employee (

	fname varchar(16),
	lname varchar(16),
	staffID varchar(16),
	job jobtype,
	primary key (staffID)

);

create table ord (

	orderID varchar(16),
	customerID varchar(16),
	staffID varchar(16),
	diagnosticID varchar(16),
	results text,
	primary key (orderID),
	foreign key (diagnosticID) references diagnostic(ID) 

);
