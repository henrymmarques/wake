-- -----------------------------------------------------
-- Table `wake`.`Conteudo_Pacote`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `wake`.`Conteudo_Pacote` ;
DROP TABLE IF EXISTS `wake`.`Estilo_Roupa` ;
DROP TABLE IF EXISTS `wake`.`Roupa` ;

- -----------------------------------------------------
-- Table `wake`.`Roupa`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wake`.`Roupa` (
  `idRoupa` INT NOT NULL AUTO_INCREMENT,
  `URL` varchar(500) NULL,
  `Genero` varchar(25) NULL,
  -- Fazer Insert Roupas
  PRIMARY KEY (`idRoupa`),
  UNIQUE INDEX `idRoupa_UNIQUE` (`idRoupa` ASC) VISIBLE)
ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `wake`.`Estilo_Roupa`
-- -----------------------------------------------------

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
