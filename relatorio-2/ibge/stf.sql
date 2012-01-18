SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `STF` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;
USE `STF` ;

-- -----------------------------------------------------
-- Table `STF`.`t_uf`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_uf` (
  `id` VARCHAR(4) NOT NULL ,
  `nome` VARCHAR(19) NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STF`.`t_oab`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_oab` (
  `id_uf` VARCHAR(20) NOT NULL ,
  `qtd_Advogados` FLOAT NULL ,
  `t_uf_id` VARCHAR(4) NOT NULL ,
  INDEX `fk_t_oab_t_uf1` (`t_uf_id` ASC) ,
  CONSTRAINT `fk_t_oab_t_uf1`
    FOREIGN KEY (`t_uf_id` )
    REFERENCES `STF`.`t_uf` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STF`.`t_regiao`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_regiao` (
  `id` VARCHAR(9) NOT NULL ,
  `nome_regiao` VARCHAR(9) NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STF`.`t_pea`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_pea` (
  `sexo` VARCHAR(11) NULL ,
  `numeros_relativos` DECIMAL(10,0)  NULL ,
  `faixa_salarial` VARCHAR(25) NULL ,
  `qtd_por_salario` DECIMAL(10,0)  NULL ,
  `regiao` VARCHAR(11) NULL ,
  `qtd_por_regiao` DECIMAL(10,0)  NULL ,
  `t_regiao_id` VARCHAR(9) NOT NULL ,
  CONSTRAINT `fk_t_pea_t_regiao1`
    FOREIGN KEY (`t_regiao_id` )
    REFERENCES `STF`.`t_regiao` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STF`.`t_area_domicilio`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_area_domicilio` (
  `id` VARCHAR(9) NOT NULL ,
  `nome` VARCHAR(9) NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STF`.`t_educacao`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_educacao` (
  `escolaridade` VARCHAR(26) NULL ,
  `total_escolaridade` DECIMAL(10,0)  NULL ,
  `id_sexo` VARCHAR(11) NULL ,
  `qtd_por_sexo` DECIMAL(10,0)  NULL ,
  `id_area` VARCHAR(11) NULL ,
  `qtd_por_area` DECIMAL(10,0)  NULL ,
  `t_area_domicilio_id` VARCHAR(9) NOT NULL ,
  INDEX `fk_t_educacao_t_area_domicilio1` (`t_area_domicilio_id` ASC) ,
  CONSTRAINT `fk_t_educacao_t_area_domicilio1`
    FOREIGN KEY (`t_area_domicilio_id` )
    REFERENCES `STF`.`t_area_domicilio` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STF`.`t_func_publicos`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_func_publicos` (
  `id_regiao` VARCHAR(19) NOT NULL ,
  `id_uf` VARCHAR(19) NOT NULL ,
  `total_por_uf` FLOAT NULL ,
  `esfera_federal` FLOAT NULL ,
  `esfera_estadual` FLOAT NULL ,
  `esfera_municipal` FLOAT NULL ,
  `t_regiao_id` VARCHAR(9) NOT NULL ,
  `t_uf_id` VARCHAR(4) NOT NULL ,
  INDEX `fk_t_func_publicos_t_regiao1` (`t_regiao_id` ASC) ,
  INDEX `fk_t_func_publicos_t_uf1` (`t_uf_id` ASC) ,
  CONSTRAINT `fk_t_func_publicos_t_regiao1`
    FOREIGN KEY (`t_regiao_id` )
    REFERENCES `STF`.`t_regiao` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_func_publicos_t_uf1`
    FOREIGN KEY (`t_uf_id` )
    REFERENCES `STF`.`t_uf` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STF`.`t_idades`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_idades` (
  `id` VARCHAR(11) NOT NULL ,
  `faixa` VARCHAR(11) NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STF`.`t_populacao`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_populacao` (
  `id_sexo` VARCHAR(11) NOT NULL ,
  `qtd_por_sexo` FLOAT NULL ,
  `id_area` VARCHAR(11) NOT NULL ,
  `qtd_por_area` FLOAT NULL ,
  `sexo_por_zona` VARCHAR(45) NULL ,
  `qtd_sexo_por_zona` FLOAT NULL ,
  `id_idade` VARCHAR(11) NOT NULL ,
  `qtd_idade` DECIMAL(10,0)  NULL ,
  `t_area_domicilio_id` VARCHAR(9) NOT NULL ,
  `t_idades_id` VARCHAR(11) NOT NULL ,
  INDEX `fk_t_populacao_t_area_domicilio1` (`t_area_domicilio_id` ASC) ,
  INDEX `fk_t_populacao_t_idades1` (`t_idades_id` ASC) ,
  CONSTRAINT `fk_t_populacao_t_area_domicilio1`
    FOREIGN KEY (`t_area_domicilio_id` )
    REFERENCES `STF`.`t_area_domicilio` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_populacao_t_idades1`
    FOREIGN KEY (`t_idades_id` )
    REFERENCES `STF`.`t_idades` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STF`.`t_alfabetizados`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_alfabetizados` (
  `id_idade` VARCHAR(11) NOT NULL ,
  `taxa_nacional` FLOAT NULL ,
  `id_regiao` VARCHAR(13) NOT NULL ,
  `taxa_por_regiao` FLOAT NULL ,
  `id_sexo` VARCHAR(10) NOT NULL ,
  `taxa_por_sexo` FLOAT NULL ,
  `ano_pesquisado` YEAR NULL ,
  `t_idades_id` VARCHAR(11) NOT NULL ,
  `t_regiao_id` VARCHAR(9) NOT NULL ,
  INDEX `fk_t_alfabetizados_t_idades1` (`t_idades_id` ASC) ,
  INDEX `fk_t_alfabetizados_t_regiao1` (`t_regiao_id` ASC) ,
  CONSTRAINT `fk_t_alfabetizados_t_idades1`
    FOREIGN KEY (`t_idades_id` )
    REFERENCES `STF`.`t_idades` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_alfabetizados_t_regiao1`
    FOREIGN KEY (`t_regiao_id` )
    REFERENCES `STF`.`t_regiao` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STF`.`t_nao_alfabetizados`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STF`.`t_nao_alfabetizados` (
  `id_idade` VARCHAR(9) NOT NULL ,
  `taxa_nacional` FLOAT NULL ,
  `id_regiao` VARCHAR(9) NOT NULL ,
  `taxa_por_regiao` FLOAT NULL ,
  `id_sexo` VARCHAR(9) NOT NULL ,
  `taxa_por_sexo` FLOAT NULL ,
  `ano_pesquisado` YEAR NULL ,
  `t_idades_id` VARCHAR(11) NOT NULL ,
  `t_regiao_id` VARCHAR(9) NOT NULL ,
  INDEX `fk_t_nao_alfabetizados_t_idades` (`t_idades_id` ASC) ,
  INDEX `fk_t_nao_alfabetizados_t_regiao1` (`t_regiao_id` ASC) ,
  CONSTRAINT `fk_t_nao_alfabetizados_t_idades`
    FOREIGN KEY (`t_idades_id` )
    REFERENCES `STF`.`t_idades` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_nao_alfabetizados_t_regiao1`
    FOREIGN KEY (`t_regiao_id` )
    REFERENCES `STF`.`t_regiao` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `STF`.`t_uf`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;
USE `STF`;
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('AC', 'Acre');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('AM', 'Amazonas');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('AP', 'Amapa');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('RR', 'Roraima');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('PA', 'Para');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('TO', 'Tocantins');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('MA', 'Maranhao');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('PI', 'Piaui');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('CE', 'Ceara');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('PB', 'Paraiba');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('PE', 'Pernambuco');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('RN', 'Rio Grande do Norte');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('AL', 'Alagoas');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('SE', 'Sergipe');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('BA', 'Bahia');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('ES', 'Espirito Santo');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('RJ', 'Rio de Janeiro');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('MG', 'Minas Gerais');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('SP', 'Sao Paulo');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('PR', 'Parana');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('SC', 'Santa Catarina');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('RS', 'Rio Grande do Sul');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('RO', 'Rondonia');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('MT', 'Mato Grosso');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('MS', 'Mato Grosso do Sul');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('GO', 'Goias');
INSERT INTO `STF`.`t_uf` (`id`, `nome`) VALUES ('DF', 'Brasilia');

COMMIT;

-- -----------------------------------------------------
-- Data for table `STF`.`t_oab`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;
USE `STF`;
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Acre', 2.104, 'AC');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Alagoas', 5.28, 'AL');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Amazonas', 4.275, 'AM');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Amapa', 1.127, 'AP');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Bahia', 23.421, 'BA');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Ceara', 11.463, 'CE');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Distrito Federal', 19.536, 'DF');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Espirito Santo', 9.851, 'ES');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Goias', 18.831, 'GO');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Maranhao', 5.675, 'MA');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Minas Gerais', 69.017, 'MG');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Mato Grosso do Sul', 7.56, 'MS');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Mato Grosso', 7.474, 'MT');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Para', 9.822, 'PA');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Paraiba', 6.148, 'PB');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Pernambuco', 16.379, 'PE');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Piaui', 4.987, 'PI');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Parana', 39.184, 'PR');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Rio de Janeiro', 116.225, 'RJ');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Rio Grande do Norte', 5.163, 'RN');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Rondonia', 3.303, 'RO');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Roraima', 591, 'RR');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Rio Grande do Sul', 45.609, 'RS');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Santa Catarina', 19.278, 'SC');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Sergipe', 3.388, 'SE');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Sao Paulo', 228.931, 'SP');
INSERT INTO `STF`.`t_oab` (`id_uf`, `qtd_Advogados`, `t_uf_id`) VALUES ('Tocatins', 2.396, 'TO');

COMMIT;

-- -----------------------------------------------------
-- Data for table `STF`.`t_regiao`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;
USE `STF`;
INSERT INTO `STF`.`t_regiao` (`id`, `nome_regiao`) VALUES ('norte', 'norte');
INSERT INTO `STF`.`t_regiao` (`id`, `nome_regiao`) VALUES ('nordeste', 'nordeste');
INSERT INTO `STF`.`t_regiao` (`id`, `nome_regiao`) VALUES ('sul', 'sul');
INSERT INTO `STF`.`t_regiao` (`id`, `nome_regiao`) VALUES ('sudeste', 'sudeste');
INSERT INTO `STF`.`t_regiao` (`id`, `nome_regiao`) VALUES ('centro_oeste', 'centro_oeste');

COMMIT;

-- -----------------------------------------------------
-- Data for table `STF`.`t_pea`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;
USE `STF`;
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'ate 1 salario', 21.2, 'Norte', 25.4, 'norte');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'ate 1 salario', 21.2, 'Nordeste', 37.0, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'ate 1 salario', 21.2, 'Sudeste', 13.6, 'sudeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'ate 1 salario', 21.2, 'Sul', 13.5, 'sul');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'ate 1 salario', 21.2, 'Centro_Oeste', 17.3, 'centro_oeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'ate 1 salario', 28.9, 'Norte', 32.7, 'norte');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'ate 1 salario', 28.9, 'Nordeste', 42.2, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'ate 1 salario', 28.9, 'Sudeste', 22.3, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'ate 1 salario', 28.9, 'Sul', 22.3, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'ate 1 salario', 28.9, 'Centro_Oeste', 27.3, 'centro_oeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 1 a 2 salarios', 10.1, 'Norte', 7.7, 'norte');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 1 a 2 salarios', 10.1, 'Nordeste', 4.8, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 1 a 2 salarios', 10.1, 'Sudeste', 12.6, 'sudeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 1 a 2 salarios', 10.1, 'Sul', 13.7, 'sul');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 1 a 2 salarios', 10.1, 'Centro_Oeste', 11.2, 'centro_oeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 1 a 2 salarios', 19.3, 'Norte', 14.6, 'norte');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 1 a 2 salarios', 19.3, 'Nordeste', 13.1, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 1 a 2 salarios', 19.3, 'Sudeste', 22.4, 'sudeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 1 a 2 salarios', 19.3, 'Sul', 24.3, 'sul');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 1 a 2 salarios', 19.3, 'Centro_Oeste', 19.4, 'centro_oeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 3 a 5 salarios', 8.9, 'Norte', 6.2, 'norte');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 3 a 5 salarios', 8.9, 'Nordeste', 4.1, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 3 a 5 salarios', 8.9, 'Sudeste', 11.3, 'sudeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 3 a 5 salarios', 8.9, 'Sul', 12.4, 'sul');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 3 a 5 salarios', 8.9, 'Centro_Oeste', 8.8, 'centro_oeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 3 a 5 salarios', 4.6, 'Norte', 3.2, 'norte');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 3 a 5 salarios', 4.6, 'Nordeste', 2.3, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 3 a 5 salarios', 4.6, 'Sudeste', 5.8, 'sudeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 3 a 5 salarios', 4.6, 'Sul', 6.2, 'sul');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 3 a 5 salarios ', 4.6, 'Centro_Oeste', 4.6, 'centro_oeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 5 a 10 salarios', 5.2, 'Norte', 3.4, 'norte');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 5 a 10 salarios', 5.2, 'Nordeste', 2.5, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 5 a 10 salarios', 5.2, 'Sudeste', 6.5, 'sudeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 5 a 10 salarios', 5.2, 'Sul', 7.3, 'sul');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 5 a 10 salarios', 5.2, 'Centro_Oeste', 5.7, 'centro_oeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 5 a 10 salarios', 2.7, 'Norte', 1.8, 'norte');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 5 a 10 salarios', 2.7, 'Nordeste', 1.4, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 5 a 10 salarios', 2.7, 'Sudeste', 3.4, 'sudeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 5 a 10 salarios', 2.7, 'Sul', 3.6, 'sul');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 5 a 10 salarios', 2.7, 'Centro_Oeste', 3.5, 'centro_oeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 10 a 20 salarios', 2.2, 'Norte', 1.2, 'norte');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 10 a 20 salarios', 2.2, 'Nordeste', 1.1, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 10 a 20 salarios', 2.2, 'Sudeste', 2.6, 'sudeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 10 a 20 salarios', 2.2, 'Sul', 2.8, 'sul');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Homens', 100, 'mais de 10 a 20 salarios', 2.2, 'Centro_Oeste', 3.0, 'centro_oeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 10 a 20 salarios', 0.9, 'Norte', 0.4, 'norte');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 10 a 20 salarios', 0.9, 'Nordeste', 0.6, 'nordeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 10 a 20 salarios', 0.9, 'Sudeste', 1.1, 'sudeste');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 10 a 20 salarios', 0.9, 'Sul', 1.0, 'sul');
INSERT INTO `STF`.`t_pea` (`sexo`, `numeros_relativos`, `faixa_salarial`, `qtd_por_salario`, `regiao`, `qtd_por_regiao`, `t_regiao_id`) VALUES ('Mulheres', 100, 'mais de 10 a 20 salarios', 0.9, 'Centro_Oeste', 1.5, 'centro_oeste');

COMMIT;

-- -----------------------------------------------------
-- Data for table `STF`.`t_area_domicilio`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;
USE `STF`;
INSERT INTO `STF`.`t_area_domicilio` (`id`, `nome`) VALUES ('urbana', 'zona urbana');
INSERT INTO `STF`.`t_area_domicilio` (`id`, `nome`) VALUES ('rural', 'zona rural');

COMMIT;

-- -----------------------------------------------------
-- Data for table `STF`.`t_educacao`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;
USE `STF`;
INSERT INTO `STF`.`t_educacao` (`escolaridade`, `total_escolaridade`, `id_sexo`, `qtd_por_sexo`, `id_area`, `qtd_por_area`, `t_area_domicilio_id`) VALUES ('alfabetizadas', 147.380581, 'homens', 71.361117, 'Urbana', 61.365353, 'urbana');
INSERT INTO `STF`.`t_educacao` (`escolaridade`, `total_escolaridade`, `id_sexo`, `qtd_por_sexo`, `id_area`, `qtd_por_area`, `t_area_domicilio_id`) VALUES ('alfabetizadas', 147.380581, 'mulheres', 76.024464, 'Urbana', 66.725805, 'urbana');
INSERT INTO `STF`.`t_educacao` (`escolaridade`, `total_escolaridade`, `id_sexo`, `qtd_por_sexo`, `id_area`, `qtd_por_area`, `t_area_domicilio_id`) VALUES ('alfabetizadas', 147.385581, 'homens', 71.361117, 'Rural', 9.995764, 'rural');
INSERT INTO `STF`.`t_educacao` (`escolaridade`, `total_escolaridade`, `id_sexo`, `qtd_por_sexo`, `id_area`, `qtd_por_area`, `t_area_domicilio_id`) VALUES ('alfabetizadas', 147.385581, 'mulheres', 76.024464, 'Rural', 9.298659, 'rural');
INSERT INTO `STF`.`t_educacao` (`escolaridade`, `total_escolaridade`, `id_sexo`, `qtd_por_sexo`, `id_area`, `qtd_por_area`, `t_area_domicilio_id`) VALUES ('nao_alfabetizadas', 14.604155, 'homens', 7.404481, 'Urbana', 4.429995, 'urbana');
INSERT INTO `STF`.`t_educacao` (`escolaridade`, `total_escolaridade`, `id_sexo`, `qtd_por_sexo`, `id_area`, `qtd_por_area`, `t_area_domicilio_id`) VALUES ('nao_alfabetizadas', 14.604155, 'mulheres', 7.199674, 'Urbana', 4.967838, 'urbana');
INSERT INTO `STF`.`t_educacao` (`escolaridade`, `total_escolaridade`, `id_sexo`, `qtd_por_sexo`, `id_area`, `qtd_por_area`, `t_area_domicilio_id`) VALUES ('nao_alfabetizadas', 14.604155, 'homens', 7.404481, 'Rural', 2.974486, 'rural');
INSERT INTO `STF`.`t_educacao` (`escolaridade`, `total_escolaridade`, `id_sexo`, `qtd_por_sexo`, `id_area`, `qtd_por_area`, `t_area_domicilio_id`) VALUES ('nao_alfabetizadas', 14.604155, 'mulheres', 7.199674, 'Rural', 2.231836, 'rural');

COMMIT;

-- -----------------------------------------------------
-- Data for table `STF`.`t_func_publicos`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;
USE `STF`;
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Norte', 'Rondonia', 100.459, 10.642, 45.877, 43.897, 'norte', 'RO');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Norte', 'Acre', 44.139, 2.239, 34.665, 7.15, 'norte', 'AC');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Norte', 'Amazonas', 160.261, 12.767, 69.434, 77.906, 'norte', 'AM');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Norte', 'Roraima', 18.698, 3.696, 8.628, 6.178, 'norte', 'RR');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Norte', 'Para', 303.096, 19.965, 101.291, 181.263, 'norte', 'PA');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Norte', 'Amapa', 41.211, 10.315, 17.745, 12.855, 'norte', 'AP');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Norte', 'Tocatins', 112.632, 3.641, 56.465, 52.526, 'norte', 'TO');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Nordeste', 'Maranhao', 194.705, 8.455, 63.741, 122.499, 'nordeste', 'MA');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Nordeste', 'Piaui', 126.043, 7.445, 62.509, 55.382, 'nordeste', 'PI');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Nordeste', 'Ceara', 297.738, 18.543, 60.547, 216.962, 'nordeste', 'CE');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Nordeste', 'Rio Grande do Norte', 184.362, 11.699, 70.492, 99.925, 'nordeste', 'RN');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Nordeste', 'Paraiba', 217.279, 15.776, 81.203, 120.063, 'nordeste', 'PB');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Nordeste', 'Pernambuco', 373.849, 24.502, 119.136, 228.661, 'nordeste', 'PE');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Nordeste', 'Alagoas', 134.193, 6.725, 43.136, 84.782, 'nordeste', 'AL');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Nordeste', 'Sergipe', 116.904, 6.108, 48.57, 61.693, 'nordeste', 'SE');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Nordeste', 'Bahia', 582.17, 29.07, 192.399, 360.028, 'nordeste', 'BA');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Sul', 'Parana', 426.258, 21.422, 151.425, 253.367, 'sul', 'PR');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Sul', 'Santa Catarina', 273.512, 16.666, 95.612, 161.183, 'sul', 'SC');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Sul', 'Rio Grande do Sul', 444.025, 34.692, 164.841, 244.025, 'sul', 'RS');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Sudeste', 'Minas Gerais', 992.809, 51.593, 370.507, 570.635, 'sudeste', 'MG');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Sudeste', 'Epirito Santo', 219.123, 9.793, 79.656, 129.104, 'sudeste', 'ES');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Sudeste', 'Rio de Janeiro', 734.047, 150.199, 265.213, 317.207, 'sudeste', 'RJ');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Sudeste', 'Sao Paulo', 1.460947, 57.04, 729.566, 629.486, 'sudeste', 'SP');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Centro_Oeste', 'Mato Grosso do Sul', 162.007, 9.471, 70.729, 81.778, 'centro_oeste', 'MS');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Centro_Oeste', 'Mato Grosso', 157.053, 7.815, 66.959, 82.212, 'centro_oeste', 'MT');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Centro_Oeste', 'Goias', 302.59, 13.362, 108.36, 173.853, 'centro_oeste', 'GO');
INSERT INTO `STF`.`t_func_publicos` (`id_regiao`, `id_uf`, `total_por_uf`, `esfera_federal`, `esfera_estadual`, `esfera_municipal`, `t_regiao_id`, `t_uf_id`) VALUES ('Centro_Oeste', 'Distrito Federal', 426.059, 293.791, 131.676, 0, 'centro_oeste', 'DF');

COMMIT;

-- -----------------------------------------------------
-- Data for table `STF`.`t_idades`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;
USE `STF`;
INSERT INTO `STF`.`t_idades` (`id`, `faixa`) VALUES ('18 a 24', 'de 18 a 24 anos');
INSERT INTO `STF`.`t_idades` (`id`, `faixa`) VALUES ('25 ou mais', 'de 25 anos ou mais');

COMMIT;

-- -----------------------------------------------------
-- Data for table `STF`.`t_alfabetizados`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;
USE `STF`;
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 30.3, 'norte', 33.9, 'homens', 32.3, 2009, '18 a 24', 'norte');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 30.3, 'norte', 33.9, 'mulheres', 35.4, 2009, '18 a 24', 'norte');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 30.3, 'nordeste', 30.6, 'homens', 29.4, 2009, '18 a 24', 'nordeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 30.3, 'nordeste', 30.6, 'mulheres', 31.8, 2009, '18 a 24', 'nordeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 30.3, 'sudeste', 29.1, 'homens', 27.5, 2009, '18 a 24', 'sudeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 30.3, 'sudeste', 29.1, 'mulheres', 30.8, 2009, '18 a 24', 'sudeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 30.3, 'sul', 30.2, 'homens', 26.9, 2009, '18 a 24', 'sul');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 30.3, 'sul', 30.2, 'mulheres', 33.6, 2009, '18 a 24', 'sul');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 30.3, 'centro_oeste', 31.8, 'homens', 28.8, 2009, '18 a 24', 'centro_oeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 30.3, 'centro_oeste', 31.8, 'mulheres', 34.7, 2009, '18 a 24', 'centro_oeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 5.1, 'norte', 7.2, 'homens', 5.3, 2009, '25 ou mais', 'norte');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 5.1, 'norte', 7.2, 'mulheres', 9.0, 2009, '25 ou mais', 'norte');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 5.1, 'nordeste', 5.9, 'homens', 4.7, 2009, '25 ou mais', 'nordeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 5.1, 'nordeste', 5.9, 'mulheres', 6.9, 2009, '25 ou mais', 'nordeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 5.1, 'sudeste', 4.4, 'homens', 4.1, 2009, '25 ou mais', 'sudeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 5.1, 'sudeste', 4.4, 'mulheres', 4.7, 2009, '25 ou mais', 'sudeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 5.1, 'sul', 4.4, 'homens', 3.9, 2009, '25 ou mais', 'sul');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 5.1, 'sul', 4.4, 'mulheres', 4.8, 2009, '25 ou mais', 'sul');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 5.1, 'centro_oeste', 5.4, 'homens', 4.3, 2009, '25 ou mais', 'centro_oeste');
INSERT INTO `STF`.`t_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 5.1, 'centro_oeste', 5.4, 'mulheres', 6.5, 2009, '25 ou mais', 'centro_oeste');

COMMIT;

-- -----------------------------------------------------
-- Data for table `STF`.`t_nao_alfabetizados`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;
USE `STF`;
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 10.3, 'norte', 11.4, 'homens', 12.3, 2009, '18 a 24', 'norte');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 10.3, 'norte', 11.4, 'mulheres', 10.5, 2009, '18 a 24', 'norte');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 10.3, 'nordeste', 20.1, 'homens', 22.0, 2009, '18 a 24', 'nordeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 10.3, 'nordeste', 20.1, 'mulheres', 18.5, 2009, '18 a 24', 'nordeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 10.3, 'sudeste', 6.0, 'homens', 5.2, 2009, '18 a 24', 'sudeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 10.3, 'sudeste', 6.0, 'mulheres', 6.7, 2009, '18 a 24', 'sudeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 10.3, 'sul', 5.8, 'homens', 5.3, 2009, '18 a 24', 'sul');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 10.3, 'sul', 5.8, 'mulheres', 6.3, 2009, '18 a 24', 'sul');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 10.3, 'centro_oeste', 8.6, 'homens', 8.2, 2009, '18 a 24', 'centro_oeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('18 a 24', 10.3, 'centro_oeste', 8.6, 'mulheres', 8.9, 2009, '18 a 24', 'centro_oeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 12.0, 'norte', 13.8, 'homens', 14.7, 2009, '25 ou mais', 'norte');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 12.0, 'norte', 13.8, 'mulheres', 12.9, 2009, '25 ou mais', 'norte');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 12.0, 'nordeste', 23.8, 'homens', 25.9, 2009, '25 ou mais', 'nordeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 12.0, 'nordeste', 23.8, 'mulheres', 22.0, 2009, '25 ou mais', 'nordeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 12.0, 'sudeste', 6.9, 'homens', 6.1, 2009, '25 ou mais', 'sudeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 12.0, 'sudeste', 6.9, 'mulheres', 7.7, 2009, '25 ou mais', 'sudeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 12.0, 'sul', 6.7, 'homens', 6.1, 2009, '25 ou mais', 'sul');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 12.0, 'sul', 6.7, 'mulheres', 7.2, 2009, '25 ou mais', 'sul');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 12.0, 'centro_oeste', 10.2, 'homens', 9.8, 2009, '25 ou mais', 'centro_oeste');
INSERT INTO `STF`.`t_nao_alfabetizados` (`id_idade`, `taxa_nacional`, `id_regiao`, `taxa_por_regiao`, `id_sexo`, `taxa_por_sexo`, `ano_pesquisado`, `t_idades_id`, `t_regiao_id`) VALUES ('25 ou mais', 12.0, 'centro_oeste', 10.2, 'mulheres', 10.6, 2009, '25 ou mais', 'centro_oeste');

COMMIT;
