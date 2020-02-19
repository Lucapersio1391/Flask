
create table if not exists node_tree
( `idNode` int NOT NULL AUTO_INCREMENT,
`level` int NOT NULL,
`iLeft` int NOT NULL,
`iRight` int NOT NULL,
PRIMARY KEY (idNode)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

create table if not exists node_tree_names
( `idNode` int NOT NULL,
`language` ENUM('english', 'italian') NOT NULL,
`nodeName` varchar(100) NOT NULL,
CONSTRAINT `Nodo_FK` FOREIGN KEY (`idNode`) REFERENCES `node_tree` (`idNode`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=INNODB DEFAULT CHARSET=utf8;
