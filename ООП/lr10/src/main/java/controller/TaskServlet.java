package controller;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;
import model.Task;
import repository.TaskRepository;
import exception.ValidationException;
import view.JsonView;
import org.json.*;

import java.io.*;
import java.sql.SQLException;
import java.util.*;

@WebServlet("/tasks/*")
public class TaskServlet extends HttpServlet {
    private TaskRepository repository;

    @Override
    public void init() throws ServletException {
        try {
            repository = new TaskRepository();
        } catch (Exception e) {
            throw new ServletException("Ошибка инициализации хранилища задач", e);
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");

        String pathInfo = request.getPathInfo();
        
        try {
            if (pathInfo == null || pathInfo.equals("/")) {
                // Получить список всех задач
                List<Task> tasks = repository.getAll();
                response.getWriter().write(JsonView.toJson(tasks));
            } else {
                // Получить одну задачу по ID
                Long taskId = getTaskIdFromPath(pathInfo);
                Optional<Task> task = repository.getById(taskId);
                
                if (task.isPresent()) {
                    response.getWriter().write(JsonView.toJson(task.get()));
                } else {
                    response.setStatus(HttpServletResponse.SC_NOT_FOUND);
                    response.getWriter().write(JsonView.error("Задача с ID " + taskId + " не найдена"));
                }
            }
        } catch (NumberFormatException e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            response.getWriter().write(JsonView.error("Некорректный ID задачи"));
        } catch (SQLException e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            response.getWriter().write(JsonView.error("Ошибка при работе с базой данных: " + e.getMessage()));
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");

        try (BufferedReader reader = request.getReader()) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) sb.append(line);
            JSONObject json = new JSONObject(sb.toString());

            Task task = new Task(
                    json.getString("title"),
                    json.getString("description"),
                    json.getString("category"),
                    json.getString("dueDate"),
                    json.getString("priority")
            );
            validate(task);
            Task savedTask = repository.save(task);
            response.getWriter().write(JsonView.toJson(savedTask));

        } catch (JSONException | ValidationException e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            response.getWriter().write(JsonView.error(e.getMessage()));
        } catch (SQLException e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            response.getWriter().write(JsonView.error("Ошибка при сохранении задачи: " + e.getMessage()));
        }
    }
    
    @Override
    protected void doPut(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        
        String pathInfo = request.getPathInfo();
        
        try {
            if (pathInfo == null || pathInfo.equals("/")) {
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                response.getWriter().write(JsonView.error("ID задачи не указан"));
                return;
            }
            
            Long taskId = getTaskIdFromPath(pathInfo);
            
            BufferedReader reader = request.getReader();
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) sb.append(line);
            JSONObject json = new JSONObject(sb.toString());
            
            Optional<Task> existingTask = repository.getById(taskId);
            if (existingTask.isEmpty()) {
                response.setStatus(HttpServletResponse.SC_NOT_FOUND);
                response.getWriter().write(JsonView.error("Задача с ID " + taskId + " не найдена"));
                return;
            }
            
            Task task = new Task(
                    taskId,
                    json.getString("title"),
                    json.getString("description"),
                    json.getString("category"),
                    json.getString("dueDate"),
                    json.getString("priority")
            );
            
            validate(task);
            
            boolean updated = repository.update(task);
            if (updated) {
                response.getWriter().write(JsonView.toJson(task));
            } else {
                response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
                response.getWriter().write(JsonView.error("Не удалось обновить задачу"));
            }
            
        } catch (NumberFormatException e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            response.getWriter().write(JsonView.error("Некорректный ID задачи"));
        } catch (JSONException | ValidationException e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            response.getWriter().write(JsonView.error(e.getMessage()));
        } catch (SQLException e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            response.getWriter().write(JsonView.error("Ошибка при обновлении задачи: " + e.getMessage()));
        }
    }
    
    @Override
    protected void doDelete(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        
        String pathInfo = request.getPathInfo();
        
        try {
            if (pathInfo == null || pathInfo.equals("/")) {
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                response.getWriter().write(JsonView.error("ID задачи не указан"));
                return;
            }
            
            Long taskId = getTaskIdFromPath(pathInfo);
            
            boolean deleted = repository.delete(taskId);
            if (deleted) {
                response.getWriter().write(JsonView.success("Задача с ID " + taskId + " успешно удалена"));
            } else {
                response.setStatus(HttpServletResponse.SC_NOT_FOUND);
                response.getWriter().write(JsonView.error("Задача с ID " + taskId + " не найдена"));
            }
            
        } catch (NumberFormatException e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            response.getWriter().write(JsonView.error("Некорректный ID задачи"));
        } catch (SQLException e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            response.getWriter().write(JsonView.error("Ошибка при удалении задачи: " + e.getMessage()));
        }
    }

    private void validate(Task task) throws ValidationException {
        if (task.getTitle().isEmpty()) throw new ValidationException("Поле title обязательно");
        if (task.getDescription().isEmpty()) throw new ValidationException("Поле description обязательно");
        if (task.getCategory().isEmpty()) throw new ValidationException("Поле category обязательно");
        if (task.getDueDate().isEmpty()) throw new ValidationException("Поле dueDate обязательно");
        if (task.getPriority().isEmpty()) throw new ValidationException("Поле priority обязательно");
    }
    
    private Long getTaskIdFromPath(String pathInfo) {
        String[] pathParts = pathInfo.split("/");
        if (pathParts.length > 1) {
            return Long.parseLong(pathParts[1]);
        }
        throw new NumberFormatException("ID задачи не найден в пути");
    }
}