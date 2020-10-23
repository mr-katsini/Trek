CREATE TABLE __Migrations(
    [Name] VARCHAR PRIMARY KEY,
    [Applied] bit,
    [DateApplied] DATETIME DEFAULT(GETDATE())
)
