USE [master]
GO
/****** Object:  Database [u_szkola]    Script Date: 14/12/2021 18:13:04 ******/
CREATE DATABASE [u_szkola]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'u_szkola', FILENAME = N'/var/opt/mssql/data/u_szkola.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'u_szkola_log', FILENAME = N'/var/opt/mssql/data/u_szkola_log.ldf' , SIZE = 66048KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [u_szkola] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [u_szkola].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [u_szkola] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [u_szkola] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [u_szkola] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [u_szkola] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [u_szkola] SET ARITHABORT OFF 
GO
ALTER DATABASE [u_szkola] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [u_szkola] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [u_szkola] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [u_szkola] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [u_szkola] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [u_szkola] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [u_szkola] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [u_szkola] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [u_szkola] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [u_szkola] SET  ENABLE_BROKER 
GO
ALTER DATABASE [u_szkola] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [u_szkola] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [u_szkola] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [u_szkola] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [u_szkola] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [u_szkola] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [u_szkola] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [u_szkola] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [u_szkola] SET  MULTI_USER 
GO
ALTER DATABASE [u_szkola] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [u_szkola] SET DB_CHAINING OFF 
GO
ALTER DATABASE [u_szkola] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [u_szkola] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [u_szkola] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [u_szkola] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [u_szkola] SET QUERY_STORE = OFF
GO
USE [u_szkola]
GO
/****** Object:  Table [dbo].[Bibliotekarz]    Script Date: 14/12/2021 18:13:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Bibliotekarz](
	[id_bibliotekarza] [int] IDENTITY(1,1) NOT NULL,
	[imie] [nvarchar](50) NULL,
	[nazwisko] [nvarchar](50) NULL,
	[login] [nvarchar](50) NULL,
	[haslo] [nvarchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[id_bibliotekarza] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Czytelnik]    Script Date: 14/12/2021 18:13:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Czytelnik](
	[id_czytelnika] [int] IDENTITY(1,1) NOT NULL,
	[imie] [nvarchar](50) NULL,
	[nazwisko] [nvarchar](50) NULL,
	[login] [nvarchar](50) NULL,
	[haslo] [nvarchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[id_czytelnika] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Ksiazka]    Script Date: 14/12/2021 18:13:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Ksiazka](
	[id_ksiazki] [int] IDENTITY(1,1) NOT NULL,
	[tytul] [nvarchar](50) NULL,
	[autor] [nvarchar](50) NULL,
	[na_stanie] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id_ksiazki] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Rezerwacja]    Script Date: 14/12/2021 18:13:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Rezerwacja](
	[id_rezerwacji] [int] IDENTITY(1,1) NOT NULL,
	[id_ksiazki] [int] NULL,
	[id_czytelnika] [int] NULL,
	[tytul] [nvarchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[id_rezerwacji] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Wypozyczone]    Script Date: 14/12/2021 18:13:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Wypozyczone](
	[id_wypozyczenia] [int] IDENTITY(1,1) NOT NULL,
	[id_ksiazki] [int] NULL,
	[id_czytelnika] [int] NULL,
	[tytul] [nvarchar](50) NULL,
	[max_termin_oddania] [date] NULL,
	[prolongacja] [bit] NULL,
	[zwrocone] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[id_wypozyczenia] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Rezerwacja]  WITH CHECK ADD  CONSTRAINT [FK_Rezerwacja_Czytelnik] FOREIGN KEY([id_czytelnika])
REFERENCES [dbo].[Czytelnik] ([id_czytelnika])
GO
ALTER TABLE [dbo].[Rezerwacja] CHECK CONSTRAINT [FK_Rezerwacja_Czytelnik]
GO
ALTER TABLE [dbo].[Rezerwacja]  WITH CHECK ADD  CONSTRAINT [FK_Rezerwacja_Ksiazka] FOREIGN KEY([id_ksiazki])
REFERENCES [dbo].[Ksiazka] ([id_ksiazki])
GO
ALTER TABLE [dbo].[Rezerwacja] CHECK CONSTRAINT [FK_Rezerwacja_Ksiazka]
GO
ALTER TABLE [dbo].[Wypozyczone]  WITH CHECK ADD  CONSTRAINT [FK_Wypozyczone_Czytelnik] FOREIGN KEY([id_czytelnika])
REFERENCES [dbo].[Czytelnik] ([id_czytelnika])
GO
ALTER TABLE [dbo].[Wypozyczone] CHECK CONSTRAINT [FK_Wypozyczone_Czytelnik]
GO
ALTER TABLE [dbo].[Wypozyczone]  WITH CHECK ADD  CONSTRAINT [FK_Wypozyczone_Ksiazka] FOREIGN KEY([id_ksiazki])
REFERENCES [dbo].[Ksiazka] ([id_ksiazki])
GO
ALTER TABLE [dbo].[Wypozyczone] CHECK CONSTRAINT [FK_Wypozyczone_Ksiazka]
GO
USE [master]
GO
ALTER DATABASE [u_szkola] SET  READ_WRITE 
GO
