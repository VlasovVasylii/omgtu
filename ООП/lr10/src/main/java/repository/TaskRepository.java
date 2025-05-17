package repository;

import model.Task;

import java.sql.*;
import java.util.*;

public class TaskRepository {
    
    public TaskRepository() {
        try {
            createTableIfNotExists();
        } catch (SQLException e) {
            throw new RuntimeException("Ошибка при инициализации репозитория задач", e);
        }
    }

    private void createTableIfNotExists() throws SQLException {
        String sql = "CREATE TABLE IF NOT EXISTS tasks (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY, " +
                "title VARCHAR(255) NOT NULL, " +
                "description TEXT NOT NULL, " +
                "category VARCHAR(100) NOT NULL, " +
                "due_date VARCHAR(50) NOT NULL, " +
                "priority VARCHAR(50) NOT NULL)";

        try (Connection conn = DatabaseConnection.getConnection();
             Statement stmt = conn.createStatement()) {
            stmt.execute(sql);
        }
    }

    // Создание новой задачи (Create)
    public Task save(Task task) throws SQLException {
        String sql = "INSERT INTO tasks (title, description, category, due_date, priority) VALUES (?, ?, ?, ?, ?)";
        
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            
            stmt.setString(1, task.getTitle());
            stmt.setString(2, task.getDescription());
            stmt.setString(3, task.getCategory());
            stmt.setString(4, task.getDueDate());
            stmt.setString(5, task.getPriority());
            
            int affectedRows = stmt.executeUpdate();
            
            if (affectedRows == 0) {
                throw new SQLException("Создание задачи не удалось, строки не изменены.");
            }
            
            try (ResultSet generatedKeys = stmt.getGeneratedKeys()) {
                if (generatedKeys.next()) {
                    task.setId(generatedKeys.getLong(1));
                } else {
                    throw new SQLException("Создание задачи не удалось, ID не получен.");
                }
            }
            return task;
        }
    }

    // Получение всех задач (Read all)
    public List<Task> getAll() throws SQLException {
        String sql = "SELECT id, title, description, category, due_date, priority FROM tasks";
        List<Task> tasks = new ArrayList<>();
        
        try (Connection conn = DatabaseConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                Task task = new Task(
                    rs.getLong("id"),
                    rs.getString("title"),
                    rs.getString("description"),
                    rs.getString("category"),
                    rs.getString("due_date"),
                    rs.getString("priority")
                );
                tasks.add(task);
            }
        }
        return tasks;
    }

    // Получение задачи по ID (Read one)
    public Optional<Task> getById(Long id) throws SQLException {
        String sql = "SELECT id, title, description, category, due_date, priority FROM tasks WHERE id = ?";
        
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setLong(1, id);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    Task task = new Task(
                        rs.getLong("id"),
                        rs.getString("title"),
                        rs.getString("description"),
                        rs.getString("category"),
                        rs.getString("due_date"),
                        rs.getString("priority")
                    );
                    return Optional.of(task);
                }
            }
        }
        return Optional.empty();
    }

    // Обновление задачи (Update)
    public boolean update(Task task) throws SQLException {
        String sql = "UPDATE tasks SET title = ?, description = ?, category = ?, due_date = ?, priority = ? WHERE id = ?";
        
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setString(1, task.getTitle());
            stmt.setString(2, task.getDescription());
            stmt.setString(3, task.getCategory());
            stmt.setString(4, task.getDueDate());
            stmt.setString(5, task.getPriority());
            stmt.setLong(6, task.getId());
            
            int affectedRows = stmt.executeUpdate();
            return affectedRows > 0;
        }
    }

    // Удаление задачи (Delete)
    public boolean delete(Long id) throws SQLException {
        String sql = "DELETE FROM tasks WHERE id = ?";
        
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setLong(1, id);
            
            int affectedRows = stmt.executeUpdate();
            return affectedRows > 0;
        }
    }
}
