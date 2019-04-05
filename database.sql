SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


CREATE TABLE `zhwiki_bulletin_message` (
  `mid` int(11) NOT NULL,
  `html` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `zhwiki_bulletin_record` (
  `mid` int(11) NOT NULL,
  `chat_id` bigint(20) NOT NULL,
  `message_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


ALTER TABLE `zhwiki_bulletin_message`
  ADD PRIMARY KEY (`mid`);

ALTER TABLE `zhwiki_bulletin_record`
  ADD KEY `mid` (`mid`);


ALTER TABLE `zhwiki_bulletin_message`
  MODIFY `mid` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `zhwiki_bulletin_record`
  ADD CONSTRAINT `zhwiki_bulletin_record_ibfk_1` FOREIGN KEY (`mid`) REFERENCES `zhwiki_bulletin_message` (`mid`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
