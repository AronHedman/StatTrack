-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: Apr 09, 2026 at 09:29 PM
-- Server version: 12.0.2-MariaDB-ubu2404
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `statTrack`
--

-- --------------------------------------------------------

--
-- Table structure for table `artists`
--

CREATE TABLE `artists` (
  `artist_id` int(11) NOT NULL,
  `artist_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `play_history`
--

CREATE TABLE `play_history` (
  `history_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL,
  `played_at_datetime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `songs`
--

CREATE TABLE `songs` (
  `song_id` int(11) NOT NULL,
  `artist_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `extralarge` varchar(255) DEFAULT NULL,
  `large` varchar(255) DEFAULT NULL,
  `medium` varchar(255) DEFAULT NULL,
  `small` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `last_synced_datetime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_artist_stats`
--

CREATE TABLE `user_artist_stats` (
  `user_id` int(11) NOT NULL,
  `artist_id` int(11) NOT NULL,
  `stream_count` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_song_stats`
--

CREATE TABLE `user_song_stats` (
  `user_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL,
  `stream_count` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `artists`
--
ALTER TABLE `artists`
  ADD PRIMARY KEY (`artist_id`),
  ADD UNIQUE KEY `artist_name` (`artist_name`);

--
-- Indexes for table `play_history`
--
ALTER TABLE `play_history`
  ADD PRIMARY KEY (`history_id`),
  ADD UNIQUE KEY `unique_user_stream` (`user_id`,`song_id`,`played_at_datetime`),
  ADD UNIQUE KEY `unique_user_song_time` (`user_id`,`song_id`,`played_at_datetime`),
  ADD KEY `song_id` (`song_id`);

--
-- Indexes for table `songs`
--
ALTER TABLE `songs`
  ADD PRIMARY KEY (`song_id`),
  ADD UNIQUE KEY `unique_song_entry` (`artist_id`,`title`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `user_artist_stats`
--
ALTER TABLE `user_artist_stats`
  ADD PRIMARY KEY (`user_id`,`artist_id`),
  ADD UNIQUE KEY `unique_user_artist` (`user_id`,`artist_id`),
  ADD KEY `artist_id` (`artist_id`);

--
-- Indexes for table `user_song_stats`
--
ALTER TABLE `user_song_stats`
  ADD PRIMARY KEY (`user_id`,`song_id`),
  ADD UNIQUE KEY `unique_user_song` (`user_id`,`song_id`),
  ADD KEY `song_id` (`song_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `artists`
--
ALTER TABLE `artists`
  MODIFY `artist_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `play_history`
--
ALTER TABLE `play_history`
  MODIFY `history_id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `songs`
--
ALTER TABLE `songs`
  MODIFY `song_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `play_history`
--
ALTER TABLE `play_history`
  ADD CONSTRAINT `play_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `play_history_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`);

--
-- Constraints for table `songs`
--
ALTER TABLE `songs`
  ADD CONSTRAINT `songs_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`);

--
-- Constraints for table `user_artist_stats`
--
ALTER TABLE `user_artist_stats`
  ADD CONSTRAINT `fk_user_artist_stats_artist` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_song_stats`
--
ALTER TABLE `user_song_stats`
  ADD CONSTRAINT `user_song_stats_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `user_song_stats_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
