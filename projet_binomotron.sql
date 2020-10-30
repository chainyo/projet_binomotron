-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8081
-- Generation Time: Oct 30, 2020 at 01:17 PM
-- Server version: 5.7.24
-- PHP Version: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `projet_binomotron`
--

-- --------------------------------------------------------

--
-- Table structure for table `grp`
--

CREATE TABLE `grp` (
  `id_grp` int(11) NOT NULL,
  `label` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `grp`
--

INSERT INTO `grp` (`id_grp`, `label`) VALUES
(1, 'Groupe 1'),
(2, 'Groupe 2'),
(3, 'Groupe 3'),
(4, 'Groupe 4'),
(5, 'Groupe 5'),
(6, 'Groupe 6'),
(7, 'Groupe 7'),
(8, 'Groupe 8'),
(9, 'Groupe 9'),
(10, 'Groupe 10');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `id_project` int(11) NOT NULL,
  `label` varchar(30) NOT NULL,
  `date` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id_student` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `forename` varchar(20) NOT NULL,
  `photo` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id_student`, `name`, `forename`, `photo`) VALUES
(1, 'Bokalli', 'Luigi', ''),
(2, 'Bertho', 'Amaury', ''),
(3, 'Chaigneau', 'Thomas', ''),
(4, 'Cloatre', 'Erwan', ''),
(5, 'Guillen', 'Céline', ''),
(6, 'Hergoualc-h', 'Pereg', ''),
(7, 'Ibanni', 'Jamal', ''),
(8, 'Le Joncour', 'Jérémy', ''),
(9, 'Le Goff', 'Baptiste', ''),
(10, 'Le Berre', 'Baptiste', ''),
(11, 'Le Moal', 'Patricia', ''),
(12, 'Maintier', 'Ludivine', ''),
(13, 'Mbarga Mvogo', 'Christian', ''),
(14, 'Moulard', 'Eva', ''),
(15, 'Pertron', 'Aude', ''),
(16, 'Rioual', 'Ronan', ''),
(17, 'Sabia', 'Paul', ''),
(18, 'Verpoest', 'Guillaume', ''),
(19, 'Furiga', 'Julien', ''),
(20, 'Karfaoui', 'Christelle', '');

-- --------------------------------------------------------

--
-- Table structure for table `students_grp`
--

CREATE TABLE `students_grp` (
  `id_student` int(11) NOT NULL,
  `id_grp` int(11) NOT NULL,
  `id_project` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `grp`
--
ALTER TABLE `grp`
  ADD PRIMARY KEY (`id_grp`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id_project`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id_student`);

--
-- Indexes for table `students_grp`
--
ALTER TABLE `students_grp`
  ADD KEY `id_student` (`id_student`),
  ADD KEY `id_grp` (`id_grp`),
  ADD KEY `id_project` (`id_project`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `grp`
--
ALTER TABLE `grp`
  MODIFY `id_grp` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `id_project` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id_student` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `students_grp`
--
ALTER TABLE `students_grp`
  ADD CONSTRAINT `students_grp_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `students` (`id_student`),
  ADD CONSTRAINT `students_grp_ibfk_2` FOREIGN KEY (`id_grp`) REFERENCES `grp` (`id_grp`),
  ADD CONSTRAINT `students_grp_ibfk_3` FOREIGN KEY (`id_project`) REFERENCES `projects` (`id_project`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
