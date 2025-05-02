package lr8;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;

import java.io.*;
import java.nio.file.*;

import org.json.*;

@WebServlet("/tasks")
public class TaskServlet extends HttpServlet {
    private static final String RELATIVE_DATA_FILE = "WEB-INF/data/tasks.json";
    private Path dataFilePath;

    @Override
    public void init() throws ServletException {
        super.init();
        String appPath = getServletContext().getRealPath("");
        dataFilePath = Paths.get(appPath, RELATIVE_DATA_FILE);
        createDataFileIfNotExists();
    }

    private void createDataFileIfNotExists() throws ServletException {
        try {
            Path parentDir = dataFilePath.getParent();
            if (!Files.exists(parentDir)) {
                Files.createDirectories(parentDir);
            }
            if (!Files.exists(dataFilePath)) {
                Files.write(dataFilePath, "[]".getBytes());
            }
        } catch (IOException e) {
            throw new ServletException("Не удалось создать файл данных задач", e);
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");

        try {
            String jsonData = new String(Files.readAllBytes(dataFilePath));
            response.getWriter().write(jsonData);
        } catch (IOException e) {
            sendError(response, "Ошибка чтения данных задач", HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");

        try {
            StringBuilder sb = new StringBuilder();
            String line;
            BufferedReader reader = request.getReader();
            while ((line = reader.readLine()) != null) {
                sb.append(line);
            }

            JSONObject newTask = new JSONObject(sb.toString());
            validateTask(newTask);

            JSONArray taskArray = readExistingData();
            taskArray.put(newTask);

            saveData(taskArray);

            JSONObject successResponse = new JSONObject();
            successResponse.put("success", true);
            successResponse.put("message", "Задача успешно добавлена");
            response.getWriter().write(successResponse.toString());
        } catch (JSONException e) {
            sendError(response, "Неверный формат данных задачи", HttpServletResponse.SC_BAD_REQUEST);
        } catch (ValidationException e) {
            sendError(response, e.getMessage(), HttpServletResponse.SC_BAD_REQUEST);
        } catch (IOException e) {
            sendError(response, "Ошибка сохранения данных задачи", HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }

    private JSONArray readExistingData() throws IOException, JSONException {
        String jsonData = new String(Files.readAllBytes(dataFilePath));
        return new JSONArray(jsonData);
    }

    private void saveData(JSONArray data) throws IOException {
        Files.write(dataFilePath, data.toString().getBytes());
    }

    private void validateTask(JSONObject task) throws ValidationException {
        String[] requiredFields = {"title", "description", "category", "dueDate", "priority"};

        for (String field : requiredFields) {
            if (!task.has(field) || task.getString(field).isEmpty()) {
                throw new ValidationException("Поле " + field + " обязательно для заполнения");
            }
        }
    }

    private void sendError(HttpServletResponse response, String message, int statusCode) throws IOException {
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");

        response.setStatus(statusCode);
        JSONObject errorResponse = new JSONObject();
        errorResponse.put("success", false);
        errorResponse.put("message", message);
        response.getWriter().write(errorResponse.toString());
    }

    private static class ValidationException extends Exception {
        public ValidationException(String message) {
            super(message);
        }
    }
}
