SELECT * FROM mantenimiento.usuarios
DELIMITER $$
CREATE TRIGGER after_user_insert
AFTER INSERT ON usuarios
FOR EACH ROW
BEGIN
    IF NEW.rol = 'tecnico' THEN
        INSERT INTO tecnico (id_usuario) VALUES (NEW.id);
    END IF;
END$$
DELIMITER ;usuarios