SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE;
SET SQL_MODE = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `ecommerce` DEFAULT CHARACTER SET utf8;
USE `ecommerce`;

CREATE TABLE IF NOT EXISTS `Clientes` (
    `idClientes` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(45) NOT NULL,
    `e-mail` VARCHAR(45) NOT NULL,
    `senha` VARCHAR(128) NOT NULL,
    `telefone` VARCHAR(45) NULL,
    `dataNascimento` DATE NULL,
    PRIMARY KEY (`idClientes`),
    UNIQUE KEY `uk_Clientes_email` (`e-mail`)
 ) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Categoria` (
    `idCategoria` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(45) NOT NULL,
    `descricao` VARCHAR(45) NULL,
    PRIMARY KEY (`idCategoria`)
 ) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Produtos` (
    `idProdutos` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(45) NOT NULL,
    `descricao` VARCHAR(45) NOT NULL,
    `preco` DECIMAL(10,2) NOT NULL,
    `imagem` VARCHAR(45) NULL,
    `peso` DECIMAL(10,2) NULL,
    `estoque` INT NULL,
    `Categoria_idCategoria` INT NOT NULL,
    `ativo` TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (`idProdutos`),
    INDEX `fk_Produtos_Categoria1_idx` (`Categoria_idCategoria` ASC),
    CONSTRAINT `fk_Produtos_Categoria1`
        FOREIGN KEY (`Categoria_idCategoria`)
        REFERENCES `Categoria` (`idCategoria`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
 ) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Pedidos` (
    `idPedidos` INT NOT NULL AUTO_INCREMENT,
    `dataPedido` DATE NULL,
    `status` VARCHAR(45) NULL,
    `total` DECIMAL(10,2) NULL,
    `Clientes_idClientes` INT NOT NULL,
    PRIMARY KEY (`idPedidos`),
    INDEX `fk_Pedidos_Clientes1_idx` (`Clientes_idClientes` ASC),
    CONSTRAINT `fk_Pedidos_Clientes1`
        FOREIGN KEY (`Clientes_idClientes`)
        REFERENCES `Clientes` (`idClientes`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
 ) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `ItemPedido` (
    `idItemPedido` INT NOT NULL AUTO_INCREMENT,
    `quantidade` INT NULL,
    `precoTotal` DECIMAL(10,2) NULL,
    `Pedidos_idPedidos` INT NOT NULL,
    `Produtos_idProdutos` INT NOT NULL,
    PRIMARY KEY (`idItemPedido`),
    INDEX `fk_ItemPedido_Pedidos1_idx` (`Pedidos_idPedidos` ASC),
    INDEX `fk_ItemPedido_Produtos1_idx` (`Produtos_idProdutos` ASC),
    CONSTRAINT `fk_ItemPedido_Pedidos1`
        FOREIGN KEY (`Pedidos_idPedidos`)
        REFERENCES `Pedidos` (`idPedidos`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `fk_ItemPedido_Produtos1`
        FOREIGN KEY (`Produtos_idProdutos`)
        REFERENCES `Produtos` (`idProdutos`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
 ) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Endereco` (
    `idEndereco` INT NOT NULL AUTO_INCREMENT,
    `rua` VARCHAR(45) NULL,
    `numero` INT NULL,
    `bairro` VARCHAR(45) NULL,
    `cidade` VARCHAR(45) NULL,
    `estado` VARCHAR(2) NULL,
    `cep` VARCHAR(9) NULL,
    `Clientes_idClientes` INT NOT NULL,
    PRIMARY KEY (`idEndereco`),
    INDEX `fk_Endereco_Clientes1_idx` (`Clientes_idClientes` ASC),
    CONSTRAINT `fk_Endereco_Clientes1`
        FOREIGN KEY (`Clientes_idClientes`)
        REFERENCES `Clientes` (`idClientes`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
 ) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Pagamento` (
    `idPagamento` INT NOT NULL,
    `tipo` VARCHAR(45) NOT NULL,
    `data` DATE NOT NULL,
    `status` VARCHAR(45) NOT NULL,
    `valor` DECIMAL(10,2) NOT NULL,
    `Pedidos_idPedidos` INT NOT NULL,
    PRIMARY KEY (`idPagamento`),
    INDEX `fk_Pagamento_Pedidos1_idx` (`Pedidos_idPedidos` ASC),
    CONSTRAINT `fk_Pagamento_Pedidos1`
        FOREIGN KEY (`Pedidos_idPedidos`)
        REFERENCES `Pedidos` (`idPedidos`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
 ) ENGINE = InnoDB;

SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;

ALTER TABLE `Clientes` MODIFY COLUMN `senha` VARCHAR(128) NOT NULL;

SET @sql_idx := (
    SELECT IF(
        EXISTS(
            SELECT 1 FROM information_schema.statistics 
            WHERE table_schema = DATABASE() 
                AND table_name = 'Clientes' 
                AND index_name = 'uk_Clientes_email'
        ),
        'SELECT 1',
        'ALTER TABLE `Clientes` ADD UNIQUE KEY `uk_Clientes_email` (`e-mail`)'
    )
);
PREPARE stmt FROM @sql_idx; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql_col := (
    SELECT IF(
        EXISTS(
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = DATABASE()
                AND table_name = 'Produtos'
                AND column_name = 'ativo'
        ),
        'SELECT 1',
        'ALTER TABLE `Produtos` ADD COLUMN `ativo` TINYINT(1) NOT NULL DEFAULT 1'
    )
);
PREPARE stmt2 FROM @sql_col; EXECUTE stmt2; DEALLOCATE PREPARE stmt2;

DELIMITER $$
DROP PROCEDURE IF EXISTS buscar_produto $$
CREATE PROCEDURE buscar_produto(IN p_nome VARCHAR(100))
BEGIN
    SELECT p.idProdutos AS ID,
        p.nome       AS Nome,
        p.preco      AS Preco,
        c.nome       AS Categoria
    FROM Produtos p
    JOIN Categoria c ON c.idCategoria = p.Categoria_idCategoria
    WHERE p.ativo = 1
      AND (p.nome LIKE CONCAT('%', p_nome, '%') OR p_nome IS NULL OR p_nome = '');
END $$
DELIMITER ;
