create type privilege as ENUM('admin', 'scheduler', 'medicalStaff', 'patient');
create type category as ENUM('Lab', 'MRI', 'Xray', 'Office Visit');


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
	rice decimal(6,2),
	cat category,
	primary key (ID)

);

create table patient (

	fname char()

);
