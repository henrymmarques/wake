-- MySQL Script generated by MySQL Workbench
-- Tue Nov  2 20:38:14 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema wake
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `wake` ;

-- -----------------------------------------------------
-- Schema wake
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `wake` DEFAULT CHARACTER SET utf8 ;
USE `wake` ;

-- -----------------------------------------------------
-- Table `wake`.`Cliente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `wake`.`Cliente` ;

CREATE TABLE IF NOT EXISTS `wake`.`Cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `Email` VARCHAR(45) NOT NULL,
  `Nome` VARCHAR(45) NOT NULL,
  `Password` VARCHAR(200) NOT NULL,
  `Morada` VARCHAR(45) NULL,
  `Morada de Faturação` VARCHAR(45) NULL,
  `Peso` INT NULL,
  `Altura` INT NULL,
  `Genero` VARCHAR(45) NULL,
  UNIQUE INDEX `Email_Cliente_UNIQUE` (`idCliente` ASC) VISIBLE,
  PRIMARY KEY (`idCliente`),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wake`.`Estilo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `wake`.`Estilo` ;

CREATE TABLE IF NOT EXISTS `wake`.`Estilo` (
  `idEstilo` INT NOT NULL,
  `Nome_Estilo` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idEstilo`),
  UNIQUE INDEX `idEstilo_UNIQUE` (`idEstilo` ASC) VISIBLE,
  UNIQUE INDEX `Nome_Estilo_UNIQUE` (`Nome_Estilo` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wake`.`Formulario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `wake`.`Formulario` ;

CREATE TABLE IF NOT EXISTS `wake`.`Formulario` (
  `idFormulario` INT NOT NULL auto_increment,
  `Resposta 1` INT NULL,
   `Resposta 2` INT NULL,
    `Resposta 3` INT NULL,
     `Resposta 4` INT NULL,
     `Resposta 5` INT NULL,
      `Resposta 6` INT NULL,
       `Resposta 7` INT NULL,
        `Resposta 8` INT NULL,
         `Resposta 9` INT NULL,
          `Resposta 10` INT NULL,
            `Resposta 11` INT NULL,
             `Resposta 12` INT NULL,
              `Resposta 13` INT NULL,
               `Resposta 14` INT NULL,
                `Resposta 15` INT NULL,
      
  `Cliente_idCliente` INT NOT NULL,
  `Estilo_idEstilo1` INT NOT NULL,
  PRIMARY KEY (`idFormulario`),
  UNIQUE INDEX `idFormulário_UNIQUE` (`idFormulario` ASC) VISIBLE,
  INDEX `fk_Formulário_Cliente1_idx` (`Cliente_idCliente` ASC) VISIBLE,
  INDEX `fk_Formulario_Estilo1_idx` (`Estilo_idEstilo1` ASC) VISIBLE,
  CONSTRAINT `fk_Formulário_Cliente1`
    FOREIGN KEY (`Cliente_idCliente`)
    REFERENCES `wake`.`Cliente` (`idCliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Formulario_Estilo1`
    FOREIGN KEY (`Estilo_idEstilo1`)
    REFERENCES `wake`.`Estilo` (`idEstilo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wake`.`Roupa`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `wake`.`Roupa` ;

CREATE TABLE IF NOT EXISTS `wake`.`Roupa` (
  `idRoupa` INT NOT NULL AUTO_INCREMENT,
  `URL` varchar(500) NULL,
  `Genero` varchar(25) NULL,
  -- Fazer Insert Roupas
  PRIMARY KEY (`idRoupa`),
  UNIQUE INDEX `idRoupa_UNIQUE` (`idRoupa` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wake`.`Pacote`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `wake`.`Pacote` ;

CREATE TABLE IF NOT EXISTS `wake`.`Pacote` (
  `idPacote` INT NOT NULL,
  `Cliente_idCliente` INT NOT NULL,
  PRIMARY KEY (`idPacote`),
  UNIQUE INDEX `idPacote_UNIQUE` (`idPacote` ASC) VISIBLE,
  INDEX `fk_Pacote_Cliente1_idx` (`Cliente_idCliente` ASC) VISIBLE,
  CONSTRAINT `fk_Pacote_Cliente1`
    FOREIGN KEY (`Cliente_idCliente`)
    REFERENCES `wake`.`Cliente` (`idCliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wake`.`Estilo_Roupa`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `wake`.`Estilo_Roupa` ;

CREATE TABLE IF NOT EXISTS `wake`.`Estilo_Roupa` (
  `Estilo_idEstilo` INT NOT NULL,
  `Roupa_idRoupa` INT NOT NULL,
  PRIMARY KEY (`Estilo_idEstilo`, `Roupa_idRoupa`),
  INDEX `fk_Estilo_has_Roupa_Roupa1_idx` (`Roupa_idRoupa` ASC) VISIBLE,
  INDEX `fk_Estilo_has_Roupa_Estilo1_idx` (`Estilo_idEstilo` ASC) VISIBLE,
  CONSTRAINT `fk_Estilo_has_Roupa_Estilo1`
    FOREIGN KEY (`Estilo_idEstilo`)
    REFERENCES `wake`.`Estilo` (`idEstilo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Estilo_has_Roupa_Roupa1`
    FOREIGN KEY (`Roupa_idRoupa`)
    REFERENCES `wake`.`Roupa` (`idRoupa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wake`.`Conteudo_Pacote`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `wake`.`Conteudo_Pacote` ;

CREATE TABLE IF NOT EXISTS `wake`.`Conteudo_Pacote` (
  `Pacote_idPacote` INT NOT NULL,
  `Estilo_Roupa_Estilo_idEstilo` INT NOT NULL,
  `Estilo_Roupa_Roupa_idRoupa` INT NOT NULL,
  PRIMARY KEY (`Pacote_idPacote`, `Estilo_Roupa_Estilo_idEstilo`, `Estilo_Roupa_Roupa_idRoupa`),
  INDEX `fk_Pacote_has_Estilo_Roupa_Estilo_Roupa1_idx` (`Estilo_Roupa_Estilo_idEstilo` ASC, `Estilo_Roupa_Roupa_idRoupa` ASC) VISIBLE,
  INDEX `fk_Pacote_has_Estilo_Roupa_Pacote1_idx` (`Pacote_idPacote` ASC) VISIBLE,
  CONSTRAINT `fk_Pacote_has_Estilo_Roupa_Pacote1`
    FOREIGN KEY (`Pacote_idPacote`)
    REFERENCES `wake`.`Pacote` (`idPacote`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pacote_has_Estilo_Roupa_Estilo_Roupa1`
    FOREIGN KEY (`Estilo_Roupa_Estilo_idEstilo` , `Estilo_Roupa_Roupa_idRoupa`)
    REFERENCES `wake`.`Estilo_Roupa` (`Estilo_idEstilo` , `Roupa_idRoupa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
