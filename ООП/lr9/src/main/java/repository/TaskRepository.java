package repository;

import model.Task;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.nio.file.*;
import java.util.*;

public class TaskRepository {
    private final Path dataFilePath;

    public TaskRepository(Path dataFilePath) throws IOException {
        this.dataFilePath = dataFilePath;
        createDataFileIfNotExists();
    }

    private void createDataFileIfNotExists() throws IOException {
        if (!Files.exists(dataFilePath.getParent())) {
            Files.createDirectories(dataFilePath.getParent());
        }
        if (!Files.exists(dataFilePath)) {
            Files.write(dataFilePath, "[]".getBytes());
        }
    }

    public List<Task> getAll() throws IOException {
        String jsonData = new String(Files.readAllBytes(dataFilePath));
        JSONArray array = new JSONArray(jsonData);
        List<Task> tasks = new ArrayList<>();
        for (int i = 0; i < array.length(); i++) {
            JSONObject obj = array.getJSONObject(i);
            Task task = new Task(
                    obj.getString("title"),
                    obj.getString("description"),
                    obj.getString("category"),
                    obj.getString("dueDate"),
                    obj.getString("priority")
            );
            tasks.add(task);
        }
        return tasks;
    }

    public void save(Task task) throws IOException {
        List<Task> tasks = getAll();
        tasks.add(task);
        JSONArray array = new JSONArray();
        for (Task t : tasks) {
            JSONObject obj = new JSONObject();
            obj.put("title", t.getTitle());
            obj.put("description", t.getDescription());
            obj.put("category", t.getCategory());
            obj.put("dueDate", t.getDueDate());
            obj.put("priority", t.getPriority());
            array.put(obj);
        }
        Files.write(dataFilePath, array.toString().getBytes());
    }
}
