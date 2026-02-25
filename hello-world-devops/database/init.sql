-- Criar database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'TestDB')
BEGIN
    CREATE DATABASE TestDB;
END
GO

USE TestDB;
GO

-- Criar tabela de teste
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'test_table')
BEGIN
    CREATE TABLE test_table (
        id INT PRIMARY KEY IDENTITY(1,1),
        message NVARCHAR(200),
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO

-- Inserir dados de teste
IF NOT EXISTS (SELECT * FROM test_table WHERE message = 'Hello from SQL Server!')
BEGIN
    INSERT INTO test_table (message) VALUES ('Hello from SQL Server!');
    INSERT INTO test_table (message) VALUES ('Multi-tier application working!');
    INSERT INTO test_table (message) VALUES ('DevOps pipeline deployed successfully!');
END
GO

-- Verificar dados
SELECT * FROM test_table;
GO
