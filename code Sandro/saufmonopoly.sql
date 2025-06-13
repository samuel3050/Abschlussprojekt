-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 10. Jun 2025 um 15:39
-- Server-Version: 10.4.32-MariaDB
-- PHP-Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `saufmonopoly`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `spielfelder`
--

CREATE TABLE `spielfelder` (
  `feld_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `typ` enum('Straße','Bahnhof','Ereignis','Gemeinschaft','Frei Parken','Gefängnis','Los','Steuer','Werk','Spezial') NOT NULL,
  `kaufpreis` varchar(20) DEFAULT NULL,
  `miete` varchar(20) DEFAULT NULL,
  `farbe` varchar(20) DEFAULT NULL,
  `alkohol_typ` enum('Bier','Schnaps','Shot','Wein','Mixgetränk','Kater','Wasser','Joker') NOT NULL,
  `alkohol_menge` varchar(20) NOT NULL,
  `zusatz_regel` varchar(100) DEFAULT NULL,
  `besitzer` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Daten für Tabelle `spielfelder`
--

-- Eckfelder (Special-Felder ohne Alkohol oder Joker)
INSERT INTO `spielfelder` (`feld_id`, `name`, `typ`, `kaufpreis`, `miete`, `farbe`, `alkohol_typ`, `alkohol_menge`, `zusatz_regel`, `besitzer`) VALUES
(1, 'Los', 'Los', NULL, NULL, NULL, 'Wasser', '0', 'Starthilfe: 1 Schluck Bier', NULL),
(10, 'Alkohol-Joker', 'Spezial', NULL, NULL, 'Rainbow', 'Joker', '0', 'Wähle einen beliebigen Alkoholtyp', NULL),
(20, 'Hydrations-Station', 'Spezial', NULL, NULL, 'Blau', 'Wasser', '0', 'Trinke Wasser - überspringe nächsten Shot', NULL),
(30, 'Kater-Polizei', 'Spezial', NULL, NULL, 'Rot', 'Wasser', '0', 'Wenn du betrunken bist: 1 Runde Pause', NULL);

-- Fields 2-9: Wein und Bier (Rot und Gelb)
INSERT INTO `spielfelder` (`feld_id`, `name`, `typ`, `kaufpreis`, `miete`, `farbe`, `alkohol_typ`, `alkohol_menge`, `zusatz_regel`, `besitzer`) VALUES
(2, 'Biergasse 1', 'Straße', '2 Schlucke', '1 Schluck', 'Gelb', 'Bier', '1 Schluck', NULL, 'Lorenz'),
(3, 'Inndrinks', 'Straße', '3 Schlucke', '2 Schlucke', 'Gelb', 'Bier', '2 Schlucke', 'Sie bringen dir ein neues Bier', NULL),
(4, 'HTL Anichstrasse', 'Gemeinschaft', NULL, NULL, NULL, 'Bier', '0', 'Würfel bestimmt Menge', NULL),
(5, 'Weinberg', 'Straße', '1 Glas', '3 Schlucke', 'Rot', 'Wein', '1 Glas', NULL, NULL),
(6, 'Sektempfang', 'Straße', '3 Schlücke', '2 Schlücke', 'Rot', 'Wein', '2 Gläser', NULL, NULL),
(7, 'Magic', 'Gemeinschaft', NULL, NULL, NULL, '', '0', 'Gönn dir mal eine Pause', NULL),
(8, 'Ereignisfeld', 'Ereignis', NULL, NULL, NULL, 'Shot', '1', 'Karte ziehen: Würfel entscheidet', NULL),
(9, 'Bierpalast', 'Straße', '5 Schlucke', '3 Schlucke', 'Gelb', 'Bier', '3 Schlucke', NULL, NULL);

-- Fields 11-19: Mixgetränke (Grün und Blau)
INSERT INTO `spielfelder` (`feld_id`, `name`, `typ`, `kaufpreis`, `miete`, `farbe`, `alkohol_typ`, `alkohol_menge`, `zusatz_regel`, `besitzer`) VALUES
(11, 'Longdrink-Meile', 'Straße', '6 Schlucke', '5 Schlucke', 'Grün', 'Mixgetränk', '5 Schlucke', NULL, NULL),
(12, 'Cocktail-Straße', 'Straße', '1 Glas', '1 Glas', 'Grün', 'Mixgetränk', '1 Glas', NULL, NULL),
(13, 'Gemeinschaft', 'Gemeinschaft', NULL, NULL, NULL, 'Mixgetränk', '3 Schlucke', NULL, NULL),
(14, 'Frei Parken', 'Frei Parken', NULL, NULL, NULL, 'Wasser', '0', 'Hydrationspause: 1 Runde aussetzen', NULL),
(15, 'Wasserwerk', 'Werk', '1 Glas Wasser', NULL, NULL, 'Wasser', '1 Glas', NULL, NULL),
(16, 'Tiki-Bar', 'Spezial', NULL, '4 Schlücke', NULL, 'Mixgetränk', '4 Schlucke', 'Alle trinken 1 Schluck', NULL),
(17, 'Gin-Allee', 'Straße', '5 cl', '2 cl', 'Blau', 'Mixgetränk', '2 cl', NULL, NULL),
(18, 'Whiskey-Platz', 'Straße', '6 cl', '3 cl', 'Blau', 'Mixgetränk', '3 cl', NULL, NULL),
(19, 'Sektbar', 'Straße', '3 Gläser', '2 Gläser', 'Blau', 'Mixgetränk', '2 Gläser', NULL, NULL);

-- Fields 21-29: Wein und Bier (Braun und Grau)
INSERT INTO `spielfelder` (`feld_id`, `name`, `typ`, `kaufpreis`, `miete`, `farbe`, `alkohol_typ`, `alkohol_menge`, `zusatz_regel`, `besitzer`) VALUES
(21, 'Bozner-Platz', 'Straße', '4 Schlücke', '3 Schlücke', 'Braun', 'Wein', '3 Gläser', NULL, NULL),
(22, 'Kater-Gasse', 'Straße', 'Volles Glas', 'Mixgetränk ex', 'Braun', 'Kater', 'Alles', NULL, NULL),
(23, 'Gefängnis', 'Gefängnis', NULL, '3 Shots', NULL, 'Shot', '3', 'Nachzahlung oder Pause', NULL),
(24, 'Hangover-Platz', 'Straße', 'Nachschlag', 'Nachschlag', 'Grau', 'Kater', 'Nachschlag', NULL, NULL),
(25, 'Mausefalle', 'Straße', 'Volles Glas', '10 Schlücke', 'Grau', 'Kater', 'Volles Glas', NULL, NULL),
(26, 'Supermarkt', 'Werk', '1 Liter Wasser', NULL, NULL, 'Wasser', '1 Liter', 'Katerprophylaxe: 2 Runden Schutz', NULL),
(27, 'Ereignisfeld', 'Ereignis', NULL, NULL, NULL, 'Shot', '1', NULL, NULL),
(28, 'Ereignisfeld', 'Ereignis', NULL, NULL, NULL, 'Shot', '2', NULL, NULL),
(29, 'Katerklinik', 'Spezial', NULL, NULL, NULL, 'Wasser', '0', 'Heilt 1 Kater-Runde', NULL);

-- Fields 31-39: Shots und Schnäpse (Pink und Orange)
INSERT INTO `spielfelder` (`feld_id`, `name`, `typ`, `kaufpreis`, `miete`, `farbe`, `alkohol_typ`, `alkohol_menge`, `zusatz_regel`, `besitzer`) VALUES
(31, 'Vodka-Strasse', 'Straße', '3 cl', '2 cl', 'Pink', 'Schnaps', '2 cl', NULL, NULL),
(32, 'Rum-Meile', 'Straße', '4 cl', '3 cl', 'Pink', 'Schnaps', '3 cl', NULL, NULL),
(33, 'Tequila-Kreuzung', 'Straße', '2 Shots', '1 Shot', 'Orange', 'Shot', '1', NULL, NULL),
(34, 'Absinth-Allee', 'Straße', '3 Shots', '2 Shots', 'Orange', 'Shot', '2', NULL, NULL),
(35, 'Kuppenweg 20', 'Straße', '8 cl', '4 cl', 'Pink', 'Schnaps', '4 cl', NULL, NULL),
(36, 'Whiskey-Brücke', 'Straße', '7 cl', '4 cl', 'Orange', 'Schnaps', '4 cl', NULL, NULL),
(37, 'Vodka-Bahnhof', 'Bahnhof', '6 cl', '3 Shots', NULL, 'Schnaps', '3 cl', NULL, NULL),
(38, 'Sake-Bahnhof', 'Bahnhof', '5 cl', '2 Shots', NULL, 'Schnaps', '2 cl', NULL, NULL),
(39, 'Steuer', 'Steuer', NULL, '4 Schlucke', NULL, 'Bier', '4 Schlucke', 'An alle verteilen', NULL),
(40, 'Endspurt', 'Spezial', NULL, NULL, NULL, 'Shot', '3', 'Letzter Spieler trinkt doppelt', NULL);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `spielfelder`
--
ALTER TABLE `spielfelder`
  ADD PRIMARY KEY (`feld_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;