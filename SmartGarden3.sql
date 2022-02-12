-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 11, 2022 at 03:59 PM
-- Server version: 10.3.31-MariaDB-0+deb10u1
-- PHP Version: 7.3.31-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `SmartGarden3`
--
CREATE DATABASE IF NOT EXISTS `SmartGarden3` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `SmartGarden3`;

-- --------------------------------------------------------

--
-- Table structure for table `Alarms`
--

CREATE TABLE IF NOT EXISTS `Alarms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timemodified` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `bluetooth` text NOT NULL,
  `hydroponics` text NOT NULL,
  `address` text DEFAULT NULL,
  `moisturealarm` text NOT NULL,
  `moistureminimum` int(11) NOT NULL,
  `moisturemaximum` int(11) NOT NULL,
  `temperaturealarm` text NOT NULL,
  `temperatureminimum` int(11) NOT NULL,
  `temperaturemaximum` int(11) NOT NULL,
  `lasttriggered` datetime DEFAULT NULL,
  `triggerlimit` int(11) NOT NULL,
  `triggercount` int(11) NOT NULL,
  `emailnotification` text NOT NULL,
  `textnotification` text NOT NULL,
  `currentmoisture` int(11) DEFAULT NULL,
  `currenttemperature` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `BluetoothSensorData`
--

CREATE TABLE IF NOT EXISTS `BluetoothSensorData` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` text NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `MacAddress` text NOT NULL,
  `PickAddress` text NOT NULL,
  `Temperature` float NOT NULL,
  `Brightness` int(11) NOT NULL,
  `Moisture` int(11) NOT NULL,
  `Conductivity` int(11) NOT NULL,
  `Battery` int(11) NOT NULL,
  `SensorType` text NOT NULL,
  `TimeRead` text NOT NULL,
  `ReadCount` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `TS1` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `BluetoothSensors`
--

CREATE TABLE IF NOT EXISTS `BluetoothSensors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timeadded` datetime NOT NULL,
  `fulladdress` text DEFAULT NULL,
  `pickaddress` text DEFAULT NULL,
  `assignedwirelessid` text DEFAULT NULL,
  `name` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Hydroponics`
--

CREATE TABLE IF NOT EXISTS `Hydroponics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` text NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `Temperature` float NOT NULL,
  `Turbidity` float NOT NULL,
  `RawTurbidity` int(11) NOT NULL,
  `TDS` float NOT NULL,
  `RawTDS` int(11) NOT NULL,
  `Level` float NOT NULL,
  `RawLevel` float NOT NULL,
  `Ph` float NOT NULL,
  `RawPh` float NOT NULL,
  `Temperature24Hour` float NOT NULL,
  `TDS24Hour` float NOT NULL,
  `Turbidity24Hour` float NOT NULL,
  `Ph24Hour` float NOT NULL,
  `Level24Hour` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_hy_ts` (`TimeStamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `InfraredSensorData`
--

CREATE TABLE IF NOT EXISTS `InfraredSensorData` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` text NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `Thermistor` float DEFAULT NULL,
  `PixelData` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `TS1` (`TimeStamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Sensors`
--

CREATE TABLE IF NOT EXISTS `Sensors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` text NOT NULL,
  `SensorNumber` int(11) NOT NULL,
  `SensorValue` float NOT NULL,
  `RawSensorValue` int(11) DEFAULT NULL,
  `SensorType` text NOT NULL,
  `TimeRead` datetime NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `TS1` (`TimeStamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `SkyCamPictures`
--

CREATE TABLE IF NOT EXISTS `SkyCamPictures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `messageID` int(11) NOT NULL DEFAULT -1,
  `cameraID` text NOT NULL,
  `picturename` varchar(100) NOT NULL,
  `picturesize` int(11) NOT NULL,
  `resends` int(11) NOT NULL,
  `resolution` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `TS1` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `SystemLog`
--

CREATE TABLE IF NOT EXISTS `SystemLog` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Level` int(11) NOT NULL,
  `SystemText` text NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  KEY `ID` (`ID`),
  KEY `TS1` (`TimeStamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `ValveChanges`
--

CREATE TABLE IF NOT EXISTS `ValveChanges` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` varchar(10) NOT NULL,
  `ValveNumber` int(11) NOT NULL,
  `State` int(11) NOT NULL,
  `Source` text NOT NULL,
  `ValveType` text NOT NULL,
  `SecondsOn` int(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`ID`),
  KEY `TS1` (`TimeStamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `ValveRecord`
--

CREATE TABLE IF NOT EXISTS `ValveRecord` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` varchar(10) NOT NULL,
  `State` varchar(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`ID`),
  KEY `TS1` (`TimeStamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
