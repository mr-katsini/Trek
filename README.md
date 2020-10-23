# Trek


## Dependencies

Make sure this is installed if you're using unix

```

# Mac OSX
brew install unixodbc


# Linux
# <WHATEVER PACKAGE MANAGER YOU USE> unixodbc
apt-get install unixodbc


```

These are also needed for the database driver (MACOS)

```
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql mssql-tools
brew install unixodbc
```