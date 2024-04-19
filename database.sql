CREATE TABLE `paczkomat` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `adres_paczkomatu` varchar(255),
  `czy_jest_paczka` bool,
  `paczka_id` int,
  `otworz` bool
);

CREATE TABLE `paczka` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `odbiorca_id` int,
  `nadawca_id` int,
  `paczkomat_id` int,
  `rozmiar` varchar(255),
  `waga` varchar(255),
  `haslo` varchar(255),
  `czy_paczka_odebrana` bool
);

CREATE TABLE `uzytkownik` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `imie_i_nazwisko` varchar(255),
  `email` varchar(255),
  `adres_uzytkownika` varchar(255)
);

ALTER TABLE `paczka` ADD FOREIGN KEY (`odbiorca_id`) REFERENCES `uzytkownik` (`id`);

ALTER TABLE `paczka` ADD FOREIGN KEY (`nadawca_id`) REFERENCES `uzytkownik` (`id`);

ALTER TABLE `paczka` ADD FOREIGN KEY (`paczkomat_id`) REFERENCES `paczkomat` (`id`);
