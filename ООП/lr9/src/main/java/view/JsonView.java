package view;

import model.Task;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.List;

public class JsonView {
    public static String toJson(List<Task> tasks) {
        JSONArray array = new JSONArray();
        for (Task task : tasks) {
            JSONObject obj = new JSONObject();
            obj.put("title", task.getTitle());
            obj.put("description", task.getDescription());
            obj.put("category", task.getCategory());
            obj.put("dueDate", task.getDueDate());
            obj.put("priority", task.getPriority());
            array.put(obj);
        }
        return array.toString();
    }

    public static String success(String message) {
        JSONObject json = new JSONObject();
        json.put("success", true);
        json.put("message", message);
        return json.toString();
    }

    public static String error(String message) {
        JSONObject json = new JSONObject();
        json.put("success", false);
        json.put("message", message);
        return json.toString();
    }
}