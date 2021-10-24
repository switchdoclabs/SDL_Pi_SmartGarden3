-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 24, 2021 at 09:52 AM
-- Server version: 10.3.22-MariaDB-0+deb10u1
-- PHP Version: 7.3.14-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `SmartGardenSystem`
--
CREATE DATABASE IF NOT EXISTS `SmartGardenSystem` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `SmartGardenSystem`;

-- --------------------------------------------------------

--
-- Table structure for table `BluetoothSensors`
--

DROP TABLE IF EXISTS `BluetoothSensors`;
CREATE TABLE IF NOT EXISTS `BluetoothSensors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lastchecked` datetime NOT NULL,
  `fulladdress` text NOT NULL,
  `pickaddress` text NOT NULL,
  `assignedwirelessid` text NOT NULL,
  `name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `IndoorTHSensors`
--

DROP TABLE IF EXISTS `IndoorTHSensors`;
CREATE TABLE IF NOT EXISTS `IndoorTHSensors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `DeviceID` int(11) NOT NULL,
  `ChannelID` int(11) NOT NULL,
  `Temperature` float NOT NULL,
  `Humidity` int(11) NOT NULL,
  `BatteryOK` text NOT NULL,
  `TimeRead` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Sensors`
--

DROP TABLE IF EXISTS `Sensors`;
CREATE TABLE IF NOT EXISTS `Sensors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` text NOT NULL,
  `SensorNumber` int(11) NOT NULL,
  `SensorValue` float NOT NULL,
  `SensorType` text NOT NULL,
  `TimeRead` datetime NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `SystemLog`
--

DROP TABLE IF EXISTS `SystemLog`;
CREATE TABLE IF NOT EXISTS `SystemLog` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Level` int(11) NOT NULL,
  `SystemText` text NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `ValveChanges`
--

DROP TABLE IF EXISTS `ValveChanges`;
CREATE TABLE IF NOT EXISTS `ValveChanges` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` varchar(10) NOT NULL,
  `ValveNumber` int(11) NOT NULL,
  `State` int(11) NOT NULL,
  `Source` text NOT NULL,
  `ValveType` text NOT NULL,
  `SecondsOn` int(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `ValveRecord`
--

DROP TABLE IF EXISTS `ValveRecord`;
CREATE TABLE IF NOT EXISTS `ValveRecord` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` varchar(10) NOT NULL,
  `State` varchar(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
