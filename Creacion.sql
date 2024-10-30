

create table PERSONA(
idPersona INT NOT NULL auto_increment,
Nombre VARCHAR (50) NOT NULL,
Apellido varchar (50) NOT NULL,
Cumple DATETIME DEFAULT current_timestamp,
TipoPersonal VARCHAR (30) NOT NULL,
primary key (idPersona));

create table USUARIO(
idUsuario int not null auto_increment,
idPersona int not null,
foreign key (idPersona) references PERSONA (idPersona),
UserName varchar (50) NOT NULL,
Clave varchar (60) not null,
Estado INT NOT NULL,
CONSTRAINT chk_EstadoUSER CHECK (Estado BETWEEN 0 AND 1),
primary key (idUsuario));

create table ROL(
idRol INT NOT NULL AUTO_INCREMENT,
Descripcion VARCHAR (30),
PRIMARY KEY (idRol));

create table RoleUsuario(
idRol int not null,
foreign key (idRol) references ROL(idRol),
idUsuario int not null,
foreign key (idUsuario) references USUARIO(idUsuario));

create table CLIENTE(
idCliente int not null auto_increment,
idPersona int not null,
foreign key (idPersona) references PERSONA(idPersona),
Puntos int default 0 not null,
primary key (idCliente));

create table EMPLEADO(
idEmpleado int not null auto_increment,
idPersona int not null,
foreign key (idPersona) references PERSONA(idPersona),
FechaIngreso DATETIME DEFAULT current_timestamp,
Salario decimal (10,2),
primary key (idEmpleado));

create table ESTADO(
idEstado int not null auto_increment,
Descripcion varchar (30),
primary key (idEstado));

create table SERVICIO(
idServicio int  not null auto_increment not null,
Nombre varchar (30),
Descripcion varchar (255),
Precio decimal (10,2),
primary key (idServicio));

create table PRODUCTO(
idProducto int not null auto_increment,
Nombre varchar (30),
Descripcion varchar (255),
Precio decimal (10,2),
primary key (idProducto));

create table CITA(
idCita int not null auto_increment,
idCliente int not null,
foreign key (idCliente) references CLIENTE(idCliente),
idServicio int not null,
foreign key (idServicio) references SERVICIO(idServicio),
idEstado int not null,
foreign key (idEstado) references ESTADO(idEstado),
idProducto int not null,
foreign key (idProducto) references PRODUCTO(idProducto),
idEmpleado int not null,
foreign key (idEmpleado) references EMPLEADO(idEmpleado),
FechaCita date not null,
SesionInicio time not null,
SesionFin time,
Precio decimal (10, 2),
primary key (idCita))

