package repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {
    private static final String URL = "jdbc:mysql://localhost:3306/tasks_db";
    private static final String USER = "root";
    private static final String PASSWORD = "your_password";

    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            System.out.println("MySQL драйвер успешно загружен");
        } catch (ClassNotFoundException e) {
            System.err.println("Ошибка загрузки MySQL драйвера: " + e.getMessage());
            e.printStackTrace();
            throw new RuntimeException("Не удалось загрузить драйвер MySQL: " + e.getMessage(), e);
        }
    }

    public static Connection getConnection() throws SQLException {
        try {
            Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
            System.out.println("Успешное подключение к базе данных");
            return conn;
        } catch (SQLException e) {
            System.err.println("Ошибка подключения к базе данных: " + e.getMessage());
            e.printStackTrace();
            throw e;
        }
    }
} 