-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 21, 2022 at 12:58 PM
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

DROP TABLE IF EXISTS `Alarms`;
CREATE TABLE `Alarms` (
  `id` int(11) NOT NULL,
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
  `currenttemperature` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `BluetoothSensorData`
--

DROP TABLE IF EXISTS `BluetoothSensorData`;
CREATE TABLE `BluetoothSensorData` (
  `id` int(11) NOT NULL,
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
  `ReadCount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `BluetoothSensors`
--

DROP TABLE IF EXISTS `BluetoothSensors`;
CREATE TABLE `BluetoothSensors` (
  `id` int(11) NOT NULL,
  `timeadded` datetime NOT NULL,
  `fulladdress` text DEFAULT NULL,
  `pickaddress` text DEFAULT NULL,
  `assignedwirelessid` text DEFAULT NULL,
  `name` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Hydroponics`
--

DROP TABLE IF EXISTS `Hydroponics`;
CREATE TABLE `Hydroponics` (
  `id` int(11) NOT NULL,
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
  `RawPh` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `InfraredSensorData`
--

DROP TABLE IF EXISTS `InfraredSensorData`;
CREATE TABLE `InfraredSensorData` (
  `id` int(11) NOT NULL,
  `DeviceID` text NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `Thermistor` float DEFAULT NULL,
  `PixelData` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Sensors`
--

DROP TABLE IF EXISTS `Sensors`;
CREATE TABLE `Sensors` (
  `id` int(11) NOT NULL,
  `DeviceID` text NOT NULL,
  `SensorNumber` int(11) NOT NULL,
  `SensorValue` float NOT NULL,
  `RawSensorValue` int(11) DEFAULT NULL,
  `SensorType` text NOT NULL,
  `TimeRead` datetime NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `SkyCamPictures`
--

DROP TABLE IF EXISTS `SkyCamPictures`;
CREATE TABLE `SkyCamPictures` (
  `id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `messageID` int(11) NOT NULL DEFAULT -1,
  `cameraID` text NOT NULL,
  `picturename` varchar(100) NOT NULL,
  `picturesize` int(11) NOT NULL,
  `resends` int(11) NOT NULL,
  `resolution` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `SystemLog`
--

DROP TABLE IF EXISTS `SystemLog`;
CREATE TABLE `SystemLog` (
  `ID` int(11) NOT NULL,
  `Level` int(11) NOT NULL,
  `SystemText` text NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `ValveChanges`
--

DROP TABLE IF EXISTS `ValveChanges`;
CREATE TABLE `ValveChanges` (
  `ID` int(11) NOT NULL,
  `DeviceID` varchar(10) NOT NULL,
  `ValveNumber` int(11) NOT NULL,
  `State` int(11) NOT NULL,
  `Source` text NOT NULL,
  `ValveType` text NOT NULL,
  `SecondsOn` int(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `ValveRecord`
--

DROP TABLE IF EXISTS `ValveRecord`;
CREATE TABLE `ValveRecord` (
  `ID` int(11) NOT NULL,
  `DeviceID` varchar(10) NOT NULL,
  `State` varchar(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Alarms`
--
ALTER TABLE `Alarms`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `BluetoothSensorData`
--
ALTER TABLE `BluetoothSensorData`
  ADD PRIMARY KEY (`id`),
  ADD KEY `TS1` (`id`);

--
-- Indexes for table `BluetoothSensors`
--
ALTER TABLE `BluetoothSensors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Hydroponics`
--
ALTER TABLE `Hydroponics`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_hy_ts` (`TimeStamp`);

--
-- Indexes for table `InfraredSensorData`
--
ALTER TABLE `InfraredSensorData`
  ADD PRIMARY KEY (`id`),
  ADD KEY `TS1` (`TimeStamp`);

--
-- Indexes for table `Sensors`
--
ALTER TABLE `Sensors`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `TS1` (`TimeStamp`);

--
-- Indexes for table `SkyCamPictures`
--
ALTER TABLE `SkyCamPictures`
  ADD PRIMARY KEY (`id`),
  ADD KEY `TS1` (`timestamp`);

--
-- Indexes for table `SystemLog`
--
ALTER TABLE `SystemLog`
  ADD KEY `ID` (`ID`),
  ADD KEY `TS1` (`TimeStamp`);

--
-- Indexes for table `ValveChanges`
--
ALTER TABLE `ValveChanges`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `TS1` (`TimeStamp`);

--
-- Indexes for table `ValveRecord`
--
ALTER TABLE `ValveRecord`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `TS1` (`TimeStamp`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Alarms`
--
ALTER TABLE `Alarms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `BluetoothSensorData`
--
ALTER TABLE `BluetoothSensorData`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `BluetoothSensors`
--
ALTER TABLE `BluetoothSensors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Hydroponics`
--
ALTER TABLE `Hydroponics`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `InfraredSensorData`
--
ALTER TABLE `InfraredSensorData`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Sensors`
--
ALTER TABLE `Sensors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `SkyCamPictures`
--
ALTER TABLE `SkyCamPictures`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `SystemLog`
--
ALTER TABLE `SystemLog`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ValveChanges`
--
ALTER TABLE `ValveChanges`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ValveRecord`
--
ALTER TABLE `ValveRecord`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
