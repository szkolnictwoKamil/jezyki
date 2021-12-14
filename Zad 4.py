import pyodbc

server = 'dbmanage.lab.ki.agh.edu.pl'
database = 'u_szkola'
user = 'u_szkola'
Password = '*****'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                       SERVER=' + server + '; \
                       DATABASE=' + database + ';\
                       UID=' + user + '; \
                       PWD=' + Password)


def menu(info, options, functions, special_option, special_function):
    assert len(options) == len(functions)

    def display_menu():

        for ind, option in enumerate(options, start=1):
            print(f"{ind}. {option}")
        if special_option:
            print(f"0. {special_option}")

    while True:
        print(info)
        display_menu()
        try:
            decision = int(input("> "))
            if decision in range(1, len(options) + 1):
                functions[decision - 1]()

            elif decision == 0 and special_option:
                return special_function()
            else:
                print("Spróbuj jeszcze raz.")
            print("\n Proszę wykonać kolejną operację.")
        except ValueError:
            print(f"Podaj liczbę od 1 do {len(options)}")


def wypozycz():
    cursor = cnxn.cursor()
    w = cursor.execute(f'''
                        select id_ksiazki from Ksiazka where na_stanie > 0
                                    ''').fetchall()
    list = []
    for element in w:
        list.append(int(element[0]))
    try:
        id_ksiazki = int(input("Podaj id książki:"))
        if id_ksiazki in list:
            cursor.execute(f'''
                                          UPDATE Ksiazka
                                          SET na_stanie = na_stanie - 1
                                          WHERE id_ksiazki = {id_ksiazki}
                                                ''')
            cursor.execute(f'''
                        INSERT INTO Wypozyczone (id_ksiazki, id_czytelnika, tytul, max_termin_oddania,Prolongacja, Zwrocone)
                        VALUES
                            ({id_ksiazki},{c_userid}, (select tytul from Ksiazka where id_ksiazki = {id_ksiazki}) , DATEADD(month, 3, GETDATE()),0,0)
                                ''')
        else:
            print("Książki nie ma na stanie, ale możesz ją zarezerwować.")
    except ValueError:
        print("Proszę podać liczbę!")

    cursor.commit()
    cursor.close()

def zarezerwuj():
    cursor = cnxn.cursor()
    w = cursor.execute(f'''
                            select id_ksiazki from Ksiazka where na_stanie = 0
                                        ''').fetchall()
    list = []
    for element in w:
        list.append(int(element[0]))
    try:
        id_ksiazki = int(input("Podaj id książki:"))
        if id_ksiazki in list:

            cursor.execute(f'''
                                INSERT INTO rezerwacja (id_ksiazki, id_czytelnika, tytul)
                                VALUES
                                    ({id_ksiazki},{c_userid}, (select tytul from Ksiazka where id_ksiazki = {id_ksiazki}))
                                        ''')
        else:
            print("Nie można zarezerwować książki.")
    except ValueError:
        print("Proszę podać liczbę!")
    cursor.commit()
    cursor.close()

def prolonguj():
    cursor = cnxn.cursor()
    try:
        id_wypozyczenia = int(input("Podaj id wypozyczenia:"))

        w = cursor.execute(f'''
                                    select prolongacja from wypozyczone where id_wypozyczenia = {id_wypozyczenia}
                                                ''').fetchone()

        if int(w[0]) == 0: #nie zostało wcześniej prolongowane
            cursor.execute(f'''
                            UPDATE wypozyczone
                            SET max_termin_oddania = DATEADD(day, 14, max_termin_oddania), 
                            prolongacja = 1
                            WHERE  id_wypozyczenia = {id_wypozyczenia}
                            ''')
        else:
            print("Maksymalna liczba prolongacji została wykorzystana.")

    except ValueError:
        print("Proszę podać liczbę!")
    cursor.commit()
    cursor.close()

def Wyjdz():
    print("Wychodzisz z okna.")


def Zwroc():
    cursor = cnxn.cursor()
    try:
        id_wypozyczenia = int(input("Podaj id wypozyczenia:"))

        w = cursor.execute(f'''
                                    select Zwrocone from wypozyczone where id_wypozyczenia = {id_wypozyczenia}
                                                ''').fetchone()
        if int(w[0]) == 0:
            cursor.execute(f'''
                              UPDATE wypozyczone
                              SET Zwrocone = 1
                              WHERE id_wypozyczenia = {id_wypozyczenia}
                                    ''')

            cursor.execute(f'''
                                UPDATE Ksiazka
                                SET na_stanie = na_stanie + 1
                                WHERE id_ksiazki = (select id_ksiazki from wypozyczone where id_wypozyczenia = {id_wypozyczenia})
                                        ''')
        else:
            print("Książka została już zwrócona.")
    except ValueError:
        print("Proszę podać liczbę!")
    cursor.commit()
    cursor.close()

def dodaj_ksiazke():
    cursor = cnxn.cursor()
    tytul = input("Podaj tytuł książki:")
    autor = input("Podaj autora książki:")
    stan = input("Podaj liczbę dostarczonych egzemplarzy: ")

    cursor.execute(f'''
                INSERT INTO Ksiazka (tytul, autor, na_stanie)
                VALUES
                    ('{tytul}','{autor}', '{stan}')
                        ''')
    cursor.commit()
    cursor.close()

def usun_ksiazke():
    cursor = cnxn.cursor()
    id_ksiazki = int(input("Podaj id książki:"))

    cursor.execute(f'''
    UPDATE
    Ksiazka
    SET
    na_stanie = na_stanie - 1
    WHERE
    id_ksiazki = {id_ksiazki}
            ''')
    cursor.commit()
    cursor.close()

def dodaj_uzytkownika():
    cursor = cnxn.cursor()
    tabela = input("Bibliotekarz/Czytelnik?")
    imie = input("Podaj imię użytkownika:")
    nazwisko = input("Podaj nazwisko użytkownika:")
    login = input("Podaj login użytkownika: ")
    haslo = input("Podaj hasło użytkownika: ")

    cursor.execute(f'''
            INSERT INTO {tabela} (imie, nazwisko, login, haslo)
            VALUES
                ('{imie}','{nazwisko}', '{login}', '{haslo}')
                    ''')
    cursor.commit()
    cursor.close()


def katalog():
    print("Książki w systemie:")
    cursor = cnxn.cursor()
    katalog = cursor.execute("""select distinct tytul from Ksiazka """).fetchall()

    for ind, element in enumerate(katalog, start=1):
        print(f"{ind}. {element[0]}")
    cursor.close()


def wyszukaj():
    cursor = cnxn.cursor()
    wpis = input('Proszę wpisać tytuł, autora lub słowo klucz: ')
    katalog = cursor.execute(
        f"""select * from Ksiazka where tytul like '%{wpis}%' or autor like '%{wpis}%' """).fetchall()
    print("Pasujące wyniki w postaci (id książki, tytuł, autor, liczba sztuk na stanie):")
    for ind, element in enumerate(katalog, start=1):
        print(f"{ind}. {element}")

    cursor.close()


def b_logowanie():
    try:

        log_result = logowanie('id_bibliotekarza', 'Bibliotekarz')
        global userid
        userid = log_result[0]
        decision = menu("Proszę wybrać opcję:",
                        ["Wyświetl katalog.", "Zwróć Książkę.", "Dodaj nową książkę.", "Usuń książkę.", "Dodaj użytkownika.",
                         "Wyszukaj."],
                        [katalog, Zwroc, dodaj_ksiazke, usun_ksiazke, dodaj_uzytkownika, wyszukaj], "Wstecz", Wyjdz)
    except TypeError:
        print("Błędny login lub hasło. Spróbuj ponownie")


def c_logowanie():
    try:
        log_result = logowanie('id_czytelnika', 'Czytelnik')
        global c_userid

        c_userid = log_result[0]
        decision = menu("Proszę wybrać opcję:",
                        ["Zobacz katalog.", "Wypożycz książkę.", "Zarezerwuj książkę.", "Przedłuż wypożyczenie.",
                         "Wyszukaj."],
                        [katalog, wypozycz, zarezerwuj, prolonguj, wyszukaj], "Wstecz", Wyjdz)

    except TypeError:
        print("Błędny login lub hasło. Spróbuj ponownie")


def logowanie(id_name, table_name):
    cursor = cnxn.cursor()
    login = input("Podaj login: ")
    haslo = input("Podaj hasło: ")

    cursor.execute(f"select {id_name}, haslo from {table_name} where login like '{login}' and haslo like '{haslo}'")
    user = cursor.fetchone()

    cursor.close()
    return user


logowanie = menu("Proszę wybrać użytkownika do logowania.", ["Bibliotekarz", "Czytelnik"], [b_logowanie, c_logowanie],
                 "Wyjdź", Wyjdz)



# Tworzenie tabel

# USE [master]
# GO
# /****** Object:  Database [u_szkola]    Script Date: 14/12/2021 18:13:04 ******/
# CREATE DATABASE [u_szkola]
#  CONTAINMENT = NONE
#  ON  PRIMARY
# ( NAME = N'u_szkola', FILENAME = N'/var/opt/mssql/data/u_szkola.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
#  LOG ON
# ( NAME = N'u_szkola_log', FILENAME = N'/var/opt/mssql/data/u_szkola_log.ldf' , SIZE = 66048KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
#  WITH CATALOG_COLLATION = DATABASE_DEFAULT
# GO
# ALTER DATABASE [u_szkola] SET COMPATIBILITY_LEVEL = 150
# GO
# IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
# begin
# EXEC [u_szkola].[dbo].[sp_fulltext_database] @action = 'enable'
# end
# GO
# ALTER DATABASE [u_szkola] SET ANSI_NULL_DEFAULT OFF
# GO
# ALTER DATABASE [u_szkola] SET ANSI_NULLS OFF
# GO
# ALTER DATABASE [u_szkola] SET ANSI_PADDING OFF
# GO
# ALTER DATABASE [u_szkola] SET ANSI_WARNINGS OFF
# GO
# ALTER DATABASE [u_szkola] SET ARITHABORT OFF
# GO
# ALTER DATABASE [u_szkola] SET AUTO_CLOSE OFF
# GO
# ALTER DATABASE [u_szkola] SET AUTO_SHRINK OFF
# GO
# ALTER DATABASE [u_szkola] SET AUTO_UPDATE_STATISTICS ON
# GO
# ALTER DATABASE [u_szkola] SET CURSOR_CLOSE_ON_COMMIT OFF
# GO
# ALTER DATABASE [u_szkola] SET CURSOR_DEFAULT  GLOBAL
# GO
# ALTER DATABASE [u_szkola] SET CONCAT_NULL_YIELDS_NULL OFF
# GO
# ALTER DATABASE [u_szkola] SET NUMERIC_ROUNDABORT OFF
# GO
# ALTER DATABASE [u_szkola] SET QUOTED_IDENTIFIER OFF
# GO
# ALTER DATABASE [u_szkola] SET RECURSIVE_TRIGGERS OFF
# GO
# ALTER DATABASE [u_szkola] SET  ENABLE_BROKER
# GO
# ALTER DATABASE [u_szkola] SET AUTO_UPDATE_STATISTICS_ASYNC OFF
# GO
# ALTER DATABASE [u_szkola] SET DATE_CORRELATION_OPTIMIZATION OFF
# GO
# ALTER DATABASE [u_szkola] SET TRUSTWORTHY OFF
# GO
# ALTER DATABASE [u_szkola] SET ALLOW_SNAPSHOT_ISOLATION OFF
# GO
# ALTER DATABASE [u_szkola] SET PARAMETERIZATION SIMPLE
# GO
# ALTER DATABASE [u_szkola] SET READ_COMMITTED_SNAPSHOT OFF
# GO
# ALTER DATABASE [u_szkola] SET HONOR_BROKER_PRIORITY OFF
# GO
# ALTER DATABASE [u_szkola] SET RECOVERY SIMPLE
# GO
# ALTER DATABASE [u_szkola] SET  MULTI_USER
# GO
# ALTER DATABASE [u_szkola] SET PAGE_VERIFY CHECKSUM
# GO
# ALTER DATABASE [u_szkola] SET DB_CHAINING OFF
# GO
# ALTER DATABASE [u_szkola] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF )
# GO
# ALTER DATABASE [u_szkola] SET TARGET_RECOVERY_TIME = 60 SECONDS
# GO
# ALTER DATABASE [u_szkola] SET DELAYED_DURABILITY = DISABLED
# GO
# ALTER DATABASE [u_szkola] SET ACCELERATED_DATABASE_RECOVERY = OFF
# GO
# ALTER DATABASE [u_szkola] SET QUERY_STORE = OFF
# GO
# USE [u_szkola]
# GO
# /****** Object:  Table [dbo].[Bibliotekarz]    Script Date: 14/12/2021 18:13:05 ******/
# SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
# CREATE TABLE [dbo].[Bibliotekarz](
# 	[id_bibliotekarza] [int] IDENTITY(1,1) NOT NULL,
# 	[imie] [nvarchar](50) NULL,
# 	[nazwisko] [nvarchar](50) NULL,
# 	[login] [nvarchar](50) NULL,
# 	[haslo] [nvarchar](50) NULL,
# PRIMARY KEY CLUSTERED
# (
# 	[id_bibliotekarza] ASC
# )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
# ) ON [PRIMARY]
# GO
# /****** Object:  Table [dbo].[Czytelnik]    Script Date: 14/12/2021 18:13:05 ******/
# SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
# CREATE TABLE [dbo].[Czytelnik](
# 	[id_czytelnika] [int] IDENTITY(1,1) NOT NULL,
# 	[imie] [nvarchar](50) NULL,
# 	[nazwisko] [nvarchar](50) NULL,
# 	[login] [nvarchar](50) NULL,
# 	[haslo] [nvarchar](50) NULL,
# PRIMARY KEY CLUSTERED
# (
# 	[id_czytelnika] ASC
# )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
# ) ON [PRIMARY]
# GO
# /****** Object:  Table [dbo].[Ksiazka]    Script Date: 14/12/2021 18:13:05 ******/
# SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
# CREATE TABLE [dbo].[Ksiazka](
# 	[id_ksiazki] [int] IDENTITY(1,1) NOT NULL,
# 	[tytul] [nvarchar](50) NULL,
# 	[autor] [nvarchar](50) NULL,
# 	[na_stanie] [int] NULL,
# PRIMARY KEY CLUSTERED
# (
# 	[id_ksiazki] ASC
# )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
# ) ON [PRIMARY]
# GO
# /****** Object:  Table [dbo].[Rezerwacja]    Script Date: 14/12/2021 18:13:05 ******/
# SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
# CREATE TABLE [dbo].[Rezerwacja](
# 	[id_rezerwacji] [int] IDENTITY(1,1) NOT NULL,
# 	[id_ksiazki] [int] NULL,
# 	[id_czytelnika] [int] NULL,
# 	[tytul] [nvarchar](50) NULL,
# PRIMARY KEY CLUSTERED
# (
# 	[id_rezerwacji] ASC
# )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
# ) ON [PRIMARY]
# GO
# /****** Object:  Table [dbo].[Wypozyczone]    Script Date: 14/12/2021 18:13:05 ******/
# SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
# CREATE TABLE [dbo].[Wypozyczone](
# 	[id_wypozyczenia] [int] IDENTITY(1,1) NOT NULL,
# 	[id_ksiazki] [int] NULL,
# 	[id_czytelnika] [int] NULL,
# 	[tytul] [nvarchar](50) NULL,
# 	[max_termin_oddania] [date] NULL,
# 	[prolongacja] [bit] NULL,
# 	[zwrocone] [bit] NULL,
# PRIMARY KEY CLUSTERED
# (
# 	[id_wypozyczenia] ASC
# )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
# ) ON [PRIMARY]
# GO
# ALTER TABLE [dbo].[Rezerwacja]  WITH CHECK ADD  CONSTRAINT [FK_Rezerwacja_Czytelnik] FOREIGN KEY([id_czytelnika])
# REFERENCES [dbo].[Czytelnik] ([id_czytelnika])
# GO
# ALTER TABLE [dbo].[Rezerwacja] CHECK CONSTRAINT [FK_Rezerwacja_Czytelnik]
# GO
# ALTER TABLE [dbo].[Rezerwacja]  WITH CHECK ADD  CONSTRAINT [FK_Rezerwacja_Ksiazka] FOREIGN KEY([id_ksiazki])
# REFERENCES [dbo].[Ksiazka] ([id_ksiazki])
# GO
# ALTER TABLE [dbo].[Rezerwacja] CHECK CONSTRAINT [FK_Rezerwacja_Ksiazka]
# GO
# ALTER TABLE [dbo].[Wypozyczone]  WITH CHECK ADD  CONSTRAINT [FK_Wypozyczone_Czytelnik] FOREIGN KEY([id_czytelnika])
# REFERENCES [dbo].[Czytelnik] ([id_czytelnika])
# GO
# ALTER TABLE [dbo].[Wypozyczone] CHECK CONSTRAINT [FK_Wypozyczone_Czytelnik]
# GO
# ALTER TABLE [dbo].[Wypozyczone]  WITH CHECK ADD  CONSTRAINT [FK_Wypozyczone_Ksiazka] FOREIGN KEY([id_ksiazki])
# REFERENCES [dbo].[Ksiazka] ([id_ksiazki])
# GO
# ALTER TABLE [dbo].[Wypozyczone] CHECK CONSTRAINT [FK_Wypozyczone_Ksiazka]
# GO
# USE [master]
# GO
# ALTER DATABASE [u_szkola] SET  READ_WRITE
# GO


# Dane do tabel

# INSERT
# INTO
# Czytelnik(id_czytelnika, imie, nazwisko, login, haslo)
# VALUES
# (1, 'Karol', 'Waniszko', 'kwaniszko@czyt.pl', 'rurza4652'),
# (2, 'Arnold', 'Duralełko', 'Misiaczek@czyt.pl', 'tarnowskiegory12'),
# (3, 'Anna', 'Gumiś', 'Gumiszella@czyt.pl', 'haslo1234')
#
# INSERT
# INTO
# Bibliotekarz(id_bibliotekarza, imie, nazwisko, login, haslo)
# VALUES
# ('Kasia', 'Nursery', 'kolanko', 'nurserytonieja'),
# ('Hanna', 'Tabaszewska', 'Hansolo', '1234')
#
# INSERT
# INTO
# Książka(id_ksiazki, tytul, autor, na_stanie)
# VALUES
# ('W pustyni i w puszczy', 'Henryk Sienkiewicz', 9),
# ('Duma i uprzedzenie', 'Jane Austen', 1),
# ('Zbiry uciekaja a cukinia rośnie', 'Robert Lewandowski', 0),
# ('Romeo i Julia', 'William Shakespeare', 10),
# ('Atobiografia Karoliny Robakowskiej', 'Karolina Robakowska', 2),
# ('Hamlet', 'William Shakespeare', 6)
#
# INSERT
# INTO
# Wypozyczone(id_ksiazki, id_czytelnika, tytul, max_termin_oddania, prolongacja, zwrocone)
# VALUES
# (1, 2, 'W pustyni i w puszczy', 2022 - 02 - 01, 1, 1),
# (3, 2, 'Zbiry uciekaja a cukinia rosnie', 2022 - 03 - 29, 1, 0),
#
# INSERT
# INTO
# rezerwacja(id_ksiazki, id_czytelnika, tytul)
# VALUES
# (3, 3, 'Zbiry uciekaja a cukinia rosnie')
