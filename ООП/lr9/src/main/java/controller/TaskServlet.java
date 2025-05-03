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
import java.nio.file.*;
import java.util.*;

@WebServlet("/tasks")
public class TaskServlet extends HttpServlet {
    private static final String RELATIVE_DATA_FILE = "WEB-INF/data/tasks.json";
    private TaskRepository repository;

    @Override
    public void init() throws ServletException {
        String appPath = getServletContext().getRealPath("");
        Path path = Paths.get(appPath, RELATIVE_DATA_FILE);
        try {
            repository = new TaskRepository(path);
        } catch (IOException e) {
            throw new ServletException("Ошибка инициализации хранилища задач", e);
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");

        try {
            List<Task> tasks = repository.getAll();
            response.getWriter().write(JsonView.toJson(tasks));
        } catch (IOException e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            response.getWriter().write(JsonView.error("Ошибка чтения задач"));
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
            repository.save(task);
            response.getWriter().write(JsonView.success("Задача успешно добавлена"));

        } catch (JSONException | ValidationException e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            response.getWriter().write(JsonView.error(e.getMessage()));
        } catch (IOException e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            response.getWriter().write(JsonView.error("Ошибка сохранения задачи"));
        }
    }

    private void validate(Task task) throws ValidationException {
        if (task.getTitle().isEmpty()) throw new ValidationException("Поле title обязательно");
        if (task.getDescription().isEmpty()) throw new ValidationException("Поле description обязательно");
        if (task.getCategory().isEmpty()) throw new ValidationException("Поле category обязательно");
        if (task.getDueDate().isEmpty()) throw new ValidationException("Поле dueDate обязательно");
        if (task.getPriority().isEmpty()) throw new ValidationException("Поле priority обязательно");
    }
}